"""This module contains tests of shares, handles, datasets and archives operations
after environment upgrade"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import filecmp
import io
import os
import shutil
import tarfile
from functools import partial

from tests.upgrade.utils.rest import (
    create_archive,
    create_share,
    download_file_content,
    establish_dataset,
    get_archive_information,
    get_handle,
    get_share_info,
    lookup_file_id,
    register_handle,
)
from tests.upgrade.utils.upgrade_utils import UpgradeTest, get_prov_version
from tests.utils.utils import repeat_failed


def get_tests(tests_controller):
    return [
        UpgradeTest(
            "rest shares and handles test",
            partial(setup_shares_handles, tests_controller),
            partial(verify_shares_handles, tests_controller),
        ),
        UpgradeTest(
            "rest datasets and archives test",
            partial(setup_datasets_and_archives, tests_controller),
            partial(verify_datasets_and_archives, tests_controller),
        ),
        UpgradeTest(
            "rest all functionalities test",
            partial(setup_all_functionalities, tests_controller),
            partial(verify_all_functionalities, tests_controller),
        ),
    ]


def unpack_tarball_from_payload(raw_bytes, target_path):
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    tar_bytes = io.BytesIO(raw_bytes)
    with tarfile.open(fileobj=tar_bytes, mode="r:") as tar:
        tar.extractall(target_path)


SHARE_NAME_TO_ID = {}
HANDLE_NAME_TO_ID = {}
ARCHIVE_NAME_TO_ID = {}
RESULTS = {}


def setup_shares_handles(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    zone_host = tests_controller.hosts["onezone"]["hostname"]
    token = tests_controller.users["user1"].token
    admin_token = tests_controller.users["admin"].token

    client = tests_controller.get_client("user1", "oneclient-1", "client11")
    space_path = client.absolute_path("space_posix")
    client.mkdir(os.path.join(space_path, "dir1_shared"))
    dir_path = os.path.join(space_path, "dir1_shared")
    client.create_file(os.path.join(dir_path, "file1_shared"))

    file_id = lookup_file_id(
        "space_posix/dir1_shared/file1_shared", provider_host, token
    )
    SHARE_NAME_TO_ID["file1_shared"] = create_share(
        provider_host, token, file_id, "file1_shared"
    )
    file_id = lookup_file_id("space_posix/dir1_shared", provider_host, token)
    SHARE_NAME_TO_ID["dir1_shared"] = create_share(
        provider_host, token, file_id, "dir1_shared"
    )

    res = register_handle(zone_host, admin_token, SHARE_NAME_TO_ID["dir1_shared"])
    HANDLE_NAME_TO_ID["handle"] = res.headers["location"].split("/")[-1]
    wait_for_handle_registration(provider_host, token, SHARE_NAME_TO_ID["dir1_shared"])

    RESULTS["handle_details"] = get_handle(
        zone_host, admin_token, HANDLE_NAME_TO_ID["handle"]
    )
    RESULTS["share_details"] = get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["dir1_shared"]
    )
    share_root_dir_id = get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["dir1_shared"]
    )["rootFileId"]
    share_content = download_file_content(provider_host, token, share_root_dir_id)
    unpack_tarball_from_payload(share_content, "downloaded_share1_s")


def verify_shares_handles(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    zone_host = tests_controller.hosts["onezone"]["hostname"]
    token = tests_controller.users["user1"].token
    admin_token = tests_controller.users["admin"].token

    handle_details = get_handle(zone_host, admin_token, HANDLE_NAME_TO_ID["handle"])
    handle_details.pop("metadataPrefix")
    handle_details.pop("metadata")
    RESULTS["handle_details"].pop("metadata")
    assert RESULTS["handle_details"] == handle_details
    assert RESULTS["share_details"] == get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["dir1_shared"]
    )

    share_root_dir_id = get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["dir1_shared"]
    )["rootFileId"]
    share_content = download_file_content(provider_host, token, share_root_dir_id)
    unpack_tarball_from_payload(share_content, "downloaded_share1_v")
    compare_downloaded_dirs_content("downloaded_share1_s", "downloaded_share1_v")

    share_details = get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["file1_shared"]
    )
    assert share_details["name"] == "file1_shared"
    assert share_details["shareId"] == SHARE_NAME_TO_ID["file1_shared"]
    assert share_details["rootFileType"] == "REG"

    share_details = get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["dir1_shared"]
    )
    assert share_details["name"] == "dir1_shared"
    assert share_details["shareId"] == SHARE_NAME_TO_ID["dir1_shared"]
    assert share_details["rootFileType"] == "DIR"


def setup_datasets_and_archives(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token

    if not check_provider_supports_managing_datasets(provider_host):
        return

    client = tests_controller.get_client("user1", "oneclient-1", "client11")
    create_dir_with_example_content(client, "space_posix", "dir2_datasets")

    file_id = lookup_file_id("space_posix/dir2_datasets", provider_host, token)

    dataset_id = establish_dataset(provider_host, token, file_id)["datasetId"]
    ARCHIVE_NAME_TO_ID["archive"] = create_archive(
        provider_host, token, dataset_id, "test"
    )["archiveId"]
    root_dir_id = get_archive_information(
        provider_host, token, ARCHIVE_NAME_TO_ID["archive"]
    )["rootDirectoryId"]
    archive_content = download_file_content(provider_host, token, root_dir_id)
    unpack_tarball_from_payload(archive_content, "downloaded_archive_s")

    create_additional_content_in_dir(client, "space_posix", "dir2_datasets")

    archive_config = {
        "config": {
            "incremental": {"enabled": True, "basedOn": ARCHIVE_NAME_TO_ID["archive"]}
        }
    }
    ARCHIVE_NAME_TO_ID["archive_incremental"] = create_archive(
        provider_host, token, dataset_id, "test", archive_config
    )["archiveId"]
    root_dir_id = get_archive_information(
        provider_host, token, ARCHIVE_NAME_TO_ID["archive_incremental"]
    )["rootDirectoryId"]
    archive_inc_content = download_file_content(provider_host, token, root_dir_id)
    unpack_tarball_from_payload(archive_inc_content, "downloaded_archive_inc_s")


def verify_datasets_and_archives(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token

    if not check_provider_supports_managing_datasets(provider_host):
        return

    root_dir_id = get_archive_information(
        provider_host, token, ARCHIVE_NAME_TO_ID["archive"]
    )["rootDirectoryId"]
    archive_content = download_file_content(provider_host, token, root_dir_id)
    unpack_tarball_from_payload(archive_content, "downloaded_archive_v")

    root_dir_id = get_archive_information(
        provider_host, token, ARCHIVE_NAME_TO_ID["archive_incremental"]
    )["rootDirectoryId"]
    archive_inc_content = download_file_content(provider_host, token, root_dir_id)
    unpack_tarball_from_payload(archive_inc_content, "downloaded_archive_inc_v")
    compare_downloaded_dirs_content(
        "downloaded_archive_inc_s", "downloaded_archive_inc_v"
    )
    compare_downloaded_dirs_content("downloaded_archive_s", "downloaded_archive_v")


def setup_all_functionalities(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    zone_host = tests_controller.hosts["onezone"]["hostname"]
    token = tests_controller.users["user1"].token
    admin_token = tests_controller.users["admin"].token

    if not check_provider_supports_managing_datasets(provider_host):
        return

    client = tests_controller.get_client("user1", "oneclient-1", "client11")
    create_dir_with_example_content(client, "space_posix", "dir3_shared")

    file_id = lookup_file_id("space_posix/dir3_shared", provider_host, token)
    SHARE_NAME_TO_ID["dir3_shared"] = create_share(
        provider_host, token, file_id, "dir3_shared"
    )
    _ = register_handle(zone_host, admin_token, SHARE_NAME_TO_ID["dir3_shared"])

    dataset_id = establish_dataset(provider_host, token, file_id)["datasetId"]
    archive_id = create_archive(provider_host, token, dataset_id, "test")["archiveId"]

    create_additional_content_in_dir(client, "space_posix", "dir3_shared")

    archive_config = {
        "config": {"incremental": {"enabled": True, "basedOn": archive_id}}
    }
    archive_inc_id = create_archive(
        provider_host, token, dataset_id, "test", archive_config
    )["archiveId"]
    root_dir_id = get_archive_information(provider_host, token, archive_inc_id)[
        "rootDirectoryId"
    ]
    SHARE_NAME_TO_ID["dir3_archive_incremental"] = create_share(
        provider_host, token, root_dir_id, "dir3_archive_incremental"
    )
    _ = register_handle(
        zone_host, admin_token, SHARE_NAME_TO_ID["dir3_archive_incremental"]
    )

    share_root_dir_id = get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["dir3_shared"]
    )["rootFileId"]
    share_content = download_file_content(provider_host, token, share_root_dir_id)
    unpack_tarball_from_payload(share_content, "downloaded_dir3_shared_s")

    share_root_dir_id = get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["dir3_archive_incremental"]
    )["rootFileId"]
    share_content = download_file_content(provider_host, token, share_root_dir_id)
    unpack_tarball_from_payload(share_content, "downloaded_dir3_archive_incremental_s")


def verify_all_functionalities(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    if not check_provider_supports_managing_datasets(provider_host):
        return

    share_root_dir_id = get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["dir3_shared"]
    )["rootFileId"]
    share_content = download_file_content(provider_host, token, share_root_dir_id)
    unpack_tarball_from_payload(share_content, "downloaded_dir3_shared_v")

    share_root_dir_id = get_share_info(
        provider_host, token, SHARE_NAME_TO_ID["dir3_archive_incremental"]
    )["rootFileId"]
    share_content = download_file_content(provider_host, token, share_root_dir_id)
    unpack_tarball_from_payload(share_content, "downloaded_dir3_archive_incremental_v")

    compare_downloaded_dirs_content(
        "downloaded_dir3_shared_s", "downloaded_dir3_shared_v"
    )
    compare_downloaded_dirs_content(
        "downloaded_dir3_archive_incremental_s", "downloaded_dir3_archive_incremental_v"
    )

    archive_name = os.listdir("downloaded_dir3_archive_incremental_s")[0]
    path1 = os.path.join("downloaded_dir3_shared_s", "dir3_shared")
    path2 = os.path.join(
        "downloaded_dir3_archive_incremental_s", archive_name, "dir3_shared"
    )

    compare_downloaded_dirs_content(path1, path2)


def compare_downloaded_dirs_content(path1, path2):
    comp_res = filecmp.dircmp(path1, path2)
    comp_report = "\n".join(
        [
            f"Differences in common files: {comp_res.diff_files}",
            f"Files only in {path1}: {comp_res.left_only}",
            f"Files only in {path2}: {comp_res.right_only}",
        ]
    )
    # assert differences in common files
    assert not comp_res.diff_files, comp_report
    # assert presence of files existing only in left path
    assert not comp_res.left_only, comp_report
    # assert presence of files existing only in right path
    assert not comp_res.right_only, comp_report
    # recursively check common directories
    if any(comp_res.common_dirs):
        for common_dir in comp_res.common_dirs:
            compare_downloaded_dirs_content(
                os.path.join(path1, common_dir), os.path.join(path2, common_dir)
            )


@repeat_failed(timeout=30)
def wait_for_handle_registration(provider_host, token, share_id):
    res = get_share_info(provider_host, token, share_id)
    assert res["handleId"] is not None


def check_provider_supports_managing_datasets(provider_host):
    prov_version = get_prov_version(provider_host)
    # provider api supports managing datasets and archives from 21 version
    return prov_version >= 21


def create_dir_with_example_content(client, space_name: str, dir_name: str):
    space_path = client.absolute_path(space_name)
    dir_path = os.path.join(space_path, dir_name)
    client.mkdir(dir_path)
    client.create_file(os.path.join(dir_path, "file1"))
    client.create_file(os.path.join(dir_path, "file2"))
    client.create_file(os.path.join(dir_path, "file3"))
    client.write("abc1", os.path.join(dir_path, "file1"))
    client.write("abc2", os.path.join(dir_path, "file2"))
    client.write("abc3", os.path.join(dir_path, "file3"))


def create_additional_content_in_dir(client, space_name: str, dir_name: str):
    space_path = client.absolute_path(space_name)
    dir_path = os.path.join(space_path, dir_name)
    client.create_file(os.path.join(dir_path, "file4"))
    client.create_file(os.path.join(dir_path, "file5"))
    client.create_file(os.path.join(dir_path, "file6"))
    client.write("abc4", os.path.join(dir_path, "file4"))
    client.write("abc5", os.path.join(dir_path, "file5"))
    client.write("abc6", os.path.join(dir_path, "file6"))


@repeat_failed(timeout=60)
def wait_for_synced_file_content(provider_host, path, token, expected_content):
    file_id = lookup_file_id(path, provider_host, token)
    actual_content = str(
        download_file_content(provider_host, token, file_id), encoding="utf-8"
    )
    assert (
        actual_content == expected_content
    ), f"expected content: {expected_content} but got {actual_content}"
