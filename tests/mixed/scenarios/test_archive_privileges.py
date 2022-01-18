"""Test suite for mixed archives privileges tests
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from pytest_bdd import scenario, scenarios

from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.rest.env_up.users import *
from tests.gui.conftest import *


# empty test for backward compatibility on bamboo
scenarios('../features/pass.feature')

