"""This module implements pytest-bdd steps for running onedata_fs unit tests
in oneclient container.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os
import glob
from xml.etree import ElementTree

import yaml
from pytest_bdd import parsers, when, given, then

from tests.utils.docker_utils import run_cmd
from tests.utils.utils import check_call_with_logging
from ..unit_tests import (SPACE_NAME, PROVIDER_IP, ACCESS_TOKEN, ROOT_USER,
                          CONTAINER_ONEDATA_FS_DIR, LOCAL_UNIT_TESTS_DIR,
                          CONTAINER_TEST_CFG_FILE, CONTAINER_REPORTS_XML_DIR,
                          TEST_MODULE)


@given(parsers.re('onedata_fs unit tests directory in "(?P<client>.*)" '
                  'container'))
def unit_tests_directory_in_client_container(hosts, client):
    run_cmd(ROOT_USER, hosts[client]['container-id'],
            'mkdir -p {}'.format(CONTAINER_ONEDATA_FS_DIR))

    cmd = ['docker', 'cp', LOCAL_UNIT_TESTS_DIR,
           '{0}:{1}'.format(hosts[client]['container-id'],
                            CONTAINER_ONEDATA_FS_DIR)]
    check_call_with_logging(cmd)


@when(parsers.re('root user starts onedata_fs unit tests in "(?P<client>.*)" '
                 'container using python <python_version> and following test '
                 'configuration:\n(?P<cfg>(.|\s)*)'))
def run_tests_in_container(client, cfg, hosts, users, python_version):
    cfg = yaml.load(cfg, Loader=yaml.Loader)

    test_cfg = {
        PROVIDER_IP: hosts[cfg.get('oneprovider')]['ip'],
        SPACE_NAME: cfg.get('space'),
        ACCESS_TOKEN: users[cfg.get('user')].token
    }

    dump_test_cfg_cmd = "echo '{}' > {}".format(yaml.dump(test_cfg),
                                                CONTAINER_TEST_CFG_FILE)
    run_cmd(ROOT_USER, hosts[client]['container-id'], dump_test_cfg_cmd)

    run_tests_cmd = 'python{} -m {}'.format(python_version, TEST_MODULE)
    run_cmd(ROOT_USER, hosts[client]['container-id'],
            'cd {} && {}'.format(CONTAINER_ONEDATA_FS_DIR, run_tests_cmd))


@then(parsers.re('root user fetches tests results for python <python_version> '
                 'from "(?P<client>.*)" container'))
def fetch_test_results(client, python_version, hosts):
    results_path = os.path.join('test-reports', 'python{}'.
                                format(python_version))
    if not os.path.isdir(results_path):
        os.makedirs(results_path)

    cmd = ['docker', 'cp',
           '{0}:{1}'.format(hosts[client]['container-id'],
                            CONTAINER_REPORTS_XML_DIR),
           results_path]
    check_call_with_logging(cmd)
    _override_testcases_names(results_path, python_version)


def _override_testcases_names(results_path, python_version):
    reports = glob.glob(os.path.join(results_path, 'xml/*'))
    for report in reports:
        tree = ElementTree.parse(report)
        testsuite = tree.getroot()
        testcases = testsuite.findall('testcase')
        for testcase in testcases:
            testcase.attrib['name'] += '_python{}'.format(python_version)
        tree.write(report)
