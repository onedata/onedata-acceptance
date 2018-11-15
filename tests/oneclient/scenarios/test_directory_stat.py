"""Test suite for reading/changing  metadata of directories in onedata.
"""
__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from functools import partial

from pytest_bdd import scenario

from tests.oneclient.steps.auth_steps import *
from tests.oneclient.steps.multi_dir_steps import *
from tests.oneclient.steps.dir_steps import *
from tests.oneclient.steps.multi_file_steps import *
from tests.oneclient.steps.file_steps import *
from tests.utils.acceptance_utils import *


scenario = partial(scenario, '../features/directory_stat.feature')


@scenario('Check file type')
def test_type(env_description_file):
    pass


@scenario('Check default access permissions')
def test_default_access(env_description_file):
    pass


@scenario('Change access permissions')
def test_change_access(env_description_file):
    pass


@scenario('Timestamps at creation')
def test_timestamp(env_description_file):
    pass


@scenario('Update timestamps')
def test_update_timestamp(env_description_file):
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


