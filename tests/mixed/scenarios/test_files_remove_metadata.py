"""Test suite for mixed tests of removing files metadata
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
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.onezone.common import *

from tests.gui.conftest import *

from tests.oneclient.steps.auth_steps import *

from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.common.url import *


@pytest.fixture(scope='module')
def screens():
    return [0]


# TODO: VFS-9477 enable metadata tests after reimplement
scenarios('../features/pass.feature')
# scenarios('../features/oneprovider/files_remove_metadata.feature')

