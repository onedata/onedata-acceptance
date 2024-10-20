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

from tests.utils import ONECLIENT_MOUNT_DIR
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, parsers, when, wt
from tests.utils.onenv_utils import cmd_exec
from tests.utils.utils import assert_, assert_expected_failure, assert_generic


def create_base(user, dirs, client_node, users, should_fail=False, exists_ok=False):
    dirs = list_parser(dirs)
    user = users[user]
    client = user.clients[client_node]

    for _dir in dirs:
        path = client.absolute_path(_dir)

        def condition():
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
def create_(user, dirs, client_node, users):
    create(user, dirs, client_node, users)


def create(user, dirs, client_node, users, exists_ok=False):
    create_base(user, dirs, client_node, users, exists_ok=exists_ok)


@when(
    parsers.re(
        r"(?P<user>\w+) creates directory and parents (?P<paths>.*)\s"
        "on (?P<client_node>.*)"
    )
)
def create_parents(user, paths, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    paths = list_parser(paths)

    for path in paths:
        dir_path = client.absolute_path(path)

        def condition():
            client.mkdir(dir_path, recursive=True)

        assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to create directories (?P<dirs>.*)\son "
        "(?P<client_node>.*)"
    )
)
def fail_to_create(user, dirs, client_node, users):
    create_base(user, dirs, client_node, users, should_fail=True)


def delete_empty_base(user, dirs, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    dirs = list_parser(dirs)

    for _dir in dirs:
        path = client.absolute_path(_dir)

        def condition():
            client.rmdir(path)

        if should_fail:
            assert_expected_failure(condition)
        else:
            assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) deletes directories \(rmdir\) (?P<dirs>.*) on "
        "(?P<client_node>.*)"
    )
)
def delete_empty(user, dirs, client_node, users):
    delete_empty_base(user, dirs, client_node, users)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to delete directories \(rmdir\) "
        "(?P<dirs>.*) on (?P<client_node>.*)"
    )
)
def fail_to_delete_empty(user, dirs, client_node, users):
    delete_empty_base(user, dirs, client_node, users, should_fail=True)


def purge_all_spaces(client):
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
def purge_all_user_spaces(user, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    purge_all_spaces(client)


@wt(
    parsers.re(
        r"(?P<user>\w+) deletes directories \(rm -rf\) (?P<dirs>.*) on "
        "(?P<client_node>.*)"
    )
)
def delete_non_empty(user, dirs, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    dirs = list_parser(dirs)

    for _dir in dirs:
        path = client.absolute_path(_dir)

        def condition():
            client.rm(path, recursive=True, force=True)

        assert_(client.perform, condition)


def try_to_delete_root_dir(user, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    client.rm(client.get_mount_path(), recursive=True)


def try_to_move_root_dir(user, client_node, users, dst):
    user = users[user]
    client = user.clients[client_node]
    client.mv(client.get_mount_path(), os.path.join(ONECLIENT_MOUNT_DIR, dst))


def move_dir_by_id(user, client_node, users, file_id, dst):
    user = users[user]
    client = user.clients[client_node]
    client.mv(
        f"{client.get_mount_path()}/.__onedata__file_id__{file_id}",
        os.path.join(ONECLIENT_MOUNT_DIR, dst),
    )


def delete_dir_by_id(user, client_node, users, file_id):
    user = users[user]
    client = user.clients[client_node]
    client.rm(
        f"{client.get_mount_path()}/.__onedata__file_id__{file_id}",
        recursive=True,
    )


@when(
    parsers.re(
        r"(?P<user>\w+) deletes directory \(rmdir -p\) "
        "(?P<paths>.*) on (?P<client_node>.*)"
    )
)
def delete_parents(user, paths, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    paths = list_parser(paths)

    for path in paths:
        dir_path = client.absolute_path(path)

        def condition():
            client.rmdir(dir_path, recursive=True)

        assert_(client.perform, condition)


def list_dirs_base(user, directory, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    path = client.absolute_path(directory)
    path_content = []

    def condition():
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
def list_dir(user, directory, client_node, users):
    list_dirs_base(user, directory, client_node, users)


@wt(parsers.re(r"(?P<user>\w+) can't list (?P<directory>.*) on (?P<client_node>.*)"))
def cannot_list_dir(user, directory, client_node, users):
    list_dirs_base(user, directory, client_node, users, should_fail=True)


@when(
    parsers.re(
        r"(?P<user>\w+) copies directory (?P<dir1>.*) to (?P<dir2>.*) "
        "on (?P<client_node>.*)"
    )
)
def copy_dir(user, dir1, dir2, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    src_path = client.absolute_path(dir1)
    dest_path = client.absolute_path(dir2)

    def condition():
        client.cp(src_path, dest_path, recursive=True)

    assert_(client.perform, condition)


@given(
    parsers.re(
        "there (is|are) director(y|ies) (?P<paths>.*) owned by "
        "(?P<uid>.*):(?P<gid>.*) in container "
        '"(?P<container>.*)" on provider "(?P<provider>.*)"'
    )
)
def create_in_container(uid, gid, paths, container, provider, hosts):
    for path in list_parser(paths):
        pod_name = hosts[provider]["pod-name"]
        mkdir_cmd = ["sh", "-c", f"mkdir {path}"]
        sp.call(cmd_exec(pod_name, mkdir_cmd, container=container))
        chown_cmd = ["sh", "-c", f"chown {uid}:{gid} {path}"]
        sp.call(cmd_exec(pod_name, chown_cmd, container=container))


@wt(
    parsers.re(
        "delete is performed on director(y|ies) (?P<paths>.*) in "
        'container "(?P<container>.*)" on provider '
        '"(?P<provider>.*)"'
    )
)
def remove_in_container(paths, container, provider, hosts):
    for path in list_parser(paths):
        pod_name = hosts[provider]["pod-name"]
        cmd = ["sh", "-c", f"rm -rf {path}"]
        sp.call(cmd_exec(pod_name, cmd, container=container))
