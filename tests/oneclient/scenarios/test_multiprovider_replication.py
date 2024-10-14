"""Test suite for CRUD operations on regular files in onedata."""

__author__ = "Tomasz Lichon"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from functools import partial

from pytest_bdd import scenario
from tests.oneclient.steps.multi_auth_steps import *
from tests.oneclient.steps.multi_dir_steps import *
from tests.oneclient.steps.multi_file_steps import *
from tests.oneclient.steps.multi_reg_file_steps import *
from tests.utils.acceptance_utils import *

scenario = partial(scenario, "../features/multiprovider_replication.feature")


@scenario("Create files on one provider and see them on the other provider")
def test_create_and_list(env_description_file):
    pass


@scenario("Create empty file on one provider and read it on the other provider")
def test_create_empty_and_read(env_description_file):
    pass


@scenario("Write to file on one provider and check size on the other provider")
def test_write_and_check_size(env_description_file):
    pass


@scenario("Write to file on one provider and read on the other provider")
def test_write_and_read(env_description_file):
    pass


@scenario("Big file transfer with MD5 check")
def test_big_transfer_and_md5_check(env_description_file):
    pass


@scenario(
    "Create nonempty file on one provider and override its contents on "
    "the other provider"
)
def test_remote_file_override(env_description_file):
    pass


@scenario(
    "Create nonempty file on one provider and remove it on the other provider"
)
def test_remote_file_removal(env_description_file):
    pass


@scenario("Create nonempty file, append remotely, append locally and read both")
def test_sequential_appends(env_description_file):
    pass


@scenario(
    "Concurrently write disjoint ranges and read the same on both providers"
)
def test_conflict_on_disjoint_blocks(env_description_file):
    pass
