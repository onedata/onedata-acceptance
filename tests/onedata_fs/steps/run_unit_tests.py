"""This module implements pytest-bdd steps for running onedata_fs unit tests
in oneclient container.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import glob
import os
from typing import TypedDict, cast
from xml.etree import ElementTree

import yaml
from pytest_bdd import given, parsers, then, when

from tests.conftest import Hosts, Users
from tests.onedata_fs.unit_tests import (
    ACCESS_TOKEN,
    CONTAINER_ONEDATA_FS_DIR,
    CONTAINER_REPORTS_XML_DIR,
    CONTAINER_TEST_CFG_FILE,
    LOCAL_UNIT_TESTS_DIR,
    PROVIDER_IP,
    ROOT_USER,
    SPACE_NAME,
    TEST_MODULE,
)
from tests.utils.docker_utils import run_cmd
from tests.utils.utils import check_call_with_logging


class UnitTestConfig(TypedDict):
    oneprovider: str
    space: str
    user: str


@given(parsers.re('onedata_fs unit tests directory in "(?P<client>.*)" container'))
def unit_tests_directory_in_client_container(hosts: Hosts, client: str) -> None:
    container_id = hosts[client]["container_id"]
    run_cmd(ROOT_USER, container_id, f"mkdir -p {CONTAINER_ONEDATA_FS_DIR}")

    cmd = [
        "docker",
        "cp",
        LOCAL_UNIT_TESTS_DIR,
        f"{container_id}:{CONTAINER_ONEDATA_FS_DIR}",
    ]
    check_call_with_logging(cmd)


@when(
    parsers.re(
        'root user starts onedata_fs unit tests in "(?P<client>.*)" '
        "container using python <python_version> and following test "
        r"configuration:\n(?P<cfg>(.|\s)*)"
    )
)
def run_tests_in_container(
    client: str, cfg: str, hosts: Hosts, users: Users, python_version: str
) -> None:
    loaded_cfg = cast(UnitTestConfig, yaml.load(cfg, Loader=yaml.Loader))

    test_cfg = {
        PROVIDER_IP: hosts[loaded_cfg["oneprovider"]]["ip"],
        SPACE_NAME: loaded_cfg["space"],
        ACCESS_TOKEN: users[loaded_cfg["user"]].token,
    }

    dump_test_cfg_cmd = f"echo '{yaml.dump(test_cfg)}' > {CONTAINER_TEST_CFG_FILE}"
    container_id = hosts[client]["container_id"]
    run_cmd(ROOT_USER, container_id, dump_test_cfg_cmd)

    run_tests_cmd = f"python{python_version} -m {TEST_MODULE} --verbose"
    run_cmd(
        ROOT_USER, container_id, f"cd {CONTAINER_ONEDATA_FS_DIR} && {run_tests_cmd}"
    )


@then(
    parsers.re(
        "root user fetches tests results for python <python_version> "
        'from "(?P<client>.*)" container'
    )
)
def fetch_test_results(client: str, python_version: str, hosts: Hosts) -> None:
    results_path = os.path.join("test-reports", f"python{python_version}")
    if not os.path.isdir(results_path):
        os.makedirs(results_path)

    cmd = [
        "docker",
        "cp",
        f'{hosts[client]["container_id"]}:{CONTAINER_REPORTS_XML_DIR}',
        results_path,
    ]
    check_call_with_logging(cmd)
    _override_testcases_names(results_path, python_version)


def _override_testcases_names(results_path: str, python_version: str) -> None:
    reports = glob.glob(os.path.join(results_path, "xml/*"))
    for report in reports:
        tree = ElementTree.parse(report)
        testsuite = tree.getroot()
        testcases = testsuite.findall("testcase")
        for testcase in testcases:
            testcase.attrib["name"] += f"_python{python_version}"
        tree.write(report)
