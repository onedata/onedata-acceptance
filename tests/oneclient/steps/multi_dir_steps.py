"""Module implements pytest-bdd steps for operations on directories in
multiclient environment.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import errno

from pytest_bdd import parsers, when

from tests.utils.acceptance_utils import wt, list_parser
from tests.utils.utils import assert_generic, assert_
from tests.utils.client_utils import mkdir, rmdir, ls, rm, cp


def create_base(user, dirs, client_node, users, should_fail=False):
    dirs = list_parser(dirs)
    user = users[user]
    client = user.clients[client_node] 

    for dir in dirs:
        path = client.absolute_path(dir)

        def condition():
            mkdir(client, path)
        assert_generic(client.perform, should_fail, condition)


@when(parsers.re('(?P<user>\w+) creates directories (?P<dirs>.*)\son '
                 '(?P<client_node>.*)'))
def create(user, dirs, client_node, users):
    create_base(user, dirs, client_node, users)


@when(parsers.re('(?P<user>\w+) creates directory and parents (?P<paths>.*)\s'
                 'on (?P<client_node>.*)'))
def create_parents(user, paths, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    paths = list_parser(paths)

    for path in paths:
        dir_path = client.absolute_path(path)

        def condition():
            mkdir(client, dir_path, recursive=True)

        assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) fails to create directories (?P<dirs>.*)\son '
               '(?P<client_node>.*)'))
def fail_to_create(user, dirs, client_node, users):
    create_base(user, dirs, client_node, users, should_fail=True)


def delete_empty_base(user, dirs, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    dirs = list_parser(dirs)

    for dir in dirs:
        path = client.absolute_path(dir)

        def condition():
            rmdir(client, path)

        assert_generic(client.perform, should_fail, condition)


@wt(parsers.re('(?P<user>\w+) deletes directories \(rmdir\) (?P<dirs>.*) on '
               '(?P<client_node>.*)'))
def delete_empty(user, dirs, client_node, users):
    delete_empty_base(user, dirs, client_node, users)


@wt(parsers.re('(?P<user>\w+) fails to delete directories \(rmdir\) '
               '(?P<dirs>.*) on (?P<client_node>.*)'))
def fail_to_delete_empty(user, dirs, client_node, users):
    delete_empty_base(user, dirs, client_node, users, should_fail=True)


@wt(parsers.re('(?P<user>\w+) deletes directories \(rm -rf\) (?P<dirs>.*) on '
               '(?P<client_node>.*)'))
def delete_non_empty(user, dirs, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    dirs = list_parser(dirs)

    for dir in dirs:
        path = client.absolute_path(dir)

        def condition():
            rm(client, path, recursive=True, force=True)

        assert_(client.perform, condition)


@when(parsers.re('(?P<user>\w+) deletes directory \(rmdir -p\) '
                 '(?P<paths>.*) on (?P<client_node>.*)'))
def delete_parents(user, paths, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    paths = list_parser(paths)

    for path in paths:
        dir_path = client.absolute_path(path)

        def condition():
            rmdir(client, dir_path, recursive=True)

        assert_(client.perform, condition)


def list_dirs_base(user, dir, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    path = client.absolute_path(dir)
    path_content = []

    def condition():
        try:
            content = ls(client, path=path)
            path_content.extend(content)
        except OSError as ex:
            if ex.errno == errno.EPERM:
                return True if should_fail else False
            raise ex
        else:
            return False if should_fail else True

    assert_generic(client.perform, should_fail, condition)
    return path_content


@wt(parsers.re('(?P<user>\w+) can list (?P<dir>.*) on '
               '(?P<client_node>.*)'))
def list_dir(user, dir, client_node, users):
    list_dirs_base(user, dir, client_node, users)


@wt(parsers.re('(?P<user>\w+) can\'t list (?P<dir>.*) on (?P<client_node>.*)'))
def cannot_list_dir(user, dir, client_node, users):
    list_dirs_base(user, dir, client_node, users, should_fail=True)


@when(parsers.re('(?P<user>\w+) copies directory (?P<dir1>.*) to (?P<dir2>.*) '
                 'on (?P<client_node>.*)'))
def copy_dir(user, dir1, dir2, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    src_path = client.absolute_path(dir1)
    dest_path = client.absolute_path(dir2)

    def condition():
        cp(client, src_path, dest_path, recursive=True)

    assert_(client.perform, condition)
