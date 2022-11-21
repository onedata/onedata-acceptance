"""Test suite for mixed tests of setting files metadata
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from pytest_bdd import scenarios

from tests.utils.environment_setup.users import *
from tests.utils.environment_setup.groups import *
from tests.utils.environment_setup.spaces import *

from tests.gui.steps.oneprovider_common import *
from tests.gui.meta_steps.onezone import *
from tests.gui.meta_steps.oneprovider.data import *

from tests.mixed.steps.data_basic import *
from tests.mixed.steps.onepanel_basic import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.onezone.common import *

from tests.gui.conftest import *

from tests.oneclient.steps.auth_steps import *

from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.common.url import *


@pytest.fixture(scope='module')
def screens():
    return [0]


scenarios('../features/oneprovider/files_set_metadata.feature')
