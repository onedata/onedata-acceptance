"""This module contains tests suite for basic operations in
Onepanel GUI and multiple browser instances.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
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
from tests.gui.steps.onepanel.provider import *
from tests.gui.steps.onepanel.common import *
from tests.gui.steps.onepanel.deployment import *
from tests.gui.steps.onepanel.spaces import *
from tests.gui.steps.onepanel.storages import *
from tests.gui.steps.onepanel.emergency_passphrase import *
from tests.gui.steps.onepanel.members import *

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.user_full_name import *
from tests.gui.steps.onezone.tokens import *
from tests.gui.steps.onezone.data_space_management import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.onezone.manage_account import *
from tests.gui.steps.onezone.spaces import *
from tests.gui.steps.onezone.multibrowser_spaces import *
from tests.gui.steps.onezone.clusters import *
from tests.gui.steps.onezone.members import *
from tests.gui.steps.onezone.groups import *

from tests.gui.steps.oneprovider.common import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.shares import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider.spaces import *

from tests.gui.steps.modal import *
from tests.gui.steps.oneprovider_common import *

from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.onepanel.provider import *
from tests.gui.meta_steps.onepanel.spaces import *
from tests.gui.meta_steps.onezone.clusters import *
from tests.gui.meta_steps.onezone.groups import *
from tests.gui.meta_steps.onezone.spaces import *
from tests.gui.meta_steps.onezone.tokens import *
from tests.gui.meta_steps.onepanel.account_management import *
from tests.gui.meta_steps.onepanel.storages import *
from tests.gui.meta_steps.oneprovider.common import *
from tests.gui.meta_steps.oneprovider.data import *


from tests.mixed.steps.onepanel_basic import *
from tests.mixed.steps.space_basic import *

from tests.utils.acceptance_utils import *


@fixture(scope='module')
def screens():
    return [0, 1]


scenarios('../features/onepanel/storages.feature')
scenarios('../features/onepanel/provider.feature')
scenarios('../features/onepanel/spaces.feature')
scenarios('../features/onepanel/members.feature')
scenarios('../features/onepanel/emergency_passphrase.feature')
