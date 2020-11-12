"""Test suite for mixed directories metadata management tests
"""

__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
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


scenarios('../features/oneprovider/directories_metadata.feature')

