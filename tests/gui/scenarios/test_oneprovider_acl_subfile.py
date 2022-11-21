"""This module contains tests suite for ACL subfiles privileges operations
using Oneprovider GUI and multiple browsers instance.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest import fixture
from pytest_bdd import scenario, scenarios

from tests.utils.environment_setup.users import *
from tests.utils.environment_setup.groups import *
from tests.utils.environment_setup.spaces import *

from tests.gui.steps.common.url import *
from tests.gui.steps.common.browser_creation import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.common.local_file_system import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.common.login import *

from tests.gui.steps.onepanel.account_management import *
from tests.gui.steps.onepanel.nodes import *
from tests.gui.steps.onepanel.common import *
from tests.gui.steps.onepanel.deployment import *
from tests.gui.steps.onepanel.spaces import *

from tests.gui.steps.onezone.providers import *

from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.oneprovider.permissions import *

from tests.utils.acceptance_utils import *


@fixture(scope='module')
def screens():
    return [0, 1]


scenarios('../features/oneprovider/data/subfile_acl_privileges.feature')

