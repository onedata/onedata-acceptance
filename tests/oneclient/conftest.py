"""This module contains definitions of fixtures used in oneclient tests
of onedata.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import pytest

from tests.conftest import export_logs


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
def finalize(request, env_description_abs_path):
    yield
    export_logs(request, env_description_abs_path)
