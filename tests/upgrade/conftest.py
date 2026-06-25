"""This module contains definitions of pytest fixtures that are used in
upgrade tests of onedata.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Generator
from typing import cast

import pytest

from tests.conftest import export_logs
from tests.type_definitions import EnvDesc, Hosts, TestConfig, Users
from tests.upgrade.utils.upgrade_utils import UpgradeConfig, UpgradeTestsController
from tests.utils.environment_utils import clean_env


@pytest.fixture()
def tests_controller(
    test_config: TestConfig,
    hosts: Hosts,
    clients: dict[str, object],
    request: pytest.FixtureRequest,
    users: Users,
    env_desc: EnvDesc,
    scenario_abs_path: str,
    env_description_abs_path: str,
) -> UpgradeTestsController:
    return UpgradeTestsController(
        cast(UpgradeConfig, test_config),
        hosts,
        clients,
        request,
        users,
        env_desc,
        scenario_abs_path,
        env_description_abs_path,
    )


@pytest.fixture(autouse=True, scope="module")
def finalize(
    request: pytest.FixtureRequest, env_description_abs_path: str
) -> Generator[None, None, None]:
    yield
    export_logs(request, env_description_abs_path, "after_upgrade")
    clean_env()
