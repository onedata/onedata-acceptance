"""Module implements pytest-bdd steps for operations on regular files."""

__author__ = "Jakub Kudzia, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.utils.bdd_utils import parsers, then, when, wt

from . import multi_reg_file_steps


@wt(parsers.re(r'(?P<user>\w+) writes "(?P<text>.*)" to (?P<file>.*)'))
def write_text(user, text, file, users):
    multi_reg_file_steps.write_text(user, text, file, "client1", users)


@when(
    parsers.re(
        r"(?P<user>\w+) writes (?P<megabytes>.*) MB of random "
        "characters to (?P<file>.*) and saves MD5"
    )
)
def write_rand_text(user, megabytes, file, users, context):
    multi_reg_file_steps.write_rand_text(
        user, megabytes, file, "client1", users, context
    )


@wt(parsers.re(r'(?P<user>\w+) fails to write "(?P<text>.*)" to (?P<file>.*)'))
def write_text_fail(user, text, file, users):
    multi_reg_file_steps.write_text_fail(user, text, file, "client1", users)


@wt(parsers.re(r'(?P<user>\w+) reads "(?P<text>.*)" from file (?P<file>.*)'))
def read(user, text, file, users):
    multi_reg_file_steps.read_text(user, text, file, "client1", users)


@wt(parsers.re(r'(?P<user>\w+) appends "(?P<text>.*)" to (?P<file>.*)'))
def append(user, text, file, users):
    multi_reg_file_steps.append(user, text, file, "client1", users)


@when(
    parsers.re(
        r'(?P<user>\w+) replaces "(?P<text1>.*)" with "(?P<text2>.*)" '
        "in (?P<file>.*)"
    )
)
def replace(user, text1, text2, file, users):
    multi_reg_file_steps.replace(user, text1, text2, file, "client1", users)


@when(parsers.re(r"(?P<user>\w+) copies regular file (?P<file>.*) to (?P<path>.*)"))
def copy_reg_file(user, file, path, users):
    multi_reg_file_steps.copy_reg_file(user, file, path, "client1", users)


@then(parsers.re(r"(?P<user>\w+) checks MD5 of (?P<file>.*)"))
def check_md5(user, file, users, context):
    multi_reg_file_steps.check_md5(user, file, "client1", users, context)


@when(parsers.re(r"(?P<user>\w+) changes (?P<file>.*) size to (?P<new_size>.*) bytes"))
def do_truncate(user, file, new_size, users):
    multi_reg_file_steps.do_truncate(user, file, new_size, "client1", users)


@wt(
    parsers.re(
        r"(?P<user>\w+) fails to change (?P<file>.*) size to (?P<new_size>.*) bytes"
    )
)
def do_truncate_fail(user, file, new_size, users):
    multi_reg_file_steps.do_truncate_fail(user, file, new_size, "client1", users)


@wt(parsers.re(r"(?P<user>\w+) executes (?P<file>.*)"))
def execute_script(user, file, users):
    multi_reg_file_steps.execute_script(user, file, "client1", users)


@wt(parsers.re(r"(?P<user>\w+) fails to execute (?P<file>.*)"))
def execute_script_fail(user, file, users):
    multi_reg_file_steps.execute_script_fail(user, file, "client1", users)
