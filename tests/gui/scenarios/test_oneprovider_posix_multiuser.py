"""Test suite for features of POSIX privileges multiuser tests.
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import pytest
from pytest_bdd import scenarios, scenario

from tests.gui.steps.rest.env_up.users import *
from tests.gui.steps.rest.env_up.groups import *
from tests.gui.steps.rest.env_up.spaces import *

from tests.gui.steps.common.url import *
from tests.gui.steps.common.browser_creation import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.login import *

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.user_full_name import *
from tests.gui.steps.onezone.access_tokens import *
from tests.gui.steps.onezone.data_space_management import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.onezone.manage_account import *

from tests.gui.steps.rest.cdmi import *

from tests.gui.steps.oneprovider.permissions import *
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
from tests.gui.meta_steps.oneprovider.data import *

from tests.utils.acceptance_utils import *


@pytest.fixture(scope='module')
def screens():
    return [0, 1]


# TODO: change test because of a new gui
# scenarios('../features/oneprovider/data/posix/privileges_posix_multi.feature')
scenarios('../features/pass.feature')
