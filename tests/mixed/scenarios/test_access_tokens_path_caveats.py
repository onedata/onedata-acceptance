"""Test suite for GUI, REST and Onepanel cooperation
 for access tokens path caveats tests
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from pytest_bdd import scenarios

from tests.gui.steps.rest.env_up.users import *
from tests.gui.steps.rest.env_up.groups import *
from tests.gui.steps.rest.env_up.spaces import *

from tests.gui.steps.oneprovider_common import *
from tests.gui.meta_steps.onezone import *
from tests.gui.meta_steps.oneprovider.data import *

from tests.mixed.steps.data_basic import *
from tests.mixed.steps.onepanel_basic import *
from tests.mixed.steps.tokens_basic import *
from tests.mixed.steps.rest.onezone.tokens import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.onezone.common import *
from tests.gui.meta_steps.onezone.tokens import *

from tests.mixed.utils.common import *

from tests.gui.conftest import *

from tests.oneclient.steps.auth_steps import *
from tests.oneclient.steps.multi_file_steps import *

from tests.gui.steps.common.miscellaneous import *


@pytest.fixture(scope='module')
def screens():
    return [0, 1]


scenarios('../features/onezone/path_caveats.feature')
