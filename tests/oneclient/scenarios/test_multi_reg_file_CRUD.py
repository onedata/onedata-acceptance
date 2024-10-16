"""Test suite for CRUD operations on regular files in onedata,
in multi-client environment.
"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from functools import partial

from pytest_bdd import scenario
from tests.oneclient.steps.multi_auth_steps import *
from tests.oneclient.steps.multi_dir_steps import *
from tests.oneclient.steps.multi_file_steps import *
from tests.oneclient.steps.multi_reg_file_steps import *
from tests.utils.acceptance_utils import *

scenario = partial(scenario, "../features/multi_reg_file_CRUD.feature")


@scenario("Create regular file")
def test_create(env_description_file):
    pass


@scenario(
    "Create a file, read it on the second client, delete it, and repeat "
    "the whole process"
)
def test_recreate_and_read(env_description_file):
    pass


@scenario("Fail to rename regular file without write permission on parent")
def test_rename_without_write_permission_on_parent(env_description_file):
    pass


@scenario("Rename regular file with write permission on parent")
def test_rename_with_permission(env_description_file):
    pass


@scenario("Delete regular file by owner")
def test_delete_by_owner(env_description_file):
    pass


@scenario("Delete regular file by other user with write permission on parent")
def test_delete_by_other_user(env_description_file):
    pass


@scenario(
    "Fail to delete regular file by other user without write permission on parent"
)
def test_fail_to_delete_by_other_user_without_write_permission(
    env_description_file,
):
    pass


@scenario("Read and write to regular file")
def test_read_write(env_description_file):
    pass


@scenario("Read right after write by other client")
def test_read_right_after_write(env_description_file):
    pass


@scenario("Read right after write by other client while file is open")
def test_read_right_after_write_while_file_is_open(env_description_file):
    pass


@scenario("Fail to read regular file without read permission")
def test_read_without_permission(env_description_file):
    pass


@scenario("Write to regular file with write permission")
def test_write_with_permission(env_description_file):
    pass


@scenario("Fail to write to regular file without write permission")
def test_write_without_permission(env_description_file):
    pass


@scenario("Execute file with execute permission")
def test_execute_with_permission(env_description_file):
    pass


@scenario("Fail to execute file without execute permission")
def test_execute_without_permission(env_description_file):
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


@scenario("Delete file opened by other user for reading")
def test_delete_file_opened_for_reading(env_description_file):
    pass


@scenario("Delete file opened by other user for reading and writing")
def test_delete_file_opened_for_rdwr(env_description_file):
    pass


@scenario("Fail to delete file without permission, file is opened by other user")
def test_delete_opened_file_without_permission(env_description_file):
    pass


@scenario("Delete file right after closing it")
def test_delete_right_after_close(env_description_file):
    pass


@scenario("Create many children")
def test_create_many(env_description_file):
    pass


@scenario("Create nonempty file then copy it and remove source file")
def test_copy_delete(env_description_file):
    pass


@scenario("Create nonempty file then move it to another space")
def test_move_between_spaces(env_description_file):
    pass
