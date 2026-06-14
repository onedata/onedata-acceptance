"""Define fixtures used in onedata_fs tests."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Generator

import pytest

from tests import LOGDIRS
from tests.conftest import export_logs, get_test_type, make_logdir


@pytest.fixture(autouse=True, scope="session")
def logdir(request: pytest.FixtureRequest) -> str:
    test_type = get_test_type(request)
    return make_logdir(LOGDIRS.get(test_type), "report")


@pytest.fixture(autouse=True, scope="session")
def finalize(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    yield
    export_logs(request)
