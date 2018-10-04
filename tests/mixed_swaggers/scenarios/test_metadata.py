"""Test suite for mixed metadata management tests
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from pytest_bdd import scenarios

from tests.gui.steps.rest.env_up.users import *
from tests.gui.steps.rest.env_up.groups import *
from tests.gui.steps.rest.env_up.spaces import *

from tests.gui.steps.oneprovider_common import *
from tests.gui.meta_steps.onezone import *

from tests.mixed_swaggers.steps.data_basic import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.onezone.common import *

from tests.gui.conftest import *


scenarios('../features/metadata_basic.feature')
