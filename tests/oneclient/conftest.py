"""This module contains definitions of fixtures used in oneclient tests
of onedata.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import pytest
import errno

from tests.conftest import export_logs
from tests.oneclient.steps.multi_dir_steps import purge_all_spaces


@pytest.fixture(autouse=True)
def skip_by_env(skip_by_env):
    """Autouse fixture defined in tests.conftest
    """
    pass


@pytest.fixture(autouse=True)
def xfail_by_env(xfail_by_env):
    """Autouse fixture defined in tests.conftest
    """
    pass


@pytest.fixture(autouse=True, scope='module')
def run_around_suite(request, env_description_abs_path):
    yield
    export_logs(request, env_description_abs_path)


@pytest.fixture(autouse=True)
def run_around_testcase(users):
    unmount_all_clients_and_purge_spaces(users)
    yield
    unmount_all_clients_and_purge_spaces(users)


def unmount_all_clients_and_purge_spaces(users):
    for user in users.values():
        for client in user.clients.values():
            purge_spaces(client)
            client.unmount()
        user.clients.clear()


def purge_spaces(client):
    purge_all_spaces(client)


def pytest_bdd_before_scenario(request, feature, scenario):
    print(f"\n=================================================================")
    print(f"- Executing scenario '{scenario.name}'")
    print(f"- from feature '{feature.name}'")
    print(f"-----------------------------------------------------------------")


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    print(f"-- Executing step: '{step}'")


def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    print(f"--- STEP FAILED\n")


def pytest_bdd_after_scenario(request, feature, scenario):
    print(f"=================================================================\n")

