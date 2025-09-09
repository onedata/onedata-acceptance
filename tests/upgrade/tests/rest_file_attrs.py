"""This module contains tests of shares, handles, datasets and archives operations
after environment upgrade"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from functools import partial

from tests.upgrade.utils.rest_utils import (
    get_directory_size_statistics,
    get_file_attributes,
    lookup_file_id,
)
from tests.upgrade.utils.upgrade_utils import UpgradeTest
from tests.utils.utils import repeat_failed

TIMEOUT_FOR_UPDATING_FILE_ATTRS = 15

SPACE_NAME = "space_posix"

TEXT = "example"

ALL_ATTRS = [
    "fileId",
    "index",
    "type",
    "activePermissionsType",
    "posixPermissions",
    "acl",
    "name",
    "conflictingName",
    "path",
    "parentFileId",
    "displayGid",
    "displayUid",
    "atime",
    "mtime",
    "ctime",
    "size",
    "isFullyReplicatedLocally",
    "localReplicationRate",
    "originProviderId",
    "directShareIds",
    "ownerUserId",
    "hardlinkCount",
    "symlinkValue",
    "effProtectionFlags",
    "effDatasetProtectionFlags",
    "effDatasetInheritancePath",
    "effQosInheritancePath",
    "aggregateQosStatus",
    "archiveRecallRootFileId",
    "hasCustomMetadata",
    "xattr.key",
]  # excluded hasJsonMetadata, jsonMetadata, creationTime


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
    create_example_content_in_space(client)

    file_id = lookup_file_id(f"{SPACE_NAME}/file_attrs", provider_host, token)
    _wait_for_file_attrs(
        partial(get_file_attributes, provider_host, token, file_id, ALL_ATTRS),
        len(TEXT),
    )
    RESULTS["file attrs setup"] = get_file_attributes(
        provider_host, token, file_id, ALL_ATTRS
    )
    # breakpoint()

    file_id = lookup_file_id(f"{SPACE_NAME}/file_attrs_hardlink", provider_host, token)
    RESULTS["file attrs hardlink setup"] = get_file_attributes(
        provider_host, token, file_id, ALL_ATTRS
    )

    file_id = lookup_file_id(f"{SPACE_NAME}/file_attrs_symlink", provider_host, token)
    RESULTS["file attrs symlink setup"] = get_file_attributes(
        provider_host, token, file_id, ALL_ATTRS
    )

    file_id = lookup_file_id(f"{SPACE_NAME}/dir_stats", provider_host, token)
    RESULTS["dir stats"] = get_directory_size_statistics(
        provider_host, token, file_id, "layout"
    )


def verify_metadata(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token

    file_id = lookup_file_id(f"{SPACE_NAME}/file_attrs", provider_host, token)
    compare_attrs(
        RESULTS["file attrs setup"],
        get_file_attributes(provider_host, token, file_id, ALL_ATTRS),
    )

    file_id = lookup_file_id(f"{SPACE_NAME}/file_attrs_hardlink", provider_host, token)
    compare_attrs(
        RESULTS["file attrs hardlink setup"],
        get_file_attributes(provider_host, token, file_id, ALL_ATTRS),
    )

    file_id = lookup_file_id(f"{SPACE_NAME}/file_attrs_symlink", provider_host, token)
    compare_attrs(
        RESULTS["file attrs symlink setup"],
        get_file_attributes(provider_host, token, file_id, ALL_ATTRS),
    )

    file_id = lookup_file_id(f"{SPACE_NAME}/dir_stats", provider_host, token)
    assert RESULTS["dir stats"] == get_directory_size_statistics(
        provider_host, token, file_id, "layout"
    )


def create_example_content_in_space(client):
    space_path = client.absolute_path(SPACE_NAME)
    file_path = os.path.join(space_path, "file_attrs")
    client.create_file(file_path)
    client.write(TEXT, file_path)
    link_path = os.path.join(space_path, "file_attrs_hardlink")
    client.create_hardlink(file_path, link_path)
    link_path = os.path.join(space_path, "file_attrs_symlink")
    client.create_symlink(file_path, link_path)

    dir_path = os.path.join(space_path, "dir_stats")
    client.mkdir(dir_path)


def compare_attrs(old_attrs, new_attrs):
    for attr in old_attrs:
        err_msg = (
            f"Attr: {attr} is different after upgrade. Attrs before"
            f" upgrade:\n{old_attrs}.\nAttrs after upgrade:\n{new_attrs}."
        )
        if attr in ATTRS_MAP:
            assert old_attrs[attr] == new_attrs[ATTRS_MAP[attr]], err_msg
        else:
            assert old_attrs[attr] == new_attrs[attr], err_msg


@repeat_failed(timeout=TIMEOUT_FOR_UPDATING_FILE_ATTRS)
def _wait_for_file_attrs(query, ex_size):
    res = query()
    assert res["size"] == ex_size
