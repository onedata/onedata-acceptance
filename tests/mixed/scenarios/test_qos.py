"""Test suite for mixed datasets tests
"""

__author__ = "Agnieszka Warchoł, Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from pytest_bdd import scenario, scenarios

from tests.gui.steps.common.miscellaneous import *


scenarios('../features/pass.feature')