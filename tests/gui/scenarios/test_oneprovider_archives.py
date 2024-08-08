"""This module contains tests suite for operations on BagIt, plain and DIP
archives using Oneprovider GUI and multiple browser instances.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from functools import partial

from pytest import fixture, mark
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
from tests.gui.steps.onezone.spaces import *
from tests.gui.steps.onezone.groups import *
from tests.gui.steps.onezone.members import *

from tests.gui.steps.oneprovider.common import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.shares import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider.spaces import *
from tests.gui.steps.oneprovider.permissions import *
from tests.gui.steps.oneprovider.archives import *
from tests.gui.steps.oneprovider.archives_audit import *
from tests.gui.steps.oneprovider.dataset import *
from tests.gui.steps.oneprovider.browser import *

from tests.gui.steps.modals.modal import *
from tests.gui.steps.oneprovider_common import *
from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.onezone.tokens import *
from tests.gui.meta_steps.oneprovider.common import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.oneprovider.dataset import *
from tests.gui.meta_steps.oneprovider.archives import *
from tests.gui.meta_steps.onepanel.spaces import *
from tests.gui.meta_steps.oneprovider.files_tree import *

from tests.oneclient.steps.environment_steps import *

from . import BROWSER

from tests.utils.acceptance_utils import *


@fixture(scope='module')
def screens():
    return [0, 1]


# scenarios('../features/oneprovider/data/archive_basic.feature')
# scenarios('../features/oneprovider/data/archive_bagit_and_dip.feature')
# scenarios('../features/oneprovider/data/archive_manage_privileges.feature')
scenarios('../features/oneprovider/data/archive_stats.feature')
