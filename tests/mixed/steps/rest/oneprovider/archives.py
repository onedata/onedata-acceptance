"""Utils to facilitate archives operations in Oneprovider using REST API.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml
import time

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import transform
from tests.mixed.oneprovider_client.api.basic_file_operations_api import (
    BasicFileOperationsApi)
from tests.mixed.steps.rest.oneprovider.data import _lookup_file_id
from tests.mixed.steps.rest.oneprovider.datasets import get_dataset_id
from tests.mixed.utils.common import *
from tests.mixed.oneprovider_client.api.archive_api import ArchiveApi
from tests.mixed.oneprovider_client.api.dataset_api import DatasetApi
from oneprovider_client.rest import ApiException as OPException
from tests.utils.utils import repeat_failed


def translate_config_for_archive(config, tmp_memory):
    for item in config:
        if isinstance(config[item], str):
            config[item] = config[item].lower()
    if 'create nested archives' in config:
        del config['create nested archives']
        config['createNestedArchives'] = 'true'
    if 'include DIP' in config:
        del config['include DIP']
        config['includeDip'] = 'true'
    if 'incremental' in config and config['incremental']['basedOn']:
        config['incremental']['basedOn'] = tmp_memory[config[
            'incremental']['basedOn']]


def create_archive_in_op_rest(user, users, hosts, host, space_name, item_name,
                              config, spaces, tmp_memory, option):

    config = yaml.load(config)
    translate_config_for_archive(config, tmp_memory)
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    archive_api = ArchiveApi(client)
    data = {'datasetId': dataset_id, 'config': config}
    if 'description' in config:
        description = config['description']
        del config['description']
        data['description'] = description
    else:
        description = 'latest_created_archive'
    if option == 'succeeds':
        tmp_memory[description] = archive_api.create_archive(
            data).archive_id
    elif option == 'fails':
        try:
            archive_api.create_archive(data).archive_id
            raise Exception(
                'function: create_archive worked but it should not')
        except OPException as err:
            if err.status == 400:
                pass
            else:
                raise OPException


def assert_archive_in_op_rest(user, users, hosts, host, space_name, item_name,
                              spaces, tmp_memory, option, description):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    archive_api = ArchiveApi(client)
    dataset_archive = archive_api.list_dataset_archives(dataset_id)
    archive_id = tmp_memory[description]
    if option == 'sees':
        for archive in dataset_archive.archives:
            if archive == archive_id:
                break
        else:
            raise Exception(f'Archive for item {item_name} not found')
    else:
        for archive in dataset_archive.archives:
            if archive == archive_id:
                raise Exception(f'Archive for item {item_name} found')
        else:
            pass


def assert_number_of_archive_in_op_rest(user, users, hosts, host, space_name,
                                        item_name, spaces, number):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    archive_api = ArchiveApi(client)
    dataset_archive = archive_api.list_dataset_archives(dataset_id)
    number_of_archives = len(dataset_archive.archives)
    err_msg = (f'number of archives {number_of_archives}, '
               f'expected number of archives: {number}')
    assert int(number) == number_of_archives, err_msg


def remove_archive_in_op_rest(user, users, hosts, host, description,
                              tmp_memory, option):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    if option == 'succeeds':
        archive_api.delete_archive(archive_id)
    elif option == 'fails':
        try:
            archive_api.delete_archive(archive_id)
            raise Exception(
                'removing archive worked but it should not')
        except OPException as err:
            if err.status == 400:
                pass
            else:
                raise OPException


def get_archive_info(user, users, hosts, host, tmp_memory, description):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    return archive_api.get_archive(archive_id)


def assert_archive_with_option_in_op_rest(user, users, hosts, host, option,
                                          tmp_memory, description):
    info = get_archive_info(user, users, hosts, host, tmp_memory, description)
    err_msg = f'archive is not {option}'
    if transform(option) == 'bagit':
        assert info.config.layout == transform(option), err_msg
    elif transform(option) == 'dip':
        assert info.config.include_dip, err_msg


def assert_base_archive_for_archive_in_op_rest(user, users, hosts, host,
                                               tmp_memory, description,
                                               base_description):
    info = get_archive_info(user, users, hosts, host, tmp_memory, description)
    err_msg = (f'Base archive: {info.base_archive_id} does not match expected '
               f'archive {tmp_memory[base_description]}')
    assert tmp_memory[base_description] == info.base_archive_id, err_msg


@wt(parsers.re('using REST, (?P<user>.+?) changes archive description to '
               '"(?P<new_description>.*)" for archive with description '
               '"(?P<description>.*)" for item "(?P<item_name>.*)" in space '
               '"(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_archive_description_in_op_rest(user, users, hosts, host, tmp_memory,
                                          description, new_description):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    data = {"description": new_description}
    archive_api.update_archive(archive_id, data)
    tmp_memory[new_description] = archive_id
    del tmp_memory[description]


@wt(parsers.re('using REST, (?P<user>.+?) changes archive (?P<option>.*) '
               'callback to "(?P<new_callback>.*)" for archive with '
               'description "(?P<description>.*)" for item "(?P<item_name>.*)" '
               'in space "(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_archive_callback(user, users, hosts, host, tmp_memory, description,
                            option, new_callback):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    data = {f"{option}Callback": new_callback}
    archive_api.update_archive(archive_id, data)


def assert_archive_callback_in_op_rest(user, users, hosts, host, tmp_memory,
                                       description, option, expected_callback):
    info = get_archive_info(user, users, hosts, host, tmp_memory, description)
    callback = f'{option}_callback'
    err_msg = (f'callback {getattr(info, callback)} does '
               f'not match expected: {expected_callback}')
    if getattr(info, callback) is None:
        assert expected_callback == 'None', err_msg
    else:
        assert getattr(info, callback) == expected_callback, err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def recall_archive_for_archive_in_op_rest(user, users, hosts, host, tmp_memory,
                                          description, name, space_name,
                                          spaces):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    space_id = spaces[space_name]
    file_api = BasicFileOperationsApi(client)
    parent_id = file_api.get_attrs(space_id).file_id
    data = {"parentDirectoryId": parent_id, "targetFileName": name}
    archive_api.recall_archive(archive_id, data)


def recalled_archive_details_in_op_rest(user, users, hosts, host, data,
                                        name, space_name, spaces):

    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_api = ArchiveApi(client)
    path = f'{space_name}/{name}'
    file_id = _lookup_file_id(path, client)
    recall_details = archive_api.get_archive_recall_details(file_id)
    dataset_api = DatasetApi(client)

    err_msg = ('{key} for archive recall "{name}" is {value} '
               'but expected value is {expected_value} ')
    dataset_id = get_dataset_id(data['dataset'], spaces, space_name,
                                dataset_api)
    dataset = recall_details.dataset_id
    expected_files = int(data["files_recalled"].split(' / ')[0])
    files = recall_details.total_file_count
    expected_data = int(data["data_recalled"].split(' / ')[0].replace('B', ''))
    data = recall_details.total_byte_size

    assert dataset == dataset_id, err_msg.format(
        key="dataset", name=name, value=dataset, expected_value=dataset_id)

    assert files == expected_files, err_msg.format(
        key="files recalled", name=name, value=files,
        expected_value=expected_files)

    assert data == data, err_msg.format(
        key="data recalled", name=name, value=data,
        expected_value=expected_data)

    assert recall_details.finish_time >= recall_details.start_time, (
        f'archive recall "{name}" finish time is not greater or equal recall '
        f'start time')


def assert_progress_of_recall_in_op_rest(user, name, space_name, host,
                                         hosts, users, config):
    data = yaml.load(config)
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_api = ArchiveApi(client)
    path = f'{space_name}/{name}'
    file_id = _lookup_file_id(path, client)
    # waits for recall to start
    time.sleep(0.01)
    recall_progress = archive_api.get_archive_recall_progress(file_id)
    bytes_copied = recall_progress.bytes_copied
    expected_bytes_copied = int(data['bytes copied'].split()[-1])
    files_copied = recall_progress.files_copied
    expected_files_copied = int(data['files copied'].split()[-1])
    assert bytes_copied <= expected_bytes_copied, (
        f'Bytes copied:{bytes_copied} are not <= expected bytes '
        f'copied:{expected_bytes_copied}')
    assert files_copied <= expected_files_copied, (
        f'Files copied:{files_copied} are not <= expected files '
        f'copied:{expected_files_copied}')


def cancel_archive_for_archive_in_op_rest(user, users, hosts, host,
                                          space_name, target_name):

    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_api = ArchiveApi(client)
    path = f'{space_name}/{target_name}'
    file_id = _lookup_file_id(path, client)
    archive_api.cancel_archive_recall(file_id)

