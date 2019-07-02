"""This module contains tests suite for basic operations using
Onezone GUI and single browser instance.
"""

__author__ = "Bartosz Walkowicz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest import fixture
from pytest_bdd import scenario, scenarios

from tests.gui.steps.rest.env_up.users import *
from tests.gui.steps.rest.env_up.groups import *
from tests.gui.steps.rest.env_up.spaces import *

from tests.gui.steps.common.url import *
from tests.gui.steps.common.browser_creation import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.common.local_file_system import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.common.login import *
from tests.gui.steps.common.docker import *

from tests.gui.steps.onepanel.account_management import *
from tests.gui.steps.onepanel.nodes import *
from tests.gui.steps.onepanel.common import *
from tests.gui.steps.onepanel.deployment import *
from tests.gui.steps.onepanel.spaces import *

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.user_alias import *
from tests.gui.steps.onezone.access_tokens import *
from tests.gui.steps.onezone.data_space_management import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.onezone.manage_account import *
from tests.gui.steps.onezone.groups import *
from tests.gui.steps.onezone.members import *
from tests.gui.steps.onezone.spaces import *
from tests.gui.steps.onezone.multibrowser_spaces import *
from tests.gui.steps.onezone.discovery import *
from tests.gui.steps.onezone.clusters import *

from tests.gui.steps.oneprovider.common import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.shares import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider.spaces import *

from tests.gui.steps.modal import *
from tests.gui.steps.oneprovider_common import *

from tests.gui.meta_steps.onezone import *
from tests.gui.meta_steps.onezone.groups import *
from tests.gui.meta_steps.onezone.spaces import *
from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.onezone.harvesters import *
from tests.gui.meta_steps.onepanel.spaces import *

from tests.utils.acceptance_utils import *


@fixture(scope='module')
def screens():
    return [0]


scenarios('../features/onezone/login_page.feature')
scenarios('../features/onezone/providers.feature')
scenarios('../features/onezone/providers_multibrowser.feature')
scenarios('../features/onezone/access_tokens.feature')

scenarios('../features/onezone/groups/groups_creation.feature')
scenarios('../features/onezone/groups/groups_basic_operations.feature')
scenarios('../features/onezone/groups/groups_join.feature')
scenarios('../features/onezone/groups/'
          'groups_multiple_users_with_single_group.feature')
scenarios('../features/onezone/groups/groups_subgroup.feature')
scenarios('../features/onezone/groups/'
          'groups_multiple_users_with_multiple_groups.feature')
scenarios('../features/onezone/groups/groups_hierarchy.feature')
scenarios('../features/onezone/groups/groups_memberships.feature')
scenarios('../features/onezone/groups/groups_memberships_multibrowser.feature')
scenarios('../features/onezone/groups/groups_memberships_privileges.feature')
scenarios('../features/onezone/harvesters.feature')

