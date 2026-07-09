"""Module implements pytest-bdd steps for operations on directories in
multiclient environment.
"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"
# pylint: disable=cell-var-from-loop, deprecated-method

import errno
import os.path
import subprocess as sp

from tests.type_definitions import Hosts
from tests.utils import ONECLIENT_MOUNT_DIR
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, parsers, when, wt
from tests.utils.client_utils import Client
from tests.utils.onenv_utils import cmd_exec
from tests.utils.user_utils import Users
from tests.utils.utils import assert_, assert_expected_failure, assert_generic


def create_base(
    user: str,
    dirs: str,
    client_node: str,
    users: Users,
    should_fail: bool = False,
    exists_ok: bool = False,
) -> None:
    dir_names = list_parser(dirs)
    client = users[user].clients[client_node]

    for _dir in dir_names:
        path = client.absolute_path(_dir)

        def condition() -> None:
            client.mkdir(path, exist_ok=exists_ok)

        if should_fail:
            assert_expected_failure(condition)
        else:
            assert_(client.perform, condition)


@when(
    parsers.re(
        r"(?P<user>\w+) creates directories (?P<dirs>.*)\son (?P<client_node>.*)"
    )
)
def create_(user: str, dirs: str, client_node: str, users: Users) -> None:
    create(user, dirs, client_node, users)


def create(
    user: str, dirs: str, client_node: str, users: Users, exists_ok: bool = False
) -> None:
    create_base(user, dirs, client_node, users, exists_ok=exists_ok)


@when(
    parsers.re(
        r"(?P<user>\w+) creates directory and parents (?P<paths>.*)\s"
        r"on (?P<client_node>.*)"
    )
)
def create_parents(user: str, paths: str, client_node: str, users: Users) -> None:
    client = users[user].clients[client_node]
    path_names = list_parser(paths)

    for path in path_names:
        dir_path = client.absolute_path(path)

        def condition() -> None:
            client.mkdir(dir_path, recursive=True)

        assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to create directories (?P<dirs>.*)\son "
        r"(?P<client_node>.*)"
    )
)
def fail_to_create(user: str, dirs: str, client_node: str, users: Users) -> None:
    create_base(user, dirs, client_node, users, should_fail=True)


def delete_empty_base(
    user: str, dirs: str, client_node: str, users: Users, should_fail: bool = False
) -> None:
    client = users[user].clients[client_node]
    dir_names = list_parser(dirs)

    for _dir in dir_names:
        path = client.absolute_path(_dir)

        def condition() -> None:
            client.rmdir(path)

        if should_fail:
            assert_expected_failure(condition)
        else:
            assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) deletes directories \(rmdir\) (?P<dirs>.*) on "
        r"(?P<client_node>.*)"
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
        spaces = client.list_spaces()
        for space in spaces:
            space_path = client.absolute_path(space)
            try:
                client.rm(path=space_path, recursive=True)
            except FileNotFoundError:
                pass
            except OSError as e:
                # ignore EACCES errors during cleaning
                if e.errno == errno.EACCES:
                    pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Error during cleaning up spaces: {e}")
        raise e


@wt(parsers.re(r"(?P<user>\w+) purges all spaces on (?P<client_node>.*)"))
def purge_all_user_spaces(user: str, client_node: str, users: Users) -> None:
    client = users[user].clients[client_node]
    purge_all_spaces(client)


@wt(
    parsers.re(
        r"(?P<user>\w+) deletes directories \(rm -rf\) (?P<dirs>.*) on "
        r"(?P<client_node>.*)"
    )
)
def delete_non_empty(user: str, dirs: str, client_node: str, users: Users) -> None:
    client = users[user].clients[client_node]
    dir_names = list_parser(dirs)

    for _dir in dir_names:
        path = client.absolute_path(_dir)

        def condition() -> None:
            client.rm(path, recursive=True, force=True)

        assert_(client.perform, condition)


def try_to_delete_root_dir(user: str, client_node: str, users: Users) -> None:
    client = users[user].clients[client_node]
    client.rm(client.get_mount_path(), recursive=True)


def try_to_move_root_dir(user: str, client_node: str, users: Users, dst: str) -> None:
    client = users[user].clients[client_node]
    client.mv(client.get_mount_path(), os.path.join(ONECLIENT_MOUNT_DIR, dst))


def move_dir_by_id(
    user: str, client_node: str, users: Users, file_id: str, dst: str
) -> None:
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


@when(
    parsers.re(
        r"(?P<user>\w+) deletes directory \(rmdir -p\) "
        r"(?P<paths>.*) on (?P<client_node>.*)"
    )
)
def delete_parents(user: str, paths: str, client_node: str, users: Users) -> None:
    client = users[user].clients[client_node]
    path_names = list_parser(paths)

    for path in path_names:
        dir_path = client.absolute_path(path)

        def condition() -> None:
            client.rmdir(dir_path, recursive=True)

        assert_(client.perform, condition)


def list_dirs_base(
    user: str,
    directory: str,
    client_node: str,
    users: Users,
    should_fail: bool = False,
) -> list[str]:
    client = users[user].clients[client_node]
    path = client.absolute_path(directory)
    path_content = []

    def condition() -> bool:
        try:
            content = client.ls(path=path)
            path_content.extend(content)
        except OSError as ex:
            if ex.errno == errno.EPERM:
                return bool(should_fail)
            raise ex
        return not bool(should_fail)

    assert_generic(client.perform, should_fail, condition)
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

    def condition() -> None:
        client.cp(src_path, dest_path, recursive=True)

    assert_(client.perform, condition)


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
        r'container "(?P<container>.*)" on provider '
        r'"(?P<provider>.*)"'
    )
)
def remove_in_container(
    paths: str, container: str, provider: str, hosts: Hosts
) -> None:
    for path in list_parser(paths):
        pod_name = hosts[provider]["pod_name"]
        cmd = ["sh", "-c", f"rm -rf {path}"]
        sp.call(cmd_exec(pod_name, cmd, container=container))
