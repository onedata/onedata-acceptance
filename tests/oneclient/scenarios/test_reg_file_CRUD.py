"""Test suite for CRUD operations on regular files in onedata."""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from functools import partial

from pytest_bdd import scenario
from tests.oneclient.steps.auth_steps import *
from tests.oneclient.steps.dir_steps import *
from tests.oneclient.steps.environment_steps import *
from tests.oneclient.steps.file_steps import *
from tests.oneclient.steps.multi_dir_steps import *
from tests.oneclient.steps.multi_file_steps import *
from tests.oneclient.steps.reg_file_steps import *
from tests.utils.acceptance_utils import *

scenario = partial(scenario, "../features/reg_file_CRUD.feature")


@scenario("Create regular file")
def test_create(env_description_file):
    pass


@scenario("Create many children")
def test_create_many(env_description_file):
    pass


@scenario("Rename regular file")
def test_rename(env_description_file):
    pass


@scenario("Delete regular file")
def test_delete(env_description_file):
    pass


@scenario("Read and write to regular file")
def test_read_write(env_description_file):
    pass


@scenario("Write to regular file and assert size after listing")
def test_assert_size_after_listing(env_description_file):
    pass


@scenario("Append to regular file")
def test_append(env_description_file):
    pass


@scenario("Replace word in file")
def test_replace(env_description_file):
    pass


@scenario("Move regular file and read")
def test_move(env_description_file):
    pass


@scenario("Move big regular file and check MD5")
def test_move_big(env_description_file):
    pass


@scenario("Copy regular file and read")
def test_copy(env_description_file):
    pass


@scenario("Copy big regular file and check MD5")
def test_copy_big(env_description_file):
    pass


@scenario("Delete file copied right after read")
def test_delete_copied_after_read(env_description_file):
    pass


@scenario("Restart provider with active oneclient connection")
def test_provider_restart(env_description_file):
    pass


@scenario("Restart provider network for short time with active oneclient connection")
def test_network_restart_short(env_description_file):
    pass


@scenario("Restart provider network for long time with active oneclient connection")
def test_network_restart_long(env_description_file):
    pass
