"""Test suite for mixed ACL one entry tests
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from pytest_bdd import scenarios

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

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.user_full_name import *
from tests.gui.steps.onezone.tokens import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.onezone.manage_account import *

from tests.gui.steps.oneprovider.common import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.shares import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider.spaces import *

from tests.gui.steps.modals.modal import *
from tests.gui.steps.oneprovider_common import *
from tests.gui.meta_steps.onezone import *
from tests.gui.meta_steps.oneprovider.data import *

from tests.gui.conftest import *

from tests.mixed.steps.data_basic import *
from tests.mixed.steps.data_permissions import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.onezone.common import *

from tests.oneclient.steps.auth_steps import *


@pytest.fixture(scope='module')
def screens():
    return [0]


scenarios('../features/oneprovider/acl_one_entry.feature')
