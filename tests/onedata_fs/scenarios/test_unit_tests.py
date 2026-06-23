"""This module contains tests suite for onedata_fs unit tests.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import scenarios

from tests.onedata_fs.steps.run_unit_tests import *


scenarios('../features/unit_tests.feature')
