"""This module contains tests suite for basic quality of service storage
management using one provider instances and multiple browser instance.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


import pytest
from pytest_bdd import scenario, scenarios
from tests.gui.meta_steps.onepanel.provider import *
from tests.gui.meta_steps.onepanel.spaces import *
from tests.gui.meta_steps.onepanel.storages import *
from tests.gui.meta_steps.oneprovider.common import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.oneprovider.qos import *
from tests.gui.meta_steps.oneprovider.transfers import *
from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.onezone.groups import *
from tests.gui.meta_steps.onezone.spaces import *
from tests.gui.meta_steps.onezone.tokens import *
from tests.gui.steps.common.browser_creation import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.common.docker import *
from tests.gui.steps.common.local_file_system import *
from tests.gui.steps.common.login import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.url import *
from tests.gui.steps.modals.modal import *
from tests.gui.steps.onepanel.account_management import *
from tests.gui.steps.onepanel.common import *
from tests.gui.steps.onepanel.deployment import *
from tests.gui.steps.onepanel.nodes import *
from tests.gui.steps.onepanel.spaces import *
from tests.gui.steps.onepanel.storages import *
from tests.gui.steps.oneprovider.common import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.qos import *
from tests.gui.steps.oneprovider.shares import *
from tests.gui.steps.oneprovider.spaces import *
from tests.gui.steps.oneprovider.transfers import *
from tests.gui.steps.oneprovider.uploads import *
from tests.gui.steps.oneprovider_common import *
from tests.gui.steps.onezone.clusters import *
from tests.gui.steps.onezone.groups import *
from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.manage_account import *
from tests.gui.steps.onezone.multibrowser_spaces import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.onezone.spaces import *
from tests.gui.steps.onezone.tokens import *
from tests.gui.steps.onezone.user_full_name import *
from tests.gui.steps.rest.cdmi import *
from tests.utils.acceptance_utils import *
from tests.utils.entities_setup.groups import *
from tests.utils.entities_setup.harvesters import *
from tests.utils.entities_setup.spaces import *
from tests.utils.entities_setup.users import *


@pytest.fixture(scope="module")
def screens():
    return [0, 1]


scenarios("../features/oneprovider/data/qos_storage_oneprovider.feature")
