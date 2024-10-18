"""Test suite for GUI, REST and Onepanel cooperation
for access tokens id caveats tests
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from pytest_bdd import scenarios
from tests.gui.conftest import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.onezone import *
from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.onezone.tokens import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.oneprovider_common import *
from tests.gui.steps.onezone.tokens import *
from tests.mixed.steps.data_basic import *
from tests.mixed.steps.group_basic import *
from tests.mixed.steps.onepanel_basic import *
from tests.mixed.steps.rest.onezone.group_management import *
from tests.mixed.steps.rest.onezone.tokens import *
from tests.mixed.steps.tokens_basic import *
from tests.mixed.utils.common import *
from tests.oneclient.steps.auth_steps import *
from tests.oneclient.steps.multi_file_steps import *
from tests.utils.acceptance_utils import *
from tests.utils.entities_setup.groups import *
from tests.utils.entities_setup.spaces import *
from tests.utils.entities_setup.users import *
from tests.mixed.steps.oneclient.data_basic import *


@pytest.fixture(scope="module")
def screens():
    return [0, 1]


scenarios("../features/onezone/id_caveats.feature")
