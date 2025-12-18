"""This module contains tests of file attributes operations
after environment upgrade"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 onedata.org"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from functools import partial

from tests.gui.utils.generic import FileAttr
from tests.upgrade.utils.rest_utils import (
    get_directory_size_statistics,
    get_file_attributes,
    lookup_file_id,
)
from tests.upgrade.utils.upgrade_utils import UpgradeTest, is_prov_version_lower_than
from tests.utils.utils import repeat_failed

TIMEOUT_FOR_UPDATING_FILE_ATTRS = 15

SPACE_NAME = "space_posix"

TEXT = "example"

ALL_ATTRS = [
    attr.value
    for attr in FileAttr
    if attr.value not in ("hasJsonMetadata", "jsonMetadata")
]  # excluded hasJsonMetadata, jsonMetadata as they are available since 25.0

ATTRS_MAP = {
    "file_id": "fileId",
    "mode": "posixPermissions",
    "parent_id": "parentFileId",
    "storage_group_id": "displayGid",
    "storage_user_id": "displayUid",
    "is_fully_replicated": "isFullyReplicatedLocally",
    "provider_id": "originProviderId",
    "shares": "directShareIds",
    "owner_id": "ownerUserId",
    "hardlinks_count": "hardlinkCount",
}


RESULTS = {}

REG_NAME = "file_attrs"
HARDLINK_NAME = "file_attrs_hardlink"
SYMLINK_NAME = "file_attrs_symlink"
DIR_NAME = "dir_stats"


def get_tests(tests_controller):
    return [
        UpgradeTest(
            "rest file attrs test",
            partial(setup_metadata, tests_controller),
            partial(verify_metadata, tests_controller),
        )
    ]


def setup_metadata(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    client = tests_controller.get_client("user1", "oneclient-1", "client11")

    # create file, hardlink and symlink
    create_example_content_in_space(client, tests_controller)

    file_id = lookup_file_id(f"{SPACE_NAME}/{REG_NAME}", provider_host, token)
    _wait_for_file_size_attr(
        provider_host,
        token,
        file_id,
        len(TEXT),
    )
    RESULTS["regular_file_attrs_setup"] = get_file_attributes(
        provider_host, token, file_id, ALL_ATTRS
    )

    if not is_prov_version_lower_than(tests_controller.initial_prov_version, "21.02.1"):

        file_id = lookup_file_id(f"{SPACE_NAME}/{HARDLINK_NAME}", provider_host, token)
        RESULTS["file_attrs_hardlink_setup"] = get_file_attributes(
            provider_host, token, file_id, ALL_ATTRS
        )

        file_id = lookup_file_id(f"{SPACE_NAME}/{SYMLINK_NAME}", provider_host, token)
        RESULTS["file_attrs_symlink_setup"] = get_file_attributes(
            provider_host, token, file_id, ALL_ATTRS
        )

    if not is_prov_version_lower_than(tests_controller.initial_prov_version, "21.02.5"):
        file_id = lookup_file_id(f"{SPACE_NAME}/{DIR_NAME}", provider_host, token)
        RESULTS["dir_stats_setup"] = get_directory_size_statistics(
            provider_host, token, file_id, "layout"
        )


def verify_metadata(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token

    file_id = lookup_file_id(f"{SPACE_NAME}/{REG_NAME}", provider_host, token)
    compare_attrs(
        RESULTS["regular_file_attrs_setup"],
        get_file_attributes(provider_host, token, file_id, ALL_ATTRS),
        tests_controller,
    )

    if not is_prov_version_lower_than(tests_controller.initial_prov_version, "21.02.1"):

        file_id = lookup_file_id(f"{SPACE_NAME}/{HARDLINK_NAME}", provider_host, token)
        compare_attrs(
            RESULTS["file_attrs_hardlink_setup"],
            get_file_attributes(provider_host, token, file_id, ALL_ATTRS),
            tests_controller,
        )

        file_id = lookup_file_id(f"{SPACE_NAME}/{SYMLINK_NAME}", provider_host, token)
        compare_attrs(
            RESULTS["file_attrs_symlink_setup"],
            get_file_attributes(provider_host, token, file_id, ALL_ATTRS),
            tests_controller,
        )

    if not is_prov_version_lower_than(tests_controller.initial_prov_version, "21.02.5"):
        file_id = lookup_file_id(f"{SPACE_NAME}/{DIR_NAME}", provider_host, token)
        assert RESULTS["dir_stats_setup"] == get_directory_size_statistics(
            provider_host, token, file_id, "layout"
        )


def create_example_content_in_space(client, tests_controller):
    space_path = client.absolute_path(SPACE_NAME)
    file_path = os.path.join(space_path, REG_NAME)
    client.create_file(file_path)
    client.write(TEXT, file_path)
    if not is_prov_version_lower_than(tests_controller.initial_prov_version, "21.02.1"):
        link_path = os.path.join(space_path, HARDLINK_NAME)
        client.create_hardlink(file_path, link_path)
        link_path = os.path.join(space_path, SYMLINK_NAME)
        client.create_symlink(file_path, link_path)

    dir_path = os.path.join(space_path, DIR_NAME)
    client.mkdir(dir_path)


def compare_attrs(old_attrs, new_attrs, tests_controller):
    for attr in old_attrs:
        err_msg = (
            f"Attr: {attr} is different after upgrade. Attrs before"
            f" upgrade:\n{old_attrs}.\nAttrs after upgrade:\n{new_attrs}."
        )
        if is_prov_version_lower_than(
            tests_controller.initial_prov_version, "21.02.01"
        ):
            val = format_attr_val(attr, old_attrs)
        else:
            val = old_attrs[attr]

        if attr in ATTRS_MAP:
            assert val == new_attrs[ATTRS_MAP[attr]], err_msg
        else:
            assert val == new_attrs[attr], err_msg


@repeat_failed(timeout=TIMEOUT_FOR_UPDATING_FILE_ATTRS)
def _wait_for_file_size_attr(provider_host, token, file_id, ex_size):
    res = get_file_attributes(provider_host, token, file_id, ["size"])
    assert res["size"] == ex_size


def format_attr_val(attr, old_attrs):
    if attr == "type":
        return old_attrs[attr].upper()
    if attr == "mode":
        return old_attrs[attr][1:]
    return old_attrs[attr]
