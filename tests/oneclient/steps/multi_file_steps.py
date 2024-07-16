"""Module implements common steps for operation on files (both regular files
and directories)in multi-client environment.
"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import os
import re
import json
import stat as stat_lib
import subprocess as sp
import time
import random
import string

import jsondiff

from tests.utils.acceptance_utils import (list_parser, make_arg_list,
                                          compare, time_attr)
from tests.utils.bdd_utils import when, then, wt, parsers
from tests.utils.utils import assert_, assert_generic, assert_expected_failure, repeat_failed
from tests.utils.onenv_utils import cmd_exec
from tests.utils.client_utils import create_hardlink, create_symlink
from tests.oneclient.steps.multi_dir_steps import create

HARDLINKS_DIR = '.hardlinks'
SYMLINKS_DIR = '.symlinks'


def create_base(user, files, client_node, users, request, should_fail=False):
    files = list_parser(files)
    user_ = users[user]
    client = user_.clients[client_node]
    mode = request.config.getoption('file_mode')

    for file_name in files:
        # path for original file in hardlink/symlink mode
        # space_name/(.hardlinks or .symlinks)/(random string)

        path = client.absolute_path(file_name)
        if mode == 'regular':

            def condition():
                client.create_file(path)

        elif mode == 'hardlink':
            org_file_path = get_org_file_path(user, client, client_node, users,
                                              file_name, HARDLINKS_DIR)

            def condition():
                client.create_file(org_file_path)
                create_hardlink(client, org_file_path, path)

        elif mode == 'symlink':
            org_file_path = get_org_file_path(user, client, client_node, users,
                                              file_name, SYMLINKS_DIR)

            def condition():
                client.create_file(org_file_path)
                create_symlink(client, org_file_path, path)

        else:
            raise Exception

        try:
            assert_generic(client.perform, should_fail, condition)
        except Exception as e:
            print(e)


def get_org_file_path(user, client, client_node, users, file_name, dir_name):
    space = file_name.split('/')[0]
    create(user, f'[{space}/{dir_name}]', client_node, users,
           exists_ok=True)
    file_name_hash = ''.join(
        random.choice(string.ascii_lowercase + string.digits) for _ in
        range(16))
    org_file_path = os.path.join(space, dir_name, file_name_hash)
    org_file_path = client.absolute_path(org_file_path)
    return org_file_path


@wt(parsers.re('(?P<user>\w+) creates regular files (?P<files>.*) '
               'on (?P<client_node>.*)'))
def create_reg_file(user, files, client_node, users, request):
    create_base(user, files, client_node, users, request)


@wt(parsers.re('(?P<user>\w+) fails to create regular files (?P<files>.*) '
               'on (?P<client_node>.*)'))
def create_reg_file_fail(user, files, client_node, users, request):
    create_base(user, files, client_node, users, request, should_fail=True)


@wt(parsers.re('(?P<user>\w+) creates child files of (?P<parent_dir>.*) '
               'with names in range \[(?P<lower>.*), (?P<upper>.*)\) on '
               '(?P<client_node>.*)'))
def create_many(user, lower: int, upper: int, parent_dir, client_node, users, request):
    for i in range(lower, upper):
        new_file = os.path.join(parent_dir, str(i))
        create_reg_file(user, make_arg_list(new_file), client_node, users, request)


@wt(parsers.re('(?P<user>\w+) can stat (?P<files>.*) in (?P<path>.*)'
               ' on (?P<client_node>.*)'))
def stat_present(user, path, files, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    path = client.absolute_path(path)
    files = list_parser(files)

    def condition():
        for f in files:
            client.stat(os.path.join(path, f))

    assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) sees (?P<files>.*) in (?P<path>.*) '
               'on (?P<client_node>.*)'))
def ls_present(user, files, path, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    path = client.absolute_path(path)
    files = list_parser(files)

    def condition():
        listed_files = client.ls(path)
        for file in files:
            assert file in listed_files, "File {} not in listed files".format(file)

    assert_(client.perform, condition)


@wt(parsers.re('(?P<directory>.*) is empty for (?P<user>\w+) on (?P<client_node>.*)'))
def ls_empty(directory, user, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    dir_path = client.absolute_path(directory)

    def condition():
        assert len(client.ls(dir_path)) == 0

    assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) lists children of (?P<parent_dir>.*) and gets '
               'names in range \[(?P<lower>.*), (?P<upper>.*)\) on '
               '(?P<client_node>.*)'))
def ls_children(user, parent_dir, lower: int, upper: int, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    path = client.absolute_path(parent_dir)
    files_num = upper - lower

    def condition():
        listed_files = client.ls(path)

        assert len(listed_files) == files_num, "Listed {} files instead of expected {}".format(
            len(listed_files), files_num)
        for i in range(lower, upper):
            assert str(i) in listed_files, "File {} not in listed files".format(str(i))

    assert_(client.perform, condition)


def mv_base(user, file1, file2, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    src = client.absolute_path(file1)
    dest = client.absolute_path(file2)

    def condition():
        client.mv(src, dest)

    if should_fail:
        assert_expected_failure(condition)
    else:
        assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) renames (?P<file1>.*) to (?P<file2>.*)'
               ' on (?P<client_node>.*)'))
def rename(user, file1, file2, client_node, users):
    mv_base(user, file1, file2, client_node, users)


def rename_base(user, file1, file2, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    src = client.absolute_path(file1)
    dest = client.absolute_path(file2)

    def condition():
        client.osrename(src, dest)

    if should_fail:
        assert_expected_failure(condition)
    else:
        assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) fails to rename (?P<file1>.*) to '
               '(?P<file2>.*) on (?P<client_node>.*)'))
def rename_fail(user, file1, file2, client_node, users):
    rename_base(user, file1, file2, client_node, users, should_fail=True)


@wt(parsers.re('(?P<user>\w+) can\'t stat (?P<files>.*) in (?P<path>.*) on '
               '(?P<client_node>.*)'))
def stat_absent(user, path, files, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    path = client.absolute_path(path)
    files = list_parser(files)

    def condition():
        for f in files:
            p = os.path.join(path, f)
            try:
                client.stat(p)
                raise Exception(f'Failed: There is item {f}')
            except FileNotFoundError as exc_info:
                assert p in exc_info.filename

    assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) doesn\'t see (?P<files>.*) in (?P<path>.*) '
               'on (?P<client_node>.*)'))
def ls_absent(user, files, path, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    path = client.absolute_path(path)
    files = list_parser(files)

    def condition():
        time.sleep(1)
        listed_files = client.ls(path)
        for file in files:
            assert file not in listed_files, "File {} is in files list".format(file)

    assert_(client.perform, condition)


def shell_move_base(user, file1, file2, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    src = client.absolute_path(file1)
    dest = client.absolute_path(file2)
    cmd = 'mv {0} {1}'.format(src, dest)

    def condition():
        ret = client.run_cmd(cmd, error=True)
        if ret != 0:
            raise OSError("Command ended with exit code {}".format(ret))

    if should_fail:
        assert_expected_failure(condition)
    else:
        assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) fails to move (?P<file1>.*) to (?P<file2>.*) '
               'using shell command on (?P<client_node>.*)'))
def shell_move_fail(user, file1, file2, client_node, users):
    shell_move_base(user, file1, file2, client_node, users, should_fail=True)


def delete_file_base(user, files, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    files = list_parser(files)
    for file in files:
        path = client.absolute_path(file)

        def condition():
            client.rm(path)

        if should_fail:
            assert_expected_failure(condition)
        else:
            assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) deletes files (?P<files>.*) on '
               '(?P<client_node>.*)'))
def delete_file(user, files, client_node, users):
    delete_file_base(user, files, client_node, users)


@wt(parsers.re('(?P<user>\w+) fails to delete files (?P<files>.*) '
               'on (?P<client_node>.*)'))
def delete_file_fail(user, files, client_node, users):
    delete_file_base(user, files, client_node, users, should_fail=True)


@wt(parsers.re('size of (?P<user>\w+)\'s (?P<file>.*) is (?P<size>.*) bytes '
               'on (?P<client_node>.*)'))
def check_size(user, file, size, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)
    size = int(size)

    def condition():
        stat_result = client.stat(file_path)
        assert stat_result.st_size == size

    assert_(client.perform, condition)


@then(parsers.re('file type of (?P<user>\w+)\'s (?P<file>.*) is '
                 '(?P<file_type>.*) on (?P<client_node>.*)'))
def check_type(user, file, file_type, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    if file_type == 'regular':
        stat_method = 'S_ISREG'
    elif file_type == 'directory':
        stat_method = 'S_ISDIR'

    def condition():
        stat_result = client.stat(file_path)
        assert getattr(stat_lib, stat_method)(stat_result.st_mode)

    assert_(client.perform, condition)


@then(parsers.re('(?P<user>\w+) checks using shell stat if file type '
                 'of (?P<file>.*) is (?P<file_type>.*) on (?P<client_node>.*)'))
def shell_check_type(user, file, file_type, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    def condition():
        cmd = 'stat --format=%F {}'.format(file_path)
        stat_file_type = client.run_cmd(cmd, output=True)
        assert stat_file_type.strip() == file_type

    assert_(client.perform, condition)


@wt(parsers.re('mode of (?P<user>\w+)\'s (?P<file>.*) is (?P<mode>.*) on '
               '(?P<client_node>.*)'))
@repeat_failed(interval=1, timeout=30, exceptions=AssertionError)
def check_mode(user, file, mode, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)
    mode = int(mode, 8)

    def condition():
        stat_result = client.stat(file_path)
        assert stat_lib.S_IMODE(stat_result.st_mode) == mode

    assert_(client.perform, condition)


def change_mode_base(user, file, mode, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    mode = int(mode, 8)
    file_path = client.absolute_path(file)

    def condition():
        client.chmod(mode, file_path)

    assert_generic(client.perform, should_fail, condition)


@wt(parsers.re('(?P<user>\w+) changes (?P<file>.*) mode to (?P<mode>.*) on '
               '(?P<client_node>.*)'))
def change_mode(user, file, mode, client_node, users):
    change_mode_base(user, file, mode, client_node, users)


@wt(parsers.re('(?P<user>\w+) fails to change (?P<file>.*) mode to '
               '(?P<mode>.*) on (?P<client_node>.*)'))
def change_mode_fail(user, file, mode, client_node, users):
    change_mode_base(user, file, mode, client_node, users, should_fail=True)


@then(parsers.re('(?P<time1>.*) time of (?P<user>\w+)\'s (?P<file>.*) is '
                 '(?P<comparator>.*) to (?P<time2>.*) time on '
                 '(?P<client_node>.*)'))
@then(parsers.re('(?P<time1>.*) time of (?P<user>\w+)\'s (?P<file>.*) is '
                 '(?P<comparator>.*) than (?P<time2>.*) time on '
                 '(?P<client_node>.*)'))
def check_time(user, time1, time2, comparator, file, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    attr1 = time_attr(time1)
    attr2 = time_attr(time2)
    file_path = client.absolute_path(file)

    def condition():
        stat_result = client.stat(file_path)
        t1 = getattr(stat_result, attr1)
        t2 = getattr(stat_result, attr2)
        assert compare(t1, t2, comparator)

    assert_(client.perform, condition)


def check_files_time(user, time1, time2, comparator, file, file2,
                     client_node, users):
    user = users[user]
    client = user.clients[client_node]
    attr1 = time_attr(time1)
    attr2 = time_attr(time2)
    file_path = client.absolute_path(file)
    file2_path = client.absolute_path(file2)

    def condition():
        stat_result = client.stat(file_path)
        t1 = getattr(stat_result, attr1)
        stat_result2 = client.stat(file2_path)
        t2 = getattr(stat_result2, attr2)
        assert compare(t1, t2, comparator)

    assert_(client.perform, condition)


@then(parsers.re('(?P<time1>.*) time of (?P<user>\w+)\'s (?P<file1>.*) is '
                 '(?P<comparator>.*) to recorded one of (?P<file2>.*) on '
                 '(?P<client_node>.*)'))
@then(parsers.re('(?P<time1>.*) time of (?P<user>\w+)\'s (?P<file1>.*) is '
                 '(?P<comparator>.*) than recorded one of (?P<file2>.*) on '
                 '(?P<client_node>.*)'))
def cmp_time_to_previous(user, time1, comparator, file1, file2,
                         users, client_node):
    user = users[user]
    client = user.clients[client_node]
    attr = time_attr(time1)
    file_path = client.absolute_path(file1)
    recorded_stats = client.file_stats[client.absolute_path(file2)]

    def condition():
        stat_result = client.stat(file_path)
        t1 = getattr(stat_result, attr)
        t2 = getattr(recorded_stats, attr)
        assert compare(t1, t2, comparator)

    assert_(client.perform, condition)


def touch_file_base(user, files, client_node, users, should_fail=False):
    user = users[user]
    client = user.clients[client_node]
    files = list_parser(files)

    for file in files:
        file_path = client.absolute_path(file)

        def condition():
            try:
                client.touch(file_path)
            except OSError:
                return True if should_fail else False
            else:
                return False if should_fail else True

        assert_(client.perform, condition)


@when(parsers.re('(?P<user>\w+) updates (?P<files>.*) timestamps on'
                 ' (?P<client_node>.*)'))
def touch_file(user, files, client_node, users):
    touch_file_base(user, files, client_node, users)


@when(parsers.re('(?P<user>\w+) fails to update (?P<files>.*) timestamps '
                 'on (?P<client_node>.*)'))
def touch_file_fail(user, files, client_node, users):
    touch_file_base(user, files, client_node, users, should_fail=True)


@wt(parsers.re('(?P<user>\w+) sets extended attribute (?P<name>[.\w]+) '
               'with value (?P<value>.*) on (?P<file>\w+)'
               'on (?P<client_node>.*)'))
def set_xattr(user, file, name, value, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    def condition():
        if isinstance(value, str):
            value_bytes = value.encode('utf-8')
        else:
            value_bytes = value

        client.setxattr(file_path, name, value_bytes)

    assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) removes all extended attributes '
               'from (?P<file>\w+) on (?P<client_node>.*)'))
def remove_all_xattr(user, file, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    def condition():
        client.clear_xattr(file_path)

    assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) removes extended attribute (?P<name>[.\w]+) '
               'from (?P<file>\w+) on (?P<client_node>.*)'))
def remove_xattr(user, file, name, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    def condition():
        client.removexattr(file_path, name)

    assert_(client.perform, condition)


@then(parsers.re('(?P<user>\w+) checks if (?P<file>\w+) has extended '
                 'attribute (?P<name>[.\w]+) on (?P<client_node>.*)'))
def check_xattr_exists(user, file, name, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    def condition():
        xattrs = client.listxattr(file_path)
        assert name in xattrs

    assert_(client.perform, condition)


@then(parsers.re('(?P<user>\w+) checks if (?P<file>\w+) does not have '
                 'extended attribute (?P<name>[.\w]+) on (?P<client_node>.*)'))
def check_xattr_doesnt_exist(user, file, name, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    def condition():
        xattrs = client.listxattr(file_path)
        assert name not in xattrs

    assert_(client.perform, condition)


@then(parsers.re('(?P<user>\w+) checks if (?P<file>\w+) has extended '
                 'attribute (?P<name>[.\w]+) with string value '
                 '"(?P<value>.*)" on (?P<client_node>.*)'))
def check_string_xattr(user, file, name, value, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    def condition():
        xattr_value = client.getxattr(file_path, name)
        if isinstance(value, str):
            value_utf = value.encode('utf-8')
        else:
            value_utf = value

        assert xattr_value == value_utf

    assert_(client.perform, condition)


@then(parsers.re('(?P<user>\w+) checks if (?P<file>\w+) has extended '
                 'attribute (?P<name>[.\w]+) with numeric value (?P<value>.*) '
                 'on (?P<client_node>.*)'))
def check_numeric_xattr(user, file, name, value, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    def condition():
        xattr_value = client.getxattr(file_path, name)
        assert float(xattr_value) == float(value)

    assert_(client.perform, condition)


@then(parsers.re('(?P<user>\w+) checks if (?P<file>\w+) has extended '
                 'attribute (?P<name>[.\w]+) with JSON value "(?P<value>.*)" '
                 'on (?P<client_node>.*)'))
def check_json_xattr(user, file, name, value, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(file)

    def condition():
        xattr_value = client.getxattr(file_path, name)
        assert jsondiff.diff(json.loads(xattr_value), json.loads(value)) == {}

    assert_(client.perform, condition)


@wt(parsers.re('(?P<user>\w+) records (?P<files>.*) stats on (?P<client_node>.*)'))
def record_stats(user, files, client_node, users):
    user = users[user]
    client = user.clients[client_node]

    for file_ in list_parser(files):
        file_path = client.absolute_path(file_)
        client.file_stats[file_path] = client.stat(file_path)


def get_metadata(user, path, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(path)

    xattr_value = client.get_all_xattr(file_path)
    return xattr_value


@wt(parsers.re('(?P<user>\w+) sees that owner\'s UID and GID for (?P<path>.*) '
               'are (?P<res>equal|not equal) to (?P<uid>[\d]+) and '
               '(?P<gid>[\d]+) respectively on (?P<client_node>.*)'))
def assert_file_ownership(user, path, res, uid, gid, client_node, users):
    user = users[user]
    client = user.clients[client_node]
    file_path = client.absolute_path(path)
    uid = int(uid)
    gid = int(gid)

    def condition():
        stat_result = client.stat(file_path)
        if res == 'equal':
            wrong_id_fmt = ('Expected owner\'s {} of file {} to be {}, '
                            'but found {}')
            wrong_uid_msg = wrong_id_fmt.format('UID', path, uid,
                                                stat_result.st_uid)
            wrong_gid_msg = wrong_id_fmt.format('GID', path, gid,
                                                stat_result.st_gid)
            assert stat_result.st_uid == uid, wrong_uid_msg
            assert stat_result.st_gid == gid, wrong_gid_msg
        else:
            wrong_id_fmt = 'Expected owner\'s {} of file {} not to be {}'
            wrong_uid_msg = wrong_id_fmt.format('UID', path, uid)
            wrong_gid_msg = wrong_id_fmt.format('GID', path, gid)
            assert stat_result.st_uid != uid, wrong_uid_msg
            assert stat_result.st_gid != gid, wrong_gid_msg

    assert_(client.perform, condition)


@wt(parsers.re('there is file "(?P<path>.*)" in container "(?P<container>.*)" '
               'on provider "(?P<provider>.*)"'))
def assert_file_exists_on_storage(path, container, provider, hosts):
    pod_name = hosts[provider]['pod-name']
    filename = os.path.basename(path)
    dir_path = os.path.dirname(path)
    cmd = ['sh', '-c', 'ls {}'.format(dir_path)]
    ls_res = sp.check_output(cmd_exec(pod_name, cmd, container=container))
    listed_files = [file_name for file_name in ls_res.split('\n') if file_name]
    assert filename in listed_files, ('File {} does not exists in storage {}'
                                      .format(filename, container))


@wt(parsers.re('file "(?P<path>.*)" in container "(?P<container>.*)" '
               'on provider "(?P<provider>.*)" has owner\'s UID and GID '
               'equal to (?P<uid>[\d]+) and (?P<gid>[\d]+) respectively'))
def assert_file_stats_on_storage(path, container, provider, hosts, uid, gid):
    pod_name = hosts[provider]['pod-name']
    cmd = ['sh', '-c', 'stat {}'.format(path)]
    file_stat = sp.check_output(cmd_exec(pod_name, cmd, container=container))
    stat_uid = re.search(r'Uid:\s*\((\d+).*\)', file_stat).group(1)
    stat_gid = re.search(r'Gid:\s*\((\d+).*\)', file_stat).group(1)
    assert uid == stat_uid, ('Expected owner\'s UID of file {} to be {}, '
                             'but found {}'.format(path, uid, stat_uid))
    assert gid == stat_gid, ('Expected owner\'s GID of file {} to be {}, '
                             'but found {}'.format(path, gid, stat_gid))
