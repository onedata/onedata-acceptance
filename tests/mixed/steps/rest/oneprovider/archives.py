"""Utils to facilitate archives operations in Oneprovider using REST API."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from collections.abc import Mapping, MutableMapping
from typing import NotRequired, Protocol, TypedDict, cast

import yaml
from oneprovider_client.rest import ApiException as OPException

from tests.conftest import Hosts, Users
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import transform
from tests.mixed.oneprovider_client.api.archive_api import ArchiveApi
from tests.mixed.oneprovider_client.api.basic_file_operations_api import (
    BasicFileOperationsApi,
)
from tests.mixed.oneprovider_client.api.dataset_api import DatasetApi
from tests.mixed.steps.rest.oneprovider.data import _lookup_file_id
from tests.mixed.steps.rest.oneprovider.datasets import get_dataset_id
from tests.mixed.utils.common import login_to_provider
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

IdMap = Mapping[str, str]
TmpMemory = MutableMapping[str, str]
ArchiveConfigValue = str | MutableMapping[str, str]
ArchiveConfig = dict[str, ArchiveConfigValue]


class ArchiveData(TypedDict):
    datasetId: str
    config: ArchiveConfig
    description: NotRequired[str]


class ArchiveInfoConfig(Protocol):
    layout: str
    include_dip: bool


class ArchiveInfo(Protocol):
    config: ArchiveInfoConfig
    base_archive_id: str


def translate_config_for_archive(config: ArchiveConfig, tmp_memory: TmpMemory) -> None:
    for item, value in list(config.items()):
        if isinstance(value, str):
            config[item] = value.lower()
    if "create nested archives" in config:
        del config["create nested archives"]
        config["createNestedArchives"] = "true"
    if "include DIP" in config:
        del config["include DIP"]
        config["includeDip"] = "true"
    incremental_config = config.get("incremental")
    if isinstance(incremental_config, MutableMapping) and incremental_config["basedOn"]:
        incremental_config["basedOn"] = tmp_memory[incremental_config["basedOn"]]


def create_archive_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    space_name: str,
    item_name: str,
    config: str,
    spaces: IdMap,
    tmp_memory: TmpMemory,
    option: str,
) -> None:

    archive_config = cast(ArchiveConfig, yaml.load(config, yaml.Loader))
    translate_config_for_archive(archive_config, tmp_memory)
    client = login_to_provider(user, users, hosts[host]["hostname"])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    archive_api = ArchiveApi(client)
    data: ArchiveData = {"datasetId": dataset_id, "config": archive_config}
    if "description" in archive_config:
        description = cast(str, archive_config.pop("description"))
        data["description"] = description
    else:
        description = "latest_created_archive"
    if option in ["succeeds", "tries"]:
        tmp_memory[description] = archive_api.create_archive(data).archive_id
    elif option == "fails":
        try:
            _ = archive_api.create_archive(data).archive_id
            raise AssertionError("function: create_archive worked but it should not")
        except OPException as err:
            if err.status == 400:
                pass
            else:
                raise OPException from err


def create_n_archives_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    space_name: str,
    item_name: str,
    config: str,
    spaces: IdMap,
    tmp_memory: TmpMemory,
    number: int,
) -> None:
    archive_config = cast(ArchiveConfig, yaml.load(config, yaml.Loader))
    translate_config_for_archive(archive_config, tmp_memory)
    client = login_to_provider(user, users, hosts[host]["hostname"])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    archive_api = ArchiveApi(client)
    data: ArchiveData = {"datasetId": dataset_id, "config": archive_config}

    for i in range(number):
        description = f"archive number {i}"
        data["description"] = description
        archive_api.create_archive(data)


def assert_archive_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    space_name: str,
    item_name: str,
    spaces: IdMap,
    tmp_memory: TmpMemory,
    option: str,
    description: str,
) -> None:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    archive_api = ArchiveApi(client)
    dataset_archive = archive_api.list_dataset_archives(dataset_id)
    archive_id = tmp_memory[description]
    if option == "sees":
        for archive in dataset_archive.archives:
            if archive == archive_id:
                break
        else:
            raise AssertionError(f"Archive for item {item_name} not found")
    else:
        for archive in dataset_archive.archives:
            if archive == archive_id:
                raise AssertionError(f"Archive for item {item_name} found")


def assert_number_of_archive_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    space_name: str,
    item_name: str,
    spaces: IdMap,
    number: int,
) -> None:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    archive_api = ArchiveApi(client)
    dataset_archive = archive_api.list_dataset_archives(dataset_id)
    number_of_archives = len(dataset_archive.archives)
    err_msg = (
        f"number of archives {number_of_archives}, "
        f"expected number of archives: {number}"
    )
    assert int(number) == number_of_archives, err_msg


def remove_archive_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    description: str,
    tmp_memory: TmpMemory,
    option: str,
) -> None:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    if option == "succeeds":
        archive_api.delete_archive(archive_id)
    elif option == "fails":
        try:
            archive_api.delete_archive(archive_id)
            raise AssertionError("removing archive worked but it should not")
        except OPException as err:
            if err.status == 400:
                pass
            else:
                raise OPException from err


def get_archive_info(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    description: str,
) -> ArchiveInfo:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    return cast(ArchiveInfo, archive_api.get_archive(archive_id))


def assert_archive_with_option_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    option: str,
    tmp_memory: TmpMemory,
    description: str,
) -> None:
    info = get_archive_info(user, users, hosts, host, tmp_memory, description)
    err_msg = f"archive is not {option}"
    if transform(option) == "bagit":
        assert info.config.layout == transform(option), err_msg
    elif transform(option) == "dip":
        assert info.config.include_dip, err_msg


def assert_base_archive_for_archive_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    description: str,
    base_description: str,
) -> None:
    info = get_archive_info(user, users, hosts, host, tmp_memory, description)
    err_msg = (
        f"Base archive: {info.base_archive_id} does not match expected "
        f"archive {tmp_memory[base_description]}"
    )
    assert tmp_memory[base_description] == info.base_archive_id, err_msg


@wt(
    parsers.re(
        "using REST, (?P<user>.+?) changes archive description to "
        '"(?P<new_description>.*)" for archive with description '
        '"(?P<description>.*)" for item "(?P<item_name>.*)" in space '
        '"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_archive_description_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    description: str,
    new_description: str,
) -> None:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    data = {"description": new_description}
    archive_api.update_archive(archive_id, data)
    tmp_memory[new_description] = archive_id
    del tmp_memory[description]


@wt(
    parsers.re(
        "using REST, (?P<user>.+?) changes archive (?P<option>.*) "
        'callback to "(?P<new_callback>.*)" for archive with '
        'description "(?P<description>.*)" for item "(?P<item_name>.*)" '
        'in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_archive_callback(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    description: str,
    option: str,
    new_callback: str,
) -> None:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    data = {f"{option}Callback": new_callback}
    archive_api.update_archive(archive_id, data)


def assert_archive_callback_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    description: str,
    option: str,
    expected_callback: str,
) -> None:
    info = get_archive_info(user, users, hosts, host, tmp_memory, description)
    callback = f"{option}_callback"
    err_msg = (
        f"callback {getattr(info, callback)} does "
        f"not match expected: {expected_callback}"
    )
    if getattr(info, callback) is None:
        assert expected_callback == "None", err_msg
    else:
        assert getattr(info, callback) == expected_callback, err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def recall_archive_for_archive_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    tmp_memory: TmpMemory,
    description: str,
    name: str,
    space_name: str,
    spaces: IdMap,
) -> None:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    space_id = spaces[space_name]
    file_api = BasicFileOperationsApi(client)
    parent_id = file_api.get_attrs(space_id).file_id
    data = {"parentDirectoryId": parent_id, "targetFileName": name}
    archive_api.recall_archive(archive_id, data)


def recalled_archive_details_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    data: Mapping[str, str],
    name: str,
    space_name: str,
    spaces: IdMap,
) -> None:

    client = login_to_provider(user, users, hosts[host]["hostname"])
    archive_api = ArchiveApi(client)
    path = f"{space_name}/{name}"
    file_id = _lookup_file_id(path, client)
    recall_details = archive_api.get_archive_recall_details(file_id)
    dataset_api = DatasetApi(client)

    err_msg = (
        '{key} for archive recall "{name}" is {value} '
        "but expected value is {expected_value} "
    )
    expected_dataset_id = get_dataset_id(
        data["dataset"], spaces, space_name, dataset_api
    )
    dataset_id = recall_details.dataset_id
    expected_files = int(data["files_recalled"].split(" / ")[0])
    files = recall_details.total_file_count
    expected_data = int(data["data_recalled"].split(" / ")[0].replace("B", ""))
    data = recall_details.total_byte_size

    assert dataset_id == expected_dataset_id, err_msg.format(
        key="dataset",
        name=name,
        value=dataset_id,
        expected_value=expected_dataset_id,
    )

    assert files == expected_files, err_msg.format(
        key="files recalled",
        name=name,
        value=files,
        expected_value=expected_files,
    )

    assert data == expected_data, err_msg.format(
        key="data recalled", name=name, value=data, expected_value=expected_data
    )

    assert (
        recall_details.finish_time >= recall_details.start_time
    ), f'archive recall "{name}" finish time is not greater or equal recall start time'


def assert_progress_of_recall_in_op_rest(
    user: str,
    name: str,
    space_name: str,
    host: str,
    hosts: Hosts,
    users: Users,
    config: str,
) -> None:
    data = cast(Mapping[str, str], yaml.load(config, yaml.Loader))
    client = login_to_provider(user, users, hosts[host]["hostname"])
    archive_api = ArchiveApi(client)
    path = f"{space_name}/{name}"
    file_id = _lookup_file_id(path, client)
    # waits for recall to start
    time.sleep(0.01)
    recall_progress = archive_api.get_archive_recall_progress(file_id)
    bytes_copied = recall_progress.bytes_copied
    expected_bytes_copied = int(data["bytes copied"].split()[-1])
    files_copied = recall_progress.files_copied
    expected_files_copied = int(data["files copied"].split()[-1])
    assert bytes_copied <= expected_bytes_copied, (
        f"Bytes copied:{bytes_copied} are not <= expected bytes "
        f"copied:{expected_bytes_copied}"
    )
    assert files_copied <= expected_files_copied, (
        f"Files copied:{files_copied} are not <= expected files "
        f"copied:{expected_files_copied}"
    )


def cancel_archive_for_archive_in_op_rest(
    user: str,
    users: Users,
    hosts: Hosts,
    host: str,
    space_name: str,
    target_name: str,
) -> None:

    client = login_to_provider(user, users, hosts[host]["hostname"])
    archive_api = ArchiveApi(client)
    path = f"{space_name}/{target_name}"
    file_id = _lookup_file_id(path, client)
    archive_api.cancel_archive_recall(file_id)
