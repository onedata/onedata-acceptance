"""This module contains tests suite for basic operations using
Oneprovider data tab GUI and single browser instance.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from functools import partial

from pytest import fixture, mark
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

from tests.gui.steps.onepanel.account_management import *
from tests.gui.steps.onepanel.nodes import *
from tests.gui.steps.onepanel.common import *
from tests.gui.steps.onepanel.deployment import *
from tests.gui.steps.onepanel.spaces import *

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.user_full_name import *
from tests.gui.steps.onezone.tokens import *
from tests.gui.steps.onezone.data_space_management import *
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
from tests.gui.steps.oneprovider.dataset import *
from tests.gui.steps.oneprovider.browser import *

from tests.gui.steps.modal import *
from tests.gui.steps.oneprovider_common import *
from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.onezone.tokens import *
from tests.gui.meta_steps.oneprovider.common import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.oneprovider.dataset import *

from . import BROWSER

from tests.utils.acceptance_utils import *

from tests.gui.steps.onezone.automation import *
from tests.gui.meta_steps.onezone.tokens import *
from tests.gui.steps.onezone.members import *
from tests.gui.steps.rest.env_up.inventory import *


@fixture(scope='module')
def screens():
    return [0, 1]


scenario = partial(scenario, '../features/oneprovider/data/upload_multiple_files.feature')

skip_if_not_chrome = mark.skipif(BROWSER != 'Chrome',
                                 reason='some behaviour like multiple file '
                                        'upload at once can only be '
                                        'simulated in Chrome')


@skip_if_not_chrome
@scenario('User uploads 5 files at once')
def test_user_uploads_5_files_at_once():
    pass


@skip_if_not_chrome
@scenario('User uploads more than 50 files and uses files list lazy loading')
def test_user_uploads_more_than_50_files_and_uses_files_list_lazy_loading():
    pass


@skip_if_not_chrome
@scenario('User can change directory while uploading files')
def test_user_can_change_directory_while_uploading_files():
    pass


@skip_if_not_chrome
@scenario('Files uploaded by user are ordered by name')
def test_files_uploaded_by_user_are_ordered_by_name():
    pass


scenarios('../features/oneprovider/data/empty_file_browser.feature')
scenarios('../features/oneprovider/data/single_file.feature')
scenarios('../features/oneprovider/data/several_files.feature')
scenarios('../features/oneprovider/data/single_directory.feature')
scenarios('../features/oneprovider/data/file_management.feature')
scenarios('../features/oneprovider/data/nested_directories.feature')
scenarios('../features/oneprovider/data/create_archive.feature')
scenarios('../features/oneprovider/data/dataset.feature')
scenarios('../features/oneprovider/data/dataset_privileges.feature')

scenarios('../features/onezone/automation_basics.feature')
scenarios('../features/onezone/automation_members.feature')

