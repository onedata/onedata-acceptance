"""Utils to facilitate archives operations in Oneprovider using REST API.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import transform
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
    if 'incremental' in config:
        if config['incremental']['basedOn']:
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
    description = config['description']
    del config['description']
    data = {'datasetId': dataset_id, 'config': config,
            'description': description}
    if option == 'creates':
        tmp_memory[description] = archive_api.create_archive(
            data).archive_id
    elif option == 'fails to create':
        try:
            tmp_memory[description] = archive_api.create_archive(
                data).archive_id
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
    err_msg = (f'number of archives {len(dataset_archive.archives)} '
               f'expected number of archives: {number}')
    assert int(number) == len(dataset_archive.archives), err_msg


def remove_archive_in_op_rest(user, users, hosts, host, description,
                              tmp_memory, option):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    if option == 'removes':
        archive_api.purge_archive(archive_id)
    elif option == 'fails to remove':
        try:
            archive_api.purge_archive(archive_id)
            raise Exception(
                'function: create_archive worked but it should not')
        except OPException as err:
            if err.status == 400:
                pass
            else:
                raise OPException


def assert_archive_with_option_in_op_rest(user, users, hosts, host, option,
                                          tmp_memory, description):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    info = archive_api.get_archive(archive_id)
    err_msg = f'archive is not {option}'
    if transform(option) == 'bagit':
        assert info.config.layout == transform(option), err_msg
    elif transform(option) == 'dip':
        assert info.config.include_dip is True, err_msg


def assert_base_archive_for_archive_in_op_rest(user, users, hosts, host,
                                               tmp_memory, description,
                                               base_description):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    info = archive_api.get_archive(archive_id)
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
    data = {f"{option}callback": new_callback}
    archive_api.update_archive(archive_id, data)


@wt(parsers.re('using REST, (?P<user>.+?) sees that (?P<option>.*) callback'
               ' is "(?P<expected_callback>.*)" for archive with description '
               '"(?P<description>.*)" for item "(?P<item_name>.*)" '
               'in space "(?P<space_name>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_callback(user, users, hosts, host, tmp_memory, description,
                            option, expected_callback):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    archive_id = tmp_memory[description]
    archive_api = ArchiveApi(client)
    info = archive_api.get_archive(archive_id)
    callback = f'{option}_callback'
    if option == 'preserved':
        err_msg = (f'callback {getattr(info, callback)} does '
                   f'not match expected: {expected_callback}')
        if getattr(info, callback) is None:
            assert expected_callback == 'None', err_msg
        else:
            assert getattr(info, callback) == expected_callback, err_msg

