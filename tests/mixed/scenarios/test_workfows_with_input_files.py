"""Test suite for mixed tests workflows execution with example input files
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from pytest_bdd import scenarios

from tests.utils.entities_setup.users import *
from tests.utils.entities_setup.groups import *
from tests.utils.entities_setup.spaces import *
from tests.utils.entities_setup.inventory import *

from tests.gui.steps.common.url import *
from tests.gui.steps.common.browser_creation import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.common.local_file_system import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.common.login import *

from tests.mixed.steps.data_basic import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.onezone.common import *
from tests.mixed.steps.rest.onezone.automation import *

from tests.oneclient.steps.auth_steps import *
from tests.gui.conftest import *


@pytest.fixture(scope='module')
def screens():
    return [0]


scenarios('../features/oneprovider/automation_workflows_execution.feature')
