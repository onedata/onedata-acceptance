"""Test suite for CRUD operations on directories in onedata."""

__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from functools import partial

from pytest_bdd import scenario
from tests.oneclient.steps.auth_steps import *
from tests.oneclient.steps.dir_steps import *
from tests.oneclient.steps.file_steps import *
from tests.oneclient.steps.multi_dir_steps import *
from tests.oneclient.steps.multi_file_steps import *
from tests.utils.acceptance_utils import *

scenario = partial(scenario, "../features/directory_CRUD.feature")


@scenario("Create directory")
def test_create(env_description_file):
    pass


@scenario("Create directory in spaces directory")
def test_create_spaces_dir(env_description_file):
    pass


@scenario("Create space")
def test_create_space(env_description_file):
    pass


@scenario("Rename directory")
def test_rename(env_description_file):
    pass


@scenario("Delete empty directory")
def test_delete(env_description_file):
    pass


@scenario("Fail to delete space")
def test_delete_space(env_description_file):
    pass


@scenario("Create child directories")
def test_children(env_description_file):
    pass


@scenario("Create child directories 2")
def test_children2(env_description_file):
    pass


@scenario("Fail to create a duplicate directory")
def test_duplication(env_description_file):
    pass


@scenario("Delete empty directory and parents")
def test_delete_parents(env_description_file):
    pass


@scenario("Fail to delete non-empty directory using rmdir")
def test_delete_non_empty_wrong(env_description_file):
    pass


@scenario("Delete non-empty directory")
def test_delete_non_empty(env_description_file):
    pass


@scenario("Move directory")
def test_move(env_description_file):
    pass


@scenario("Copy directory")
def test_copy(env_description_file):
    pass


@scenario("Fail to move directory to itself")
def test_move_to_itself(env_description_file):
    pass


@scenario("Fail to move directory to its subtree")
def test_move_to_subtree(env_description_file):
    pass
