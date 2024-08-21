"""Module implements common steps for operation on files (both regular files
and directories).
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from . import multi_file_steps
from tests.utils.bdd_utils import when, then, wt, parsers


@wt(parsers.re('(?P<user>\w+) creates regular files (?P<files>.*)'))
def create_reg_file(user, files, users, request):
    multi_file_steps.create_reg_file(user, files, 'client1', users, request)


@wt(parsers.re('(?P<user>\w+) creates child files of (?P<parent_dir>.*) '
               'with names in range \[(?P<lower>.*), (?P<upper>.*)\)'))
def create_many(user, lower: int, upper: int, parent_dir, users, request):
    multi_file_steps.create_many(user, lower, upper, parent_dir, 'client1',
                                 users, request)


@wt(parsers.re('(?P<user>\w+) can stat (?P<files>.*) in (?P<path>.*)'))
def stat_present(user, path, files, users):
    multi_file_steps.stat_present(user, path, files, 'client1', users)


@wt(parsers.re('(?P<user>\w+) sees (?P<files>.*) in (?P<path>.*)'))
def ls_present(user, files, path, users):
    multi_file_steps.ls_present(user, files, path, 'client1', users)


@wt(parsers.re('(?P<user>\w+) lists children of (?P<parent_dir>.*) and gets '
               'names in range \[(?P<lower>.*), (?P<upper>.*)\)'))
def ls_children(user, parent_dir, lower: int, upper: int, users):
    multi_file_steps.ls_children(user, parent_dir, lower, upper, 'client1',
                                 users)


@wt(parsers.re('(?P<user>\w+) renames (?P<file1>.*) to (?P<file2>.*)'))
def rename(user, file1, file2, users):
    multi_file_steps.rename(user, file1, file2, 'client1', users)


@wt(parsers.re('(?P<user>\w+) fails to rename (?P<file1>.*) to (?P<file2>.*)'))
def rename_fail(user, file1, file2, users):
    multi_file_steps.rename_fail(user, file1, file2, 'client1', users)


@wt(parsers.re('(?P<user>\w+) can\'t stat (?P<files>.*) in (?P<path>.*)'))
def stat_absent(user, path, files, users):
    multi_file_steps.stat_absent(user, path, files, 'client1', users)


@wt(parsers.re('(?P<user>\w+) doesn\'t see (?P<files>.*) in (?P<path>.*)'))
def ls_absent(user, files, path, users):
    multi_file_steps.ls_absent(user, files, path, 'client1', users)


@wt(parsers.re('(?P<user>\w+) fails to move (?P<file1>.*) to (?P<file2>.*)'
               ' using shell command'))
def shell_move_fail(user, file1, file2, users):
    multi_file_steps.shell_move_fail(user, file1, file2, 'client1', users)


@wt(parsers.re('(?P<user>\w+) deletes files (?P<files>.*)'))
def delete_file(user, files, users):
    multi_file_steps.delete_file(user, files, 'client1', users)


@wt(parsers.re('(?P<user>\w+) fails to delete files (?P<files>.*)'))
def delete_file_fail(user, files, users):
    multi_file_steps.delete_file_fail(user, files, users)


@wt(parsers.re('size of (?P<user>\w+)\'s (?P<file>.*) is (?P<size>.*) bytes'))
def check_size(user, file, size, users):
    multi_file_steps.check_size(user, file, size, 'client1', users)


@then(parsers.re('file type of (?P<user>\w+)\'s (?P<file>.*) is '
                 '(?P<file_type>.*)'))
def check_type(user, file, file_type, users):
    multi_file_steps.check_type(user, file, file_type, 'client1', users)


@then(parsers.re('(?P<user>\w+) checks using shell stat if file type of '
                 '(?P<file>.*) is (?P<file_type>.*)'))
def shell_check_type(user, file, file_type, users):
    multi_file_steps.shell_check_type(user, file, file_type, 'client1', users)


@then(parsers.re('mode of (?P<user>\w+)\'s (?P<file>.*) is (?P<mode>.*)'))
def check_mode(user, file, mode, users):
    multi_file_steps.check_mode(user, file, mode, 'client1', users)


@wt(parsers.re('(?P<user>\w+) changes (?P<file>.*) mode to (?P<mode>.*)'))
def change_mode(user, file, mode, users):
    multi_file_steps.change_mode(user, file, mode, 'client1', users)


@wt(parsers.re('(?P<user>\w+) fails to change (?P<file>.*) mode to (?P<mode>.*)'))
def change_mode_fail(user, file, mode, users):
    multi_file_steps.change_mode_fail(user, file, mode, users)


@then(parsers.re('(?P<time1>.*) time of (?P<user>\w+)\'s (?P<file>.*)'
                 ' is (?P<comparator>.*) than (?P<time2>.*) time'))
@then(parsers.re('(?P<time1>.*) time of (?P<user>\w+)\'s (?P<file>.*)'
                 ' is (?P<comparator>.*) to (?P<time2>.*) time'))
def check_time(user, time1, time2, comparator, file, users):
    multi_file_steps.check_time(user, time1, time2, comparator, file,
                                'client1', users)


@when(parsers.re('(?P<user>\w+) updates (?P<files>.*) timestamps'))
def touch_file(user, files, users):
    multi_file_steps.touch_file(user, files, 'client1', users)


@when(parsers.re('(?P<user>\w+) fails to update (?P<files>.*) timestamps'))
def touch_file_fail(user, files, users):
    multi_file_steps.touch_file_fail(user, files, users)
