"""This module contains tests suite for hardlinks and symlinks using
oneclient and REST API.
"""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

from pytest_bdd import scenario, scenarios

from tests.mixed.steps.data_basic import *
from tests.mixed.steps.hardlinks_symlinks import *
from tests.mixed.steps.oneclient.data_basic import *
from tests.mixed.steps.qos import *
from tests.mixed.steps.rest.onezone.automation import *
from tests.oneclient.steps.auth_steps import *
from tests.oneclient.steps.dir_steps import *
from tests.oneclient.steps.file_steps import *
from tests.oneclient.steps.multi_dir_steps import *
from tests.oneclient.steps.multi_file_steps import *
from tests.utils.acceptance_utils import *
from tests.utils.entities_setup.groups import *
from tests.utils.entities_setup.inventory import *
from tests.utils.entities_setup.spaces import *
from tests.utils.entities_setup.users import *

scenarios("../features/hardlinks_symlinks.feature")
