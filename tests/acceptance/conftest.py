"""This module contains definitions of fixtures used in acceptance tests
of onedata.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os
import pytest

from tests.test_type import map_test_type_to_logdir
from tests.conftest import get_test_type
from tests.utils.path_utils import make_logdir, get_file_name
from tests.utils.onenv_utils import run_onenv_command


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
    test_type = get_test_type(request)
    logdir_path = map_test_type_to_logdir(test_type)
    feature_name = request.module.__name__.split('.')[-1]
    test_path = os.path.join(get_file_name(env_description_abs_path),
                             feature_name)
    logdir_path = make_logdir(logdir_path, test_path)
    run_onenv_command('export', [logdir_path])
