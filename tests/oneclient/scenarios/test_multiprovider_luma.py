"""This module contains tests suite for LUMA acceptance tests using multiple providers."""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from pytest_bdd import scenarios
from tests.oneclient.steps.multi_auth_steps import *
from tests.oneclient.steps.multi_dir_steps import *
from tests.oneclient.steps.multi_file_steps import *
from tests.oneclient.steps.multi_reg_file_steps import *
from tests.utils.acceptance_utils import *

scenarios("../features/multiprovider_luma.feature")
