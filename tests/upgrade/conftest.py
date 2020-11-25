"""This module contains definitions of pytest fixtures that are used in
upgrade tests of onedata.
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import pytest

from tests.conftest import export_logs
from tests.utils.environment_utils import clean_env
from tests.upgrade.utils.upgrade_utils import UpgradeTestsController


@pytest.fixture()
def tests_controller(test_config, hosts, clients, request, users, env_desc, scenario_abs_path):
    return UpgradeTestsController(**locals())


@pytest.fixture(autouse=True, scope='module')
def finalize(request, env_description_abs_path):
    yield
    export_logs(request, env_description_abs_path)
    clean_env()
