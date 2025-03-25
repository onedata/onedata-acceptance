"""This module contains tests of shares and handles operations after environment upgrade"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import filecmp
import io
import os
import shutil
import tarfile
import time
from functools import partial

from tests.upgrade.utils.rest import (
    create_archive,
    create_share,
    download_file_content,
    establish_dataset,
    get_archive_information,
    get_handle,
    get_share_info,
    list_handle_services,
    list_handles,
    lookup_file_id,
    register_handle,
)
from tests.upgrade.utils.upgrade_utils import UpgradeTest


def get_tests(tests_controller):
    return [
        UpgradeTest(
            "rest shares test",
            partial(setup1, tests_controller),
            partial(verify1, tests_controller),
        ),
        UpgradeTest(
            "rest shares handles and archives test",
            partial(setup2, tests_controller),
            partial(verify2, tests_controller),
        ),
    ]


def convert_bytes_and_unpack_tar(raw_bytes, path):
    if os.path.exists(path):
        shutil.rmtree(path)
    tar_bytes = io.BytesIO(raw_bytes)
    with tarfile.open(fileobj=tar_bytes, mode="r:") as tar:
        tar.extractall(path)


SHARES_ID = {}


def setup1(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    prov_version = tests_controller.test_config["initialVersions"]["oneprovider"]
    try:
        prov_version = int(prov_version.split(".")[0])
    except ValueError:
        # version is develop, so it is current enough
        prov_version = 100

    client = tests_controller.mount_client("user1", "oneclient-1", "client11")
    space_path = client.absolute_path("space_posix")
    client.mkdir(os.path.join(space_path, "dir1_shared"))
    client.create_file(os.path.join(space_path, "file1_shared"))

    file_id = lookup_file_id("space_posix/file1_shared", provider_host, token)
    share_id = create_share(provider_host, token, file_id, prov_version)
    SHARES_ID["file1_shared"] = share_id

    file_id = lookup_file_id("space_posix/dir1_shared", provider_host, token)
    share_id = create_share(provider_host, token, file_id, prov_version)
    SHARES_ID["dir1_shared"] = share_id
    # sleep is necessary as events are processed asynchronously and there is possible race
    # between client unmounting (which is done after the setup) and processing all its events
    # by provider.
    time.sleep(10)


def setup2(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    zone_host = tests_controller.hosts["onezone"]["hostname"]
    token = tests_controller.users["user1"].token
    admin_token = tests_controller.users["admin"].token
    prov_version = tests_controller.test_config["initialVersions"]["oneprovider"]
    try:
        prov_version = int(prov_version.split(".")[0])
    except ValueError:
        # version is develop, so it is current enough
        prov_version = 100
    if prov_version < 21:
        # provider api support managing datasets and archives from 21 version
        return

    client = tests_controller.mount_client("user1", "oneclient-1", "client11")
    space_path = client.absolute_path("space_posix")
    dir_path = os.path.join(space_path, "dir2_shared")
    client.mkdir(dir_path)
    client.create_file(os.path.join(dir_path, "file1"))
    client.create_file(os.path.join(dir_path, "file2"))
    client.create_file(os.path.join(dir_path, "file3"))
    client.write("abc1", os.path.join(dir_path, "file1"))
    client.write("abc2", os.path.join(dir_path, "file2"))
    client.write("abc3", os.path.join(dir_path, "file3"))

    file_id = lookup_file_id("space_posix/dir2_shared", provider_host, token)
    share_id = create_share(provider_host, token, file_id, prov_version)

    handle_service_id = list_handle_services(zone_host, admin_token)["handle_services"][
        0
    ]
    register_handle_config = {
        "handleServiceId": handle_service_id,
        "resourceType": "Share",
        "resourceId": share_id,
        "metadataPrefix": "oai_dc",
        "metadata": """<?xml version="1.0" encoding="utf-8"?>
<metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Test dataset</dc:title>
    <dc:creator>Jane Doe</dc:creator>
    <dc:subject>Test</dc:subject>
</metadata>""",
    }
    _ = register_handle(zone_host, admin_token, register_handle_config)

    dataset_id = establish_dataset(provider_host, token, file_id)["datasetId"]
    archive_id = create_archive(provider_host, token, dataset_id, "test")["archiveId"]

    client.create_file(os.path.join(dir_path, "file4"))
    client.create_file(os.path.join(dir_path, "file5"))
    client.create_file(os.path.join(dir_path, "file6"))
    client.write("abc4", os.path.join(dir_path, "file4"))
    client.write("abc5", os.path.join(dir_path, "file5"))
    client.write("abc6", os.path.join(dir_path, "file6"))

    config = {"config": {"incremental": {"enabled": True, "basedOn": archive_id}}}
    time.sleep(1)  # wait for archive creation
    archive_inc_id = create_archive(provider_host, token, dataset_id, "test", config)[
        "archiveId"
    ]
    root_dir_id = get_archive_information(provider_host, token, archive_inc_id)[
        "rootDirectoryId"
    ]
    share_id = create_share(provider_host, token, root_dir_id, prov_version)

    register_handle_config.update({"resourceId": share_id})
    _ = register_handle(zone_host, admin_token, register_handle_config)

    # sleep is necessary as events are processed asynchronously and there is possible race
    # between client unmounting (which is done after the setup) and processing all its events
    # by provider.
    time.sleep(10)


def verify1(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token

    share_details = get_share_info(provider_host, token, SHARES_ID["file1_shared"])
    assert share_details["name"] == "testShare"
    assert share_details["shareId"] == SHARES_ID["file1_shared"]
    assert share_details["rootFileType"] == "REG"

    share_details = get_share_info(provider_host, token, SHARES_ID["dir1_shared"])
    assert share_details["name"] == "testShare"
    assert share_details["shareId"] == SHARES_ID["dir1_shared"]
    assert share_details["rootFileType"] == "DIR"


def verify2(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    zone_host = tests_controller.hosts["onezone"]["hostname"]
    token = tests_controller.users["user1"].token
    admin_token = tests_controller.users["admin"].token
    prov_version = tests_controller.test_config["initialVersions"]["oneprovider"]
    try:
        prov_version = int(prov_version.split(".")[0])
    except ValueError:
        # version is develop, so it is current enough
        prov_version = 100
    if prov_version < 21:
        # provider api support managing datasets and archives from 21 version
        return

    handles = list_handles(zone_host, admin_token)["handles"]
    assert len(handles) == 2

    res = get_handle(zone_host, admin_token, handles[0])
    share_id = res["resourceId"]
    share_root_dir_id1 = get_share_info(provider_host, token, share_id)["rootFileId"]

    res = get_handle(zone_host, admin_token, handles[1])
    share_id = res["resourceId"]
    share_root_dir_id2 = get_share_info(provider_host, token, share_id)["rootFileId"]

    handle1_content = download_file_content(provider_host, token, share_root_dir_id1)
    handle2_content = download_file_content(provider_host, token, share_root_dir_id2)

    convert_bytes_and_unpack_tar(handle1_content, "downloaded_handle1")
    convert_bytes_and_unpack_tar(handle2_content, "downloaded_handle2")

    if os.listdir("downloaded_handle1")[0].startswith("archive"):
        path1 = os.path.join("downloaded_handle1", os.listdir("downloaded_handle1")[0])
        path2 = "downloaded_handle2"
    else:
        path1 = "downloaded_handle1"
        path2 = os.path.join("downloaded_handle2", os.listdir("downloaded_handle2")[0])
    path1 = os.path.join(path1, "dir2_shared")
    path2 = os.path.join(path2, "dir2_shared")

    comp_res = filecmp.dircmp(path1, path2)
    assert not comp_res.diff_files
    assert not comp_res.left_only
    assert not comp_res.right_only
