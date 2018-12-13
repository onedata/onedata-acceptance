"""Module implements pytest-bdd steps for operations on directories.
"""
__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from pytest_bdd import parsers, when

import multi_dir_steps
from tests.utils.acceptance_utils import wt


@when(parsers.re('(?P<user>\w+) creates directories (?P<dirs>.*)'))
def create(user, dirs, users):
    multi_dir_steps.create(user, dirs, 'client1', users)


@wt(parsers.re('(?P<user>\w+) fails to create directories (?P<dirs>.*)'))
def cannot_create(user, dirs, users):
    multi_dir_steps.fail_to_create(user, dirs, 'client1', users)


@when(parsers.re('(?P<user>\w+) creates directory and parents (?P<paths>.*)'))
def create_parents(user, paths, users):
    multi_dir_steps.create_parents(user, paths, 'client1', users)


@wt(parsers.re('(?P<user>\w+) deletes directories \(rmdir\) (?P<dirs>.*)'))
def delete_empty(user, dirs, users):
    multi_dir_steps.delete_empty(user, dirs, 'client1', users)


@wt(parsers.re('(?P<user>\w+) fails to delete directories \(rmdir\) '
               '(?P<dirs>.*)'))
def fail_to_delete_empty(user, dirs, users):
    multi_dir_steps.fail_to_delete_empty(user, dirs, 'client1', users)


@when(parsers.re('(?P<user>\w+) deletes directories \(rm -rf\) (?P<dirs>.*)'))
def delete_non_empty(user, dirs, users):
    multi_dir_steps.delete_non_empty(user, dirs, 'client1', users)


@when(parsers.re('(?P<user>\w+) deletes directory \(rmdir -p\) '
                 '(?P<paths>.*)'))
def delete_parents(user, paths, users):
    multi_dir_steps.delete_parents(user, paths, 'client1', users)


@wt(parsers.re('(?P<user>\w+) can list (?P<dir>.*)'))
def list_dir(user, dir, users):
    multi_dir_steps.list_dir(user, dir, 'client1', users)


@wt(parsers.re('(?P<user>\w+) can\'t list (?P<dir>.*)'))
def cannot_list_dir(user, dir, users):
    multi_dir_steps.cannot_list_dir(user, dir, "client1", users)


@when(parsers.re('(?P<user>\w+) copies directory (?P<dir1>.*) to '
                 '(?P<dir2>.*)'))
def copy_dir(user, dir1, dir2, users):
    multi_dir_steps.copy_dir(user, dir1, dir2, 'client1', users)
