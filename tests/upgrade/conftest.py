"""This module contains definitions of pytest fixtures that are used in
upgrade tests of onedata.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Any

import pytest

from tests.conftest import export_logs
from tests.upgrade.utils.upgrade_utils import UpgradeTestsController
from tests.utils.environment_utils import clean_env


@pytest.fixture()
def tests_controller(
    test_config: Any,
    hosts: Any,
    clients: Any,
    request: Any,
    users: Any,
    env_desc: Any,
    scenario_abs_path: Any,
    env_description_abs_path: Any,
) -> Any:
    return UpgradeTestsController(
        test_config,
        hosts,
        clients,
        request,
        users,
        env_desc,
        scenario_abs_path,
        env_description_abs_path,
    )


@pytest.fixture(autouse=True, scope="module")
def finalize(request: Any, env_description_abs_path: Any) -> Any:
    yield
    export_logs(request, env_description_abs_path, "after_upgrade")
    clean_env()
