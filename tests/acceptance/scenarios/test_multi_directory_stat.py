"""Test suite for reading/changing  metadata of directories in onedata,
in multi-client environment.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.utils.acceptance_utils import *

from tests.acceptance.steps.multi_auth_steps import *
from tests.acceptance.steps.multi_dir_steps import *
from tests.acceptance.steps.multi_file_steps import *
from tests.acceptance.steps.multi_reg_file_steps import *

from pytest_bdd import scenario
from functools import partial


scenario = partial(scenario, '../features/multi_directory_stat.feature')


@scenario('Check file type')
def test_type(env_description_file):
    pass


@scenario('Check default access permissions')
def test_default_access(env_description_file):
    pass


@scenario('Change access permissions')
def test_change_access(env_description_file):
    pass


@scenario('Change someone\'s file access permissions')
def test_change_access_someone(env_description_file):
    pass


@scenario('Timestamps at creation')
def test_timestamp(env_description_file):
    pass


@scenario('Update timestamps without write permission')
def test_update_timestamp_without_permission(env_description_file):
    pass


@scenario('Update timestamps with write permission')
def test_update_timestamp_with_permission(env_description_file):
    pass


@scenario('Access time')
def test_access_time(env_description_file):
    pass


@scenario('Modification time')
def test_modification_time(env_description_file):
    pass


@scenario('Status-change time when renaming')
def test_stat_change_time_mv(env_description_file):
    pass


@scenario('Status-change time when changing mode')
def test_stat_change_time_chmod(env_description_file):
    pass


