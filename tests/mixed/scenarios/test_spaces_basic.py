"""Test suite for tests using swaggers and browser
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from pytest_bdd import scenarios

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

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.user_full_name import *
from tests.gui.steps.onezone.tokens import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.onezone.manage_account import *

from tests.gui.steps.modals.modal import *
from tests.gui.steps.oneprovider_common import *

from tests.gui.conftest import *

from tests.mixed.steps.space_basic import *
from tests.mixed.steps.members import *
from tests.mixed.steps.rest.onezone.special_dirs import *

from tests.oneclient.steps.auth_steps import *

from tests.gui.steps.oneprovider.common import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.shares import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider.spaces import *
from tests.gui.steps.oneprovider.browser import *
from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.oneprovider.common import *


@pytest.fixture(scope='module')
def screens():
    return [0, 1]


scenarios('../features/onezone/space/creation.feature')
scenarios('../features/onezone/space/basic_management.feature')
scenarios('../features/onezone/space/multiuser.feature')
scenarios('../features/onezone/space/multiuser_with_admin.feature')
scenarios('../features/onezone/space/user_root_dir.feature')
scenarios('../features/onezone/space/archives_root_dir.feature')
scenarios('../features/onezone/space/trash_dir.feature')
scenarios('../features/onezone/space/share_root_dir.feature')
