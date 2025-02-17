"""This module implements some common basic functions and functionality for
acceptance tests of onedata.
"""

__author__ = "Jakub Kudzia, Piotr Ociepka, Michal Stanisz"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import subprocess
import time

from tests.utils.bdd_utils import parsers, wt

TIME_ATTR_MAPPING = {
    "access": "atime",
    "modification": "mtime",
    "status-change": "ctime",
}


def list_parser(arg):
    return [el.strip() for el in arg.strip("[]").split(",") if el != ""]


def make_arg_list(arg):
    return "[" + arg + "]"


def execute_command(cmd, error=None, should_fail=False):
    with subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as process:
        output, err = process.communicate()
        proc_returncode = process.returncode
    if (proc_returncode != 0) ^ should_fail:
        raise RuntimeError(
            f"{error}: {err}; {output}"
            if error
            else (
                f"Command did not fail: {' '.join(cmd)}, Err: {err}, Output: {output}"
                if should_fail
                else f'Error when executing command "{' '.join(cmd)}": {err}; {output}'
            )
        )
    return output


@wt(
    parsers.re(
        "if (?P<client>.+?) is web GUI, (?P<user>.+?) is idle for "
        r"(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds?"
    )
)
def wait_given_time_if_web_gui(client, seconds):
    if client == "web GUI":
        wait_given_time(seconds)


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) is idle for "
        r"(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds?"
    )
)
@wt(
    parsers.re(
        r"(?P<user>.+?) is idle for (?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds?"
    )
)
def wait_given_time(seconds):
    time.sleep(float(seconds))


@wt(parsers.parse("last operation by {user} succeeds"))
def success(user, users):
    assert not users[user].last_operation_failed


@wt(parsers.parse("last operation by {user} fails"))
def failure(user, users):
    assert users[user].last_operation_failed


def time_attr(parameter, prefix="st"):
    return f"{prefix}_{TIME_ATTR_MAPPING[parameter]}"


def compare(val1, val2, comparator):
    if comparator == "equal":
        return val1 == val2
    if comparator == "not equal":
        return val1 != val2
    if comparator == "greater":
        return val1 > val2
    if comparator == "less":
        return val1 < val2
    if comparator == "not greater":
        return val1 <= val2
    if comparator in ["not less", "greater or equal"]:
        return val1 >= val2
    raise ValueError("Wrong argument comparator to function compare")
