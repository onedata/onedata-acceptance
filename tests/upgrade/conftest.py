"""This module contains definitions of pytest fixtures that are used in
upgrade tests of onedata.
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import inspect

import yaml

from tests import *
from tests.conftest import export_logs, make_logdir, get_test_type
from tests.utils.path_utils import get_file_name
from tests.utils.git_utils import get_branch_name, get_commit, get_repository
from tests.utils.performance_utils import *
from tests.utils.utils import get_copyright, get_authors, get_suite_description


@pytest.fixture(autouse=True, scope='module')
def finalize(request, env_description_abs_path):
    yield
    export_logs(request, env_description_abs_path)
