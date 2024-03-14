"""Test suite for modifying storage parameters.
"""
__author__ = "Bartek Kryza"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from functools import partial

from pytest_bdd import scenario

from tests.oneclient.steps.auth_steps import *
from tests.oneclient.steps.multi_dir_steps import *
from tests.oneclient.steps.dir_steps import *
from tests.oneclient.steps.multi_file_steps import *
from tests.oneclient.steps.file_steps import *
from tests.oneclient.steps.file_steps import *
from tests.oneclient.steps.reg_file_steps import *
from tests.utils.acceptance_utils import *
from tests.oneclient.steps.environment_steps import *
from tests.oneclient.steps.storage_steps import *

scenario = partial(scenario, '../features/storage_modification.feature')


@scenario('Change Ceph parameters with active oneclient connection')
def test_ceph_storage_parameter_change(env_description_file):
    pass


@scenario('Change S3 parameters with active oneclient connection')
def test_s3_storage_parameter_change(env_description_file):
    pass


@scenario('Change POSIX parameters with active oneclient connection')
def test_posix_storage_parameter_change(env_description_file):
    pass