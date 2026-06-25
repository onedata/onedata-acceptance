"""Module implements common steps for operation on files (both regular files
and directories)in multi-client environment.
"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"
# pylint: disable=cell-var-from-loop, deprecated-method


import json
import os
import random
import re
import stat as stat_lib
import string
import subprocess as sp
import time
from collections.abc import Mapping

import jsondiff
import pytest

from tests.oneclient.steps.multi_dir_steps import create
from tests.types import Hosts, Users
from tests.utils.acceptance_utils import compare, list_parser, make_arg_list, time_attr
from tests.utils.bdd_utils import parsers, then, when, wt
from tests.utils.client_utils import Client
from tests.utils.onenv_utils import cmd_exec
from tests.utils.utils import (
    assert_,
    assert_expected_failure,
    assert_generic,
    repeat_failed,
)

HARDLINKS_DIR = ".hardlinks"
SYMLINKS_DIR = ".symlinks"


def create_base(
    user: str,
    files: str,
    client_node: str,
    users: Users,
    request: pytest.FixtureRequest,
    should_fail: bool = False,
) -> None:
    file_names = list_parser(files)
    user_ = users[user]
    client = user_.clients[client_node]
    mode = request.config.getoption("file_mode")

    for file_name in file_names:
        # path for original file in hardlink/symlink mode
        # space_name/(.hardlinks or .symlinks)/(random string)

        path = client.absolute_path(file_name)
        if mode == "regular":

            def condition() -> None:
                client.create_file(path)

        elif mode == "hardlink":
            target_file_path = create_target_file(
                user, client, client_node, users, file_name, HARDLINKS_DIR
            )

            def condition() -> None:
                client.create_file(target_file_path)
                client.create_hardlink(target_file_path, path)

        elif mode == "symlink":
            target_file_path = create_target_file(
                user, client, client_node, users, file_name, SYMLINKS_DIR
            )

            def condition() -> None:
                client.create_file(target_file_path)
                client.create_symlink(target_file_path, path)

        else:
            raise AssertionError

        try:
            assert_generic(client.perform, should_fail, condition)
        except AssertionError as e:
            print(e)


def create_hardlink(
    user: str, file_path: str, hardlink_path: str, client_node: str, users: Users
) -> None:
    client = users[user].clients[client_node]
    client.create_hardlink(
        client.absolute_path(file_path), client.absolute_path(hardlink_path)
    )


def create_symlink(
    user: str, file_path: str, symlink_path: str, client_node: str, users: Users
) -> None:
    user_ = users[user]
    client = user_.clients[client_node]
    client.create_symlink(
        client.absolute_path(file_path), client.absolute_path(symlink_path)
    )


def create_target_file(
    user: str,
    client: Client,
    client_node: str,
    users: Users,
    file_name: str,
    dir_name: str,
) -> str:
    space = file_name.split("/")[0]
    create(user, f"[{space}/{dir_name}]", client_node, users, exists_ok=True)
    file_name_hash = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(16)
    )
    target_file_path = os.path.join(space, dir_name, file_name_hash)
    target_file_path = client.absolute_path(target_file_path)
    return target_file_path


@wt(
    parsers.re(
        r"(?P<user>\w+) creates regular files (?P<files>.*) on (?P<client_node>.*)"
    )
)
def create_reg_file(
    user: str,
    files: str,
    client_node: str,
    users: Users,
    request: pytest.FixtureRequest,
) -> None:
    create_base(user, files, client_node, users, request)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to create regular files (?P<files>.*) "
        "on (?P<client_node>.*)"
    )
)
def create_reg_file_fail(
    user: str,
    files: str,
    client_node: str,
    users: Users,
    request: pytest.FixtureRequest,
) -> None:
    create_base(user, files, client_node, users, request, should_fail=True)


@wt(
    parsers.re(
        r"(?P<user>\w+) creates child files of (?P<parent_dir>.*) "
        r"with names in range \[(?P<lower>.*), (?P<upper>.*)\) on "
        "(?P<client_node>.*)"
    )
)
def create_many(
    user: str,
    lower: str,
    upper: str,
    parent_dir: str,
    client_node: str,
    users: Users,
    request: pytest.FixtureRequest,
) -> None:
    for i in range(int(lower), int(upper)):
        new_file = os.path.join(parent_dir, str(i))
        create_reg_file(user, make_arg_list(new_file), client_node, users, request)


@wt(
    parsers.re(
        r"(?P<user>\w+) can stat (?P<files>.*) in (?P<path>.*)"
        " on (?P<client_node>.*)"
    )
)
def stat_present(
    user: str, path: str, files: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    path = client.absolute_path(path)
    file_names = list_parser(files)

    def condition() -> None:
        for f in file_names:
            client.stat(os.path.join(path, f))

    assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) sees (?P<files>.*) in (?P<path>.*) on (?P<client_node>.*)"
    )
)
def ls_present(
    user: str, files: str, path: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    path = client.absolute_path(path)
    file_names = list_parser(files)

    def condition() -> None:
        listed_files = client.ls(path)
        for file in file_names:
            assert file in listed_files, f"File {file} not in listed files"

    assert_(client.perform, condition)


def ls_present_spaces(
    user: str, spaces: list[str], client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    path = client.absolute_path("")

    def condition() -> None:
        listed_spaces = client.ls(path)
        for space in spaces:
            assert (
                space in listed_spaces
            ), f"Space {space} not in listed spaces, listed spaces: {listed_spaces}"

    assert_(client.perform, condition)


@wt(parsers.re(r"(?P<directory>.*) is empty for (?P<user>\w+) on (?P<client_node>.*)"))
def ls_empty(directory: str, user: str, client_node: str, users: Users) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    dir_path = client.absolute_path(directory)

    def condition() -> None:
        assert len(client.ls(dir_path)) == 0

    assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) lists children of (?P<parent_dir>.*) and gets "
        r"names in range \[(?P<lower>.*), (?P<upper>.*)\) on "
        "(?P<client_node>.*)"
    )
)
def ls_children(
    user: str, parent_dir: str, lower: str, upper: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    path = client.absolute_path(parent_dir)
    lower_int = int(lower)
    upper_int = int(upper)
    files_num = upper_int - lower_int

    def condition() -> None:
        listed_files = client.ls(path)

        assert (
            len(listed_files) == files_num
        ), f"Listed {len(listed_files)} files instead of expected {files_num}"
        for i in range(lower_int, upper_int):
            assert str(i) in listed_files, f"File {i} not in listed files"

    assert_(client.perform, condition)


def mv_base(
    user: str,
    file1: str,
    file2: str,
    client_node: str,
    users: Users,
    should_fail: bool = False,
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    src = client.absolute_path(file1)
    dest = client.absolute_path(file2)

    def condition() -> None:
        client.mv(src, dest)

    if should_fail:
        assert_expected_failure(condition)
    else:
        assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) renames (?P<file1>.*) to (?P<file2>.*)"
        " on (?P<client_node>.*)"
    )
)
def rename(user: str, file1: str, file2: str, client_node: str, users: Users) -> None:
    mv_base(user, file1, file2, client_node, users)


def rename_base(
    user: str,
    file1: str,
    file2: str,
    client_node: str,
    users: Users,
    should_fail: bool = False,
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    src = client.absolute_path(file1)
    dest = client.absolute_path(file2)

    def condition() -> None:
        client.osrename(src, dest)

    if should_fail:
        assert_expected_failure(condition)
    else:
        assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to rename (?P<file1>.*) to "
        "(?P<file2>.*) on (?P<client_node>.*)"
    )
)
def rename_fail(
    user: str, file1: str, file2: str, client_node: str, users: Users
) -> None:
    rename_base(user, file1, file2, client_node, users, should_fail=True)


@wt(
    parsers.re(
        r"(?P<user>\w+) can't stat (?P<files>.*) in (?P<path>.*) on "
        "(?P<client_node>.*)"
    )
)
def stat_absent(
    user: str, path: str, files: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    path = client.absolute_path(path)
    file_names = list_parser(files)

    def condition() -> None:
        for f in file_names:
            p = os.path.join(path, f)
            try:
                client.stat(p)
                raise AssertionError(f"Failed: There is item {f}")
            except FileNotFoundError as exc_info:
                assert p in exc_info.filename

    assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) doesn't see (?P<files>.*) in (?P<path>.*) "
        "on (?P<client_node>.*)"
    )
)
def ls_absent(user: str, files: str, path: str, client_node: str, users: Users) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    path = client.absolute_path(path)
    file_names = list_parser(files)

    def condition() -> None:
        time.sleep(1)
        listed_files = client.ls(path)
        for file in file_names:
            assert file not in listed_files, f"File {file} is in files list"

    assert_(client.perform, condition)


def shell_move_base(
    user: str,
    file1: str,
    file2: str,
    client_node: str,
    users: Users,
    should_fail: bool = False,
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    src = client.absolute_path(file1)
    dest = client.absolute_path(file2)
    cmd = f"mv {src} {dest}"

    def condition() -> None:
        ret = client.run_cmd(cmd, error=True)
        if ret != 0:
            raise OSError(f"Command ended with exit code {ret}")

    if should_fail:
        assert_expected_failure(condition)
    else:
        assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to move (?P<file1>.*) to (?P<file2>.*) "
        "using shell command on (?P<client_node>.*)"
    )
)
def shell_move_fail(
    user: str, file1: str, file2: str, client_node: str, users: Users
) -> None:
    shell_move_base(user, file1, file2, client_node, users, should_fail=True)


def delete_file_base(
    user: str, files: str, client_node: str, users: Users, should_fail: bool = False
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_names = list_parser(files)
    for file in file_names:
        path = client.absolute_path(file)

        def condition() -> None:
            client.rm(path)

        if should_fail:
            assert_expected_failure(condition)
        else:
            assert_(client.perform, condition)


@wt(parsers.re(r"(?P<user>\w+) deletes files (?P<files>.*) on (?P<client_node>.*)"))
def delete_file(user: str, files: str, client_node: str, users: Users) -> None:
    delete_file_base(user, files, client_node, users)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to delete files (?P<files>.*) on (?P<client_node>.*)"
    )
)
def delete_file_fail(user: str, files: str, client_node: str, users: Users) -> None:
    delete_file_base(user, files, client_node, users, should_fail=True)


@wt(
    parsers.re(
        r"size of (?P<user>\w+)'s (?P<file>.*) is (?P<size>.*) bytes "
        "on (?P<client_node>.*)"
    )
)
def check_size(
    user: str, file: str, size: str | int, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)
    expected_size = int(size)

    def condition() -> None:
        stat_result = client.stat(file_path)
        assert stat_result.st_size == expected_size

    assert_(client.perform, condition)


def check_type_impl(
    user: str,
    file: str,
    file_type: str,
    client_node: str,
    users: Users,
    follow_symlinks: bool = True,
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)

    if file_type == "regular":
        stat_method = "S_ISREG"
    elif file_type == "directory":
        stat_method = "S_ISDIR"
    elif file_type == "symlink":
        stat_method = "S_ISLNK"
    else:
        raise ValueError(f"unknown file type {file_type}")

    def condition() -> None:
        if follow_symlinks:
            stat_result = client.stat(file_path)
        else:
            stat_result = client.lstat(file_path)
        assert getattr(stat_lib, stat_method)(stat_result.st_mode)

    assert_(client.perform, condition)


@then(
    parsers.re(
        r"file type of (?P<user>\w+)'s (?P<file>.*) is "
        r"(?P<file_type>.*) on (?P<client_node>.*)"
    )
)
def check_type(
    user: str,
    file: str,
    file_type: str,
    client_node: str,
    users: Users,
    request: pytest.FixtureRequest,
) -> None:
    check_type_impl(
        user,
        file,
        file_type,
        client_node,
        users,
        request.config.getoption("file_mode") == "symlink",
    )


@then(
    parsers.re(
        r"(?P<user>\w+) checks using shell stat if file type "
        "of (?P<file>.*) is (?P<file_type>.*) on (?P<client_node>.*)"
    )
)
def shell_check_type(
    user: str,
    file: str,
    file_type: str,
    client_node: str,
    users: Users,
    request: pytest.FixtureRequest,
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)
    mode = request.config.getoption("file_mode")

    def condition() -> None:
        follow_links = "-L " if mode == "symlink" else ""
        cmd = f"stat --format=%F {follow_links}{file_path}"
        stat_file_type = client.run_cmd(cmd, output=True)
        assert isinstance(stat_file_type, str)
        assert stat_file_type.strip() == file_type

    assert_(client.perform, condition)


@wt(
    parsers.re(
        r"mode of (?P<user>\w+)'s (?P<file>.*) is (?P<mode>.*) on "
        "(?P<client_node>.*)"
    )
)
@repeat_failed(interval=1, timeout=30, exceptions=AssertionError)
def check_mode(user: str, file: str, mode: str, client_node: str, users: Users) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)
    expected_mode = int(mode, 8)

    def condition() -> None:
        stat_result = client.stat(file_path)
        assert stat_lib.S_IMODE(stat_result.st_mode) == expected_mode

    assert_(client.perform, condition)


def change_mode_base(
    user: str,
    file: str,
    mode: str,
    client_node: str,
    users: Users,
    should_fail: bool = False,
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    parsed_mode = int(mode, 8)
    file_path = client.absolute_path(file)

    def condition() -> None:
        client.chmod(parsed_mode, file_path)

    assert_generic(client.perform, should_fail, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) changes (?P<file>.*) mode to (?P<mode>.*) on "
        "(?P<client_node>.*)"
    )
)
def change_mode(
    user: str, file: str, mode: str, client_node: str, users: Users
) -> None:
    change_mode_base(user, file, mode, client_node, users)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to change (?P<file>.*) mode to "
        "(?P<mode>.*) on (?P<client_node>.*)"
    )
)
def change_mode_fail(
    user: str, file: str, mode: str, client_node: str, users: Users
) -> None:
    change_mode_base(user, file, mode, client_node, users, should_fail=True)


@then(
    parsers.re(
        r"(?P<time1>.*) time of (?P<user>\w+)'s (?P<file>.*) is "
        "(?P<comparator>.*) to (?P<time2>.*) time on "
        "(?P<client_node>.*)"
    )
)
@then(
    parsers.re(
        r"(?P<time1>.*) time of (?P<user>\w+)'s (?P<file>.*) is "
        "(?P<comparator>.*) than (?P<time2>.*) time on "
        "(?P<client_node>.*)"
    )
)
def check_time(
    user: str,
    time1: str,
    time2: str,
    comparator: str,
    file: str,
    client_node: str,
    users: Users,
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    attr1 = time_attr(time1)
    attr2 = time_attr(time2)
    file_path = client.absolute_path(file)

    def condition() -> None:
        stat_result = client.stat(file_path)
        t1 = getattr(stat_result, attr1)
        t2 = getattr(stat_result, attr2)

        err_msg = (
            f"Time comparison failed. \nTime1: {time1} = {t1} \n"
            f"Time2: {time2} = {t2} \nComparator: {comparator}"
        )

        assert compare(t1, t2, comparator), err_msg

    assert_(client.perform, condition)


def check_files_time(
    user: str,
    time1: str,
    time2: str,
    comparator: str,
    file: str,
    file2: str,
    client_node: str,
    users: Users,
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    attr1 = time_attr(time1)
    attr2 = time_attr(time2)
    file_path = client.absolute_path(file)
    file2_path = client.absolute_path(file2)

    def condition() -> None:
        stat_result = client.stat(file_path)
        t1 = getattr(stat_result, attr1)
        stat_result2 = client.stat(file2_path)
        t2 = getattr(stat_result2, attr2)
        assert compare(t1, t2, comparator)

    assert_(client.perform, condition)


@then(
    parsers.re(
        r"(?P<time1>.*) time of (?P<user>\w+)'s (?P<file1>.*) is "
        "(?P<comparator>.*) to recorded one of (?P<file2>.*) on "
        "(?P<client_node>.*)"
    )
)
@then(
    parsers.re(
        r"(?P<time1>.*) time of (?P<user>\w+)'s (?P<file1>.*) is "
        "(?P<comparator>.*) than recorded one of (?P<file2>.*) on "
        "(?P<client_node>.*)"
    )
)
def cmp_time_to_previous(
    user: str,
    time1: str,
    comparator: str,
    file1: str,
    file2: str,
    users: Users,
    client_node: str,
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    attr = time_attr(time1)
    file_path = client.absolute_path(file1)
    recorded_stats = client.file_stats[client.absolute_path(file2)]

    def condition() -> None:
        stat_result = client.stat(file_path)
        t1 = getattr(stat_result, attr)
        t2 = getattr(recorded_stats, attr)
        assert compare(t1, t2, comparator)

    assert_(client.perform, condition)


def touch_file_base(
    user: str, files: str, client_node: str, users: Users, should_fail: bool = False
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_names = list_parser(files)

    for file in file_names:
        file_path = client.absolute_path(file)

        def condition() -> bool:
            try:
                client.touch(file_path)
            except OSError:
                return bool(should_fail)
            return not bool(should_fail)

        assert_(client.perform, condition)


@when(
    parsers.re(r"(?P<user>\w+) updates (?P<files>.*) timestamps on (?P<client_node>.*)")
)
def touch_file(user: str, files: str, client_node: str, users: Users) -> None:
    touch_file_base(user, files, client_node, users)


@when(
    parsers.re(
        r"(?P<user>\w+) fails to update (?P<files>.*) timestamps "
        "on (?P<client_node>.*)"
    )
)
def touch_file_fail(user: str, files: str, client_node: str, users: Users) -> None:
    touch_file_base(user, files, client_node, users, should_fail=True)


@wt(
    parsers.re(
        r"(?P<user>\w+) sets extended attribute (?P<name>[.\w]+) "
        r"with value (?P<value>.*) on (?P<file>\w+)"
        "on (?P<client_node>.*)"
    )
)
def set_xattr(
    user: str, file: str, name: str, value: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)

    def condition() -> None:
        if isinstance(value, str):
            value_bytes = value.encode("utf-8")
        else:
            value_bytes = value

        client.setxattr(file_path, name, value_bytes)

    assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) removes all extended attributes "
        r"from (?P<file>\w+) on (?P<client_node>.*)"
    )
)
def remove_all_xattr(user: str, file: str, client_node: str, users: Users) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)

    def condition() -> None:
        client.clear_xattr(file_path)

    assert_(client.perform, condition)


@wt(
    parsers.re(
        r"(?P<user>\w+) removes extended attribute (?P<name>[.\w]+) "
        r"from (?P<file>\w+) on (?P<client_node>.*)"
    )
)
def remove_xattr(
    user: str, file: str, name: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)

    def condition() -> None:
        client.removexattr(file_path, name)

    assert_(client.perform, condition)


@then(
    parsers.re(
        r"(?P<user>\w+) checks if (?P<file>\w+) has extended "
        r"attribute (?P<name>[.\w]+) on (?P<client_node>.*)"
    )
)
def check_xattr_exists(
    user: str, file: str, name: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)

    def condition() -> None:
        xattrs = client.listxattr(file_path)
        assert name in xattrs

    assert_(client.perform, condition)


@then(
    parsers.re(
        r"(?P<user>\w+) checks if (?P<file>\w+) does not have "
        r"extended attribute (?P<name>[.\w]+) on (?P<client_node>.*)"
    )
)
def check_xattr_doesnt_exist(
    user: str, file: str, name: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)

    def condition() -> None:
        xattrs = client.listxattr(file_path)
        assert name not in xattrs

    assert_(client.perform, condition)


@then(
    parsers.re(
        r"(?P<user>\w+) checks if (?P<file>\w+) has extended "
        r"attribute (?P<name>[.\w]+) with string value "
        '"(?P<value>.*)" on (?P<client_node>.*)'
    )
)
def check_string_xattr(
    user: str, file: str, name: str, value: str | bytes, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)

    def condition() -> None:
        xattr_value: bytes = client.getxattr(file_path, name)
        if isinstance(value, str):
            value_utf = value.encode("utf-8")
        else:
            value_utf = value
        assert xattr_value == value_utf

    assert_(client.perform, condition)


@then(
    parsers.re(
        r"(?P<user>\w+) checks if (?P<file>\w+) has extended "
        r"attribute (?P<name>[.\w]+) with numeric value (?P<value>.*) "
        "on (?P<client_node>.*)"
    )
)
def check_numeric_xattr(
    user: str, file: str, name: str, value: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)

    def condition() -> None:
        xattr_value = client.getxattr(file_path, name)
        assert float(xattr_value) == float(value)

    assert_(client.perform, condition)


@then(
    parsers.re(
        r"(?P<user>\w+) checks if (?P<file>\w+) has extended "
        r'attribute (?P<name>[.\w]+) with JSON value "(?P<value>.*)" '
        "on (?P<client_node>.*)"
    )
)
def check_json_xattr(
    user: str, file: str, name: str, value: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(file)

    def condition() -> None:
        xattr_value = client.getxattr(file_path, name)
        assert jsondiff.diff(json.loads(xattr_value), json.loads(value)) == {}

    assert_(client.perform, condition)


@wt(parsers.re(r"(?P<user>\w+) records (?P<files>.*) stats on (?P<client_node>.*)"))
def record_stats(user: str, files: str, client_node: str, users: Users) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]

    for file_ in list_parser(files):
        file_path = client.absolute_path(file_)
        client.file_stats[file_path] = client.stat(file_path)


def get_metadata(
    user: str, path: str, client_node: str, users: Users
) -> Mapping[str, str]:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(path)

    xattr_value = client.get_all_xattr(file_path)
    return xattr_value


@wt(
    parsers.re(
        r"(?P<user>\w+) sees that owner's UID and GID for (?P<path>.*) "
        r"are (?P<res>equal|not equal) to (?P<uid>[\d]+) and "
        r"(?P<gid>[\d]+) respectively on (?P<client_node>.*)"
    )
)
def assert_file_ownership(
    user: str, path: str, res: str, uid: str, gid: str, client_node: str, users: Users
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    file_path = client.absolute_path(path)
    expected_uid = int(uid)
    expected_gid = int(gid)

    def condition() -> None:
        stat_result = client.stat(file_path)
        if res == "equal":
            wrong_id_fmt = "Expected owner's {} of file {} to be {}, but found {}"
            wrong_uid_msg = wrong_id_fmt.format(
                "UID", path, expected_uid, stat_result.st_uid
            )
            wrong_gid_msg = wrong_id_fmt.format(
                "GID", path, expected_gid, stat_result.st_gid
            )
            assert stat_result.st_uid == expected_uid, wrong_uid_msg
            assert stat_result.st_gid == expected_gid, wrong_gid_msg
        else:
            wrong_id_fmt = "Expected owner's {} of file {} not to be {}"
            wrong_uid_msg = wrong_id_fmt.format("UID", path, expected_uid)
            wrong_gid_msg = wrong_id_fmt.format("GID", path, expected_gid)
            assert stat_result.st_uid != expected_uid, wrong_uid_msg
            assert stat_result.st_gid != expected_gid, wrong_gid_msg

    assert_(client.perform, condition)


@wt(
    parsers.re(
        'there is file "(?P<path>.*)" in container "(?P<container>.*)" '
        'on provider "(?P<provider>.*)"'
    )
)
def assert_file_exists_on_storage(
    path: str, container: str, provider: str, hosts: Hosts
) -> None:
    pod_name = hosts[provider]["pod_name"]
    filename = os.path.basename(path)
    dir_path = os.path.dirname(path)
    cmd = ["sh", "-c", f"ls {dir_path}"]
    ls_res_bytes = sp.check_output(cmd_exec(pod_name, cmd, container=container))
    ls_res = ls_res_bytes.decode("utf-8")
    listed_files = [file_name for file_name in ls_res.split("\n") if file_name]
    assert (
        filename in listed_files
    ), f"File {filename} does not exists in storage {container}"


@wt(
    parsers.re(
        'file "(?P<path>.*)" in container "(?P<container>.*)" '
        'on provider "(?P<provider>.*)" has owner\'s UID and GID '
        r"equal to (?P<uid>[\d]+) and (?P<gid>[\d]+) respectively"
    )
)
def assert_file_stats_on_storage(
    path: str, container: str, provider: str, hosts: Hosts, uid: str, gid: str
) -> None:
    pod_name = hosts[provider]["pod_name"]
    cmd = ["sh", "-c", f"stat {path}"]
    file_stat = sp.check_output(cmd_exec(pod_name, cmd, container=container))
    file_stat_str = file_stat.decode("utf-8")

    stat_uid_match = re.search(r"Uid:\s*\((\d+).*\)", file_stat_str)
    stat_gid_match = re.search(r"Gid:\s*\((\d+).*\)", file_stat_str)

    assert (
        stat_uid_match is not None
    ), f"Cannot parse UID from stat output: {file_stat_str}"
    assert (
        stat_gid_match is not None
    ), f"Cannot parse GID from stat output: {file_stat_str}"

    stat_uid = stat_uid_match.group(1)
    stat_gid = stat_gid_match.group(1)
    assert (
        uid == stat_uid
    ), f"Expected owner's UID of file {path} to be {uid}, but found {stat_uid}"
    assert (
        gid == stat_gid
    ), f"Expected owner's GID of file {path} to be {gid}, but found {stat_gid}"


def try_to_create_file_in_root_dir(
    user: str, client_node: str, users: Users, file_name: str
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    client.create_file(os.path.join(client.get_mount_path(), file_name))


def create_file_in_dir_by_id(
    user: str, client_node: str, users: Users, file_id: str, file_name: str
) -> None:
    user_obj = users[user]
    client = user_obj.clients[client_node]
    client.create_file(
        f"{client.get_mount_path()}/.__onedata__file_id__{file_id}/{file_name}"
    )


def assert_symlink_of_file(
    user: str,
    client_node: str,
    users: Users,
    symlink_path: str,
    file_path: str,
    request: pytest.FixtureRequest,
) -> None:

    user_name = user
    user_obj = users[user_name]
    client = user_obj.clients[client_node]
    symlink_path = client.absolute_path(symlink_path)
    file_path = client.absolute_path(file_path)

    check_type(user_name, symlink_path, "symlink", client_node, users, request)

    real_path = client.realpath(symlink_path)
    # realpath eliminates every symbolic link encountered in path,
    # however if there are multiple symlinks this function can
    # give an error

    assert real_path == file_path, (
        f"resolved symlink real path: {real_path} is different than file real path:"
        f" {file_path}"
    )


def assert_hardlink_between_files(
    user: str,
    client_node: str,
    users: Users,
    file_path1: str,
    file_path2: str,
    request: pytest.FixtureRequest,
) -> None:
    user_name = user
    user_obj = users[user_name]
    client = user_obj.clients[client_node]
    file1 = client.absolute_path(file_path1)
    file2 = client.absolute_path(file_path2)

    # hardlink and original file must be regular files
    check_type(user_name, file1, "regular", client_node, users, request)
    check_type(user_name, file2, "regular", client_node, users, request)

    # Two files are hardlinked if they point to the same node in the same
    # file system
    assert client.samefile(file1, file2), (
        f"files {file1} and {file2} do not point to the same node in the same file"
        " system"
    )
