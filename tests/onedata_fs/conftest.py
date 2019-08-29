"""Define fixtures used in onedata_fs tests.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from pytest import fixture

from tests import LOGDIRS
from tests.conftest import export_logs, make_logdir, get_test_type


@fixture(autouse=True, scope='session')
def logdir(request):
    test_type = get_test_type(request)
    logdir = make_logdir(LOGDIRS.get(test_type), 'report')
    return logdir


@fixture(autouse=True, scope='session')
def finalize(request):
    yield
    export_logs(request)
