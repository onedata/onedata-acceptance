"""This module contains tests suite for automation management concerning
automation members and privileges using Onezone GUI and multiple browsers
 instances.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest import fixture
from pytest_bdd import scenario, scenarios

from tests.utils.entities_setup.users import *
from tests.utils.entities_setup.groups import *
from tests.utils.entities_setup.spaces import *

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

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.user_full_name import *
from tests.gui.steps.onezone.tokens import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.onezone.manage_account import *
from tests.gui.steps.onezone.groups import *
from tests.gui.steps.onezone.spaces import *
from tests.gui.steps.onezone.members import *
from tests.gui.steps.onezone.multibrowser_spaces import *

from tests.gui.steps.oneprovider.common import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.shares import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider.spaces import *
from tests.gui.steps.oneprovider.browser import *

from tests.gui.steps.modals.modal import *
from tests.gui.steps.oneprovider_common import *
from tests.gui.steps.oneprovider.permissions import *

from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.onezone.spaces import *
from tests.gui.meta_steps.onezone.tokens import *
from tests.gui.meta_steps.onezone.automation.workflow_management import *
from tests.gui.meta_steps.onezone.automation.lambda_creation import *
from tests.gui.meta_steps.oneprovider.automation.run_workflow import *
from tests.gui.meta_steps.oneprovider.automation.workflow_results import *

from tests.utils.acceptance_utils import *

from tests.gui.steps.onezone.automation.automation_basic import *
from tests.gui.steps.onezone.automation.workflow_creation import *
from tests.gui.steps.oneprovider.automation.automation_basic import *
from tests.gui.steps.oneprovider.automation.initial_values import *
from tests.gui.meta_steps.onezone.tokens import *
from tests.gui.steps.onezone.members import *
from tests.utils.entities_setup.inventory import *


@fixture(scope='module')
def screens():
    return [0, 1]


scenarios('../features/atm/onezone/automation_members.feature')
scenarios('../features/atm/onezone/automation_effective_privileges.feature')
scenarios('../features/atm/workflow_stores_privileges.feature')
