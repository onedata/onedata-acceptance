"""Module implements pytest-bdd steps for operations on directories in
multiclient environment.
"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import errno
import os.path
import subprocess as sp
import time
from typing import Literal

from tests.oneclient.constants import ONECLIENT_REPEATS_INTERVAL as INTERVAL
from tests.type_definitions import Hosts
from tests.utils import ONECLIENT_MOUNT_DIR
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, parsers, when, wt
from tests.utils.client_utils import Client
from tests.utils.onenv_utils import cmd_exec
from tests.utils.user_utils import Users
from tests.utils.utils import assert_with_expected_fail, perform_action_with_timeout


def try_to_create_directory(
    user: str,
    client_node: str,
    dir_name: str,
    users: Users,
    should_fail: bool = False,
    recursive: bool = False,
    exist_ok: bool = False,
) -> None:
    client = users[user].clients[client_node]
    absolute_path = client.absolute_path(dir_name)

    def condition() -> None:
        client.mkdir(absolute_path, recursive=recursive, exist_ok=exist_ok)

    assert_with_expected_fail(
        condition,
        timeout=client.timeout,
        should_fail=should_fail,
        message="Directory creation succeeded, expected it to fail",
        exceptions=OSError if should_fail else Exception,
    )


@wt(
    parsers.re(
        r"(?P<user>\w+) (?P<result>succeeds|fails) to create directories "
        r"(?P<dir_names>.*) on (?P<client_node>.*)"
    ),
    converters={
        "dir_names": list_parser,
    },
)
def try_to_create_directories(
    user: str,
    dir_names: list[str],
    client_node: str,
    users: Users,
    result: Literal["succeeds", "fails"],
) -> None:
    should_fail = result == "fails"
    for dir_name in dir_names:
        try_to_create_directory(user, client_node, dir_name, users, should_fail=should_fail)


@when(
    parsers.parse(
        "{user} creates directory and parents {paths} on {client_node}",
    ),
    converters={"paths": list_parser},
)
def create_directory_and_parents(user: str, paths: str, client_node: str, users: Users) -> None:
    for path in paths:
        try_to_create_directory(user, client_node, path, users, recursive=True)


def try_to_remove_directory(
    user_name: str,
    client_node: str,
    dir_name: str,
    should_fail: bool,
    users: Users,
) -> None:
    user = users[user_name]
    client = user.clients[client_node]
    absolute_path = client.absolute_path(dir_name)

    def assert_action() -> None:
        try:
            client.rmdir(absolute_path)
        except OSError as e:
            if not should_fail:
                raise AssertionError("Failed to create base directory") from e

    perform_action_with_timeout(assert_action, client.timeout, interval=INTERVAL)


def delete_empty_base(
    user: str, dirs: str, client_node: str, users: Users, should_fail: bool = False
) -> None:
    dir_names = list_parser(dirs)

    for dir_name in dir_names:
        try_to_remove_directory(user, client_node, dir_name, should_fail, users)


@wt(
    parsers.re(
        r"(?P<user>\w+) deletes directories \(rmdir\) (?P<dirs>.*) "
        r"on (?P<client_node>.*)"
    )
)
def delete_empty(user: str, dirs: str, client_node: str, users: Users) -> None:
    delete_empty_base(user, dirs, client_node, users)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to delete directories \(rmdir\) "
        r"(?P<dirs>.*) on (?P<client_node>.*)"
    )
)
def fail_to_delete_empty(user: str, dirs: str, client_node: str, users: Users) -> None:
    delete_empty_base(user, dirs, client_node, users, should_fail=True)


def purge_all_spaces(client: Client) -> None:
    try:
        retry_delay = 5

        spaces = client.list_spaces()

        for space in spaces:
            space_path = client.absolute_path(space)
            retries = 10
            space_purged = False
            while retries > 0 and not space_purged:
                try:
                    print(f"\nCleaning space {space_path} (retries left {retries})")
                    client.rm(path=space_path, recursive=True)
                    space_purged = True
                except FileNotFoundError:
                    space_purged = True
                except OSError as e:
                    if e.errno in (errno.ENOTEMPTY, errno.EAGAIN) and (retries > 0):
                        # retry in case events between providers haven't synchronized yet
                        retries = retries - 1
                        time.sleep(retry_delay)
                    elif e.errno in (errno.EPERM, errno.EACCES, errno.EIO):
                        # ignore permission errors during cleaning
                        space_purged = True
                    else:
                        print(f"Unexpected error '{e.errno}' when cleaning space: {space_path}")
                        raise e
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error during cleaning up spaces: {e}")
        raise e


@wt(parsers.re(r"(?P<user>\w+) purges all spaces on (?P<client_node>.*)"))
def purge_all_user_spaces(user: str, client_node: str, users: Users) -> None:
    client = users[user].clients[client_node]
    purge_all_spaces(client)


def force_remove_directory(user_name: str, client_node: str, dir_path: str, users: Users) -> None:
    user = users[user_name]
    client = user.clients[client_node]
    absolute_path = client.absolute_path(dir_path)

    def assert_action() -> None:
        client.rm(absolute_path, recursive=True, force=True)

    perform_action_with_timeout(assert_action, client.timeout, interval=INTERVAL)


@wt(
    parsers.re(
        r"(?P<user>\w+) deletes directories \(rm -rf\) (?P<dirs>.*) "
        r"on (?P<client_node>.*)"
    )
)
def delete_non_empty(user: str, dirs: str, client_node: str, users: Users) -> None:
    dir_names = list_parser(dirs)
    for dir_name in dir_names:
        force_remove_directory(user, client_node, dir_name, users)


def try_to_delete_root_dir(user: str, client_node: str, users: Users) -> None:
    client = users[user].clients[client_node]
    client.rm(client.get_mount_path(), recursive=True)


def try_to_move_root_dir(user: str, client_node: str, users: Users, dst: str) -> None:
    client = users[user].clients[client_node]
    client.mv(client.get_mount_path(), os.path.join(ONECLIENT_MOUNT_DIR, dst))


def move_dir_by_id(user: str, client_node: str, users: Users, file_id: str, dst: str) -> None:
    client = users[user].clients[client_node]
    client.mv(
        f"{client.get_mount_path()}/.__onedata__file_id__{file_id}",
        os.path.join(ONECLIENT_MOUNT_DIR, dst),
    )


def delete_dir_by_id(user: str, client_node: str, users: Users, file_id: str) -> None:
    client = users[user].clients[client_node]
    client.rm(
        f"{client.get_mount_path()}/.__onedata__file_id__{file_id}",
        recursive=True,
    )


def remove_directory(user_name: str, client_node: str, dir_path: str, users: Users) -> None:
    user = users[user_name]
    client = user.clients[client_node]
    absolute_path = client.absolute_path(dir_path)

    def assert_action() -> None:
        client.rmdir(absolute_path, recursive=True)

    perform_action_with_timeout(assert_action, client.timeout, interval=INTERVAL)


@when(
    parsers.re(
        r"(?P<user>\w+) deletes directory \(rmdir -p\) "
        r"(?P<paths>.*) on (?P<client_node>.*)"
    )
)
def delete_parents(user: str, paths: str, client_node: str, users: Users) -> None:
    path_names = list_parser(paths)

    for path in path_names:
        remove_directory(user, client_node, path, users)


def list_dirs_base(
    user: str,
    directory: str,
    client_node: str,
    users: Users,
    should_fail: bool = False,
) -> list[str]:
    client = users[user].clients[client_node]
    path = client.absolute_path(directory)
    path_content: list[str] = []

    def condition() -> None:
        try:
            content = client.ls(path=path)
        except OSError as ex:
            if ex.errno == errno.EPERM:
                raise PermissionError(ex.errno, ex.strerror, ex.filename) from ex
            raise
        path_content[:] = content

    assert_with_expected_fail(
        condition,
        client.timeout,
        should_fail=should_fail,
        exceptions=PermissionError if should_fail else Exception,
    )
    return path_content


@wt(parsers.re(r"(?P<user>\w+) can list (?P<directory>.*) on (?P<client_node>.*)"))
def list_dir(user: str, directory: str, client_node: str, users: Users) -> None:
    list_dirs_base(user, directory, client_node, users)


@wt(parsers.re(r"(?P<user>\w+) can't list (?P<directory>.*) on (?P<client_node>.*)"))
def cannot_list_dir(user: str, directory: str, client_node: str, users: Users) -> None:
    list_dirs_base(user, directory, client_node, users, should_fail=True)


@when(
    parsers.re(
        r"(?P<user>\w+) copies directory (?P<dir1>.*) to (?P<dir2>.*) "
        r"on (?P<client_node>.*)"
    )
)
def copy_dir(user: str, dir1: str, dir2: str, client_node: str, users: Users) -> None:
    client = users[user].clients[client_node]
    src_path = client.absolute_path(dir1)
    dest_path = client.absolute_path(dir2)

    def assert_action() -> None:
        client.cp(src_path, dest_path, recursive=True)

    perform_action_with_timeout(assert_action, client.timeout, interval=INTERVAL)


@given(
    parsers.re(
        r"there (is|are) director(y|ies) (?P<paths>.*) owned by "
        r"(?P<uid>.*):(?P<gid>.*) in container "
        r'"(?P<container>.*)" on provider "(?P<provider>.*)"'
    )
)
def create_in_container(
    uid: str, gid: str, paths: str, container: str, provider: str, hosts: Hosts
) -> None:
    for path in list_parser(paths):
        pod_name = hosts[provider]["pod_name"]
        mkdir_cmd = ["sh", "-c", f"mkdir {path}"]
        sp.call(cmd_exec(pod_name, mkdir_cmd, container=container))
        chown_cmd = ["sh", "-c", f"chown {uid}:{gid} {path}"]
        sp.call(cmd_exec(pod_name, chown_cmd, container=container))


@wt(
    parsers.re(
        r"delete is performed on director(y|ies) (?P<paths>.*) in "
        r'container "(?P<container>.*)" on provider "(?P<provider>.*)"'
    )
)
def remove_in_container(paths: str, container: str, provider: str, hosts: Hosts) -> None:
    for path in list_parser(paths):
        pod_name = hosts[provider]["pod_name"]
        cmd = ["sh", "-c", f"rm -rf {path}"]
        sp.call(cmd_exec(pod_name, cmd, container=container))
