"""This module implements some common basic functions and functionality for
acceptance tests of onedata.
"""

__author__ = "Jakub Kudzia, Piotr Ociepka, Michal Stanisz"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import json
import os
import subprocess
import time
from collections.abc import Mapping, Sequence
from typing import Any, TypeAlias

from tests.gui.utils.generic import (
    upload_file_path,
    upload_lambda_path,
    upload_workflow_path,
)
from tests.utils.bdd_utils import parsers, wt

TIME_ATTR_MAPPING = {
    "access": "atime",
    "modification": "mtime",
    "status-change": "ctime",
}

Command: TypeAlias = Sequence[str]
JsonObject: TypeAlias = dict[str, Any]


def list_parser(arg: str) -> list[str]:
    return [el.strip() for el in arg.strip("[]").split(",") if el != ""]


def make_arg_list(arg: str) -> str:
    return "[" + arg + "]"


def execute_command(
    cmd: Command, error: str | None = None, should_fail: bool = False
) -> bytes:
    with subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as process:
        output, err = process.communicate()
        proc_returncode = process.returncode
        err_str = err.decode() if isinstance(err, bytes) else err
        out_str = output.decode() if isinstance(output, bytes) else output

    if (proc_returncode != 0) ^ should_fail:
        raise RuntimeError(
            f"{error}: {err_str}; {out_str}"
            if error
            else (
                f"Command did not fail: {' '.join(cmd)}, Err: {err_str}, Output:"
                f" {out_str}"
                if should_fail
                else (
                    f'Error when executing command "{" ".join(cmd)}": {err_str};'
                    f" {out_str}"
                )
            )
        )
    return output


@wt(
    parsers.re(
        "if (?P<client>.+?) is web GUI, (?P<user>.+?) is idle for "
        r"(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds?"
    )
)
def wait_given_time_if_web_gui(client: str, seconds: str) -> None:
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
def wait_given_time(seconds: str | float) -> None:
    time.sleep(float(seconds))


@wt(parsers.parse("last operation by {user} succeeds"))
def success(user: str, users: Mapping[str, Any]) -> None:
    assert not users[user].last_operation_failed


@wt(parsers.parse("last operation by {user} fails"))
def failure(user: str, users: Mapping[str, Any]) -> None:
    assert users[user].last_operation_failed


def time_attr(parameter: str, prefix: str = "st") -> str:
    return f"{prefix}_{TIME_ATTR_MAPPING[parameter]}"


def compare(val1: Any, val2: Any, comparator: str) -> bool:
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


def get_workflow_dump(workflow_name: str) -> JsonObject:
    if os.path.isfile(upload_workflow_path(f"{workflow_name}.json")):
        path = upload_workflow_path(f"{workflow_name}.json")
    elif os.path.isfile(upload_workflow_path(f"{workflow_name}/{workflow_name}.json")):
        path = upload_workflow_path(f"{workflow_name}/{workflow_name}.json")
    elif os.path.isfile(upload_file_path(f"automation/workflow/{workflow_name}.json")):
        path = upload_file_path(f"automation/workflow/{workflow_name}.json")
    else:
        raise FileNotFoundError(f"Path to {workflow_name} not found")
    with open(path) as f:
        data = json.load(f)
    return data


def get_lambda_dump(lambda_name: str) -> JsonObject:
    with open(
        upload_lambda_path("".join([lambda_name, "/", lambda_name, ".json"]))
    ) as f:
        data = json.load(f)
    return data


def num_to_ordinal(n: int) -> str:
    return {
        -1: "last",
        0: "first",
        1: "second",
        2: "third",
        3: "fourth",
        4: "fifth",
        5: "sixth",
        6: "seventh",
        7: "eighth",
        8: "ninth",
        9: "tenth",
    }.get(n, f"{n}th")
