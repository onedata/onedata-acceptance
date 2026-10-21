"""
Definitions of fixtures used in mixed tests using different clients.
"""

from collections.abc import Generator

import pytest

from tests.utils.user_utils import Users

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

pytest_plugins = "tests.gui.conftest"


@pytest.fixture(autouse=True)
def unmount_clients_after_test(users: Users) -> Generator[None, None, None]:
    yield
    for user in users.values():
        for client in user.clients.values():
            client.unmount()
        user.clients.clear()
