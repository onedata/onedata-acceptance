"""Test suite for cancelling transfers directories.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import pytest
from pytest_bdd import scenarios, scenario


from tests.gui.steps.rest.cdmi import *
from tests.gui.steps.rest.env_up.users import *
from tests.gui.steps.rest.env_up.groups import *
from tests.gui.steps.rest.env_up.spaces import *
from tests.gui.steps.rest.env_up.storage import *

from tests.gui.steps.common.url import *
from tests.gui.steps.common.browser_creation import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.common.local_file_system import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.common.login import *
from tests.gui.steps.common.docker import *

from tests.gui.steps.common import *

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.user_full_name import *
from tests.gui.steps.onezone.tokens import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.onezone.manage_account import *
from tests.gui.steps.onezone.spaces import *

from tests.gui.steps.oneprovider.common import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.shares import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider.spaces import *
from tests.gui.steps.oneprovider.transfers import *
from tests.gui.steps.oneprovider.browser import *
from tests.gui.meta_steps.oneprovider.common import *

from tests.gui.steps.modals.modal import *
from tests.gui.steps.oneprovider_common import *
from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.oneprovider.transfers import *
from tests.gui.meta_steps.oneprovider.data import *

from tests.utils.acceptance_utils import *


@pytest.fixture(scope='module')
def screens():
    return [0]


# TODO: VFS-9473 reimplement gui data distribution tests after move to file info modal
scenarios('../features/pass.feature')
# scenarios('../features/oneprovider/transfers/cancel_transfer.feature')
