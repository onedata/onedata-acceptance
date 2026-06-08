"""Module implements pytest-bdd steps for operations on regular files."""

__author__ = "Jakub Kudzia, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Any

from tests.utils.bdd_utils import parsers, then, when, wt

from . import multi_reg_file_steps


@wt(parsers.re(r'(?P<user>\w+) writes "(?P<text>.*)" to (?P<file>.*)'))
def write_text(user: Any, text: Any, file: Any, users: Any) -> Any:
    multi_reg_file_steps.write_text(user, text, file, "client1", users)


@when(
    parsers.re(
        r"(?P<user>\w+) writes (?P<megabytes>.*) MB of random "
        "characters to (?P<file>.*) and saves MD5"
    )
)
def write_rand_text(
    user: Any, megabytes: Any, file: Any, users: Any, context: Any
) -> Any:
    multi_reg_file_steps.write_rand_text(
        user, megabytes, file, "client1", users, context
    )


@wt(parsers.re(r'(?P<user>\w+) fails to write "(?P<text>.*)" to (?P<file>.*)'))
def write_text_fail(user: Any, text: Any, file: Any, users: Any) -> Any:
    multi_reg_file_steps.write_text_fail(user, text, file, "client1", users)


@wt(parsers.re(r'(?P<user>\w+) reads "(?P<text>.*)" from file (?P<file>.*)'))
def read(user: Any, text: Any, file: Any, users: Any) -> Any:
    multi_reg_file_steps.read_text(user, text, file, "client1", users)


@wt(parsers.re(r'(?P<user>\w+) appends "(?P<text>.*)" to (?P<file>.*)'))
def append(user: Any, text: Any, file: Any, users: Any) -> Any:
    multi_reg_file_steps.append(user, text, file, "client1", users)


@when(
    parsers.re(
        r'(?P<user>\w+) replaces "(?P<text1>.*)" with "(?P<text2>.*)" '
        "in (?P<file>.*)"
    )
)
def replace(user: Any, text1: Any, text2: Any, file: Any, users: Any) -> Any:
    multi_reg_file_steps.replace(user, text1, text2, file, "client1", users)


@when(parsers.re(r"(?P<user>\w+) copies regular file (?P<file>.*) to (?P<path>.*)"))
def copy_reg_file(user: Any, file: Any, path: Any, users: Any) -> Any:
    multi_reg_file_steps.copy_reg_file(user, file, path, "client1", users)


@then(parsers.re(r"(?P<user>\w+) checks MD5 of (?P<file>.*)"))
def check_md5(user: Any, file: Any, users: Any, context: Any) -> Any:
    multi_reg_file_steps.check_md5(user, file, "client1", users, context)


@when(parsers.re(r"(?P<user>\w+) changes (?P<file>.*) size to (?P<new_size>.*) bytes"))
def do_truncate(user: Any, file: Any, new_size: Any, users: Any) -> Any:
    multi_reg_file_steps.do_truncate(user, file, new_size, "client1", users)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to change (?P<file>.*) size to (?P<new_size>.*) bytes"
    )
)
def do_truncate_fail(user: Any, file: Any, new_size: Any, users: Any) -> Any:
    multi_reg_file_steps.do_truncate_fail(user, file, new_size, "client1", users)


@wt(parsers.re(r"(?P<user>\w+) executes (?P<file>.*)"))
def execute_script(user: Any, file: Any, users: Any) -> Any:
    multi_reg_file_steps.execute_script(user, file, "client1", users)


@wt(parsers.re(r"(?P<user>\w+) fails to execute (?P<file>.*)"))
def execute_script_fail(user: Any, file: Any, users: Any) -> Any:
    multi_reg_file_steps.execute_script_fail(user, file, "client1", users)
