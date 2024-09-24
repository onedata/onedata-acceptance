"""Utils to facilitate datasets operations in Oneprovider using REST API.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from tests.gui.meta_steps.oneprovider.dataset import get_flags
from tests.mixed.steps.rest.oneprovider.data import _lookup_file_id
from tests.mixed.utils.common import *
from tests.mixed.oneprovider_client.api.dataset_api import DatasetApi
from oneprovider_client.rest import ApiException as OPException


def create_dataset_in_op_rest(user, users, hosts, host, space_name, item_name,
                              option):
    path = f'{space_name}/{item_name}'
    client = login_to_provider(user, users, hosts[host]['hostname'])
    file_id = _lookup_file_id(path, client)
    create_dataset_in_op_by_id_rest(user, users, hosts, host, file_id, option)


def create_dataset_in_op_by_id_rest(
        user, users, hosts, host, file_id, option):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    data = {"rootFileId": f"{file_id}"}
    flags = get_flags(option)
    if len(flags) != 0:
        data["protectionFlags"] = flags
    dataset_api.establish_dataset(data)


def fail_to_create_dataset_in_op_rest(user, users, hosts, host, space_name,
                                      item_name):
    try:
        option = ''
        create_dataset_in_op_rest(user, users, hosts, host, space_name,
                                  item_name,
                                  option)
        raise Exception('function: establish_dataset worked but it should not')
    except OPException as err:
        if err.status == 400:
            pass
        else:
            raise OPException


def assert_top_level_dataset_in_space_in_op_rest(user, users, hosts, host,
                                                 space_name, item_name, spaces,
                                                 option):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    space_id = f'{spaces[space_name]}'
    state = 'attached'
    datasets = dataset_api.list_space_top_datasets(space_id, state)
    if option == 'sees':
        for dataset in datasets.datasets:
            if dataset.name == item_name:
                break
        else:
            raise Exception(f'Dataset for item {item_name} not found')

    else:
        for dataset in datasets.datasets:
            if dataset.name == item_name:
                raise Exception(f'Dataset for item {item_name} found')


def get_dataset_id(item_name, spaces, space_name, dataset_api,
                   state='attached'):
    space_id = f'{spaces[space_name]}'
    datasets = dataset_api.list_space_top_datasets(space_id, state)
    if '/' in item_name:
        path_list = item_name.split('/')
        for dataset in datasets.datasets:
            if dataset.name == path_list[0]:
                dataset_id = dataset.dataset_id
                return get_dataset_child_id(path_list, dataset_id, dataset_api)
    else:
        for dataset in datasets.datasets:
            if dataset.name == item_name:
                return dataset.dataset_id


def get_dataset_child_id(path_list, dataset_id, dataset_api ):
    for item in path_list[1:]:
        dataset_children = dataset_api.list_dataset_children(dataset_id)
        for dataset in dataset_children.datasets:
            if dataset.name == item:
                dataset_id = dataset.dataset_id
                if item == path_list[-1]:
                    return dataset_id


def remove_dataset_in_op_rest(user, users, hosts, host, space_name, item_name,
                              spaces):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    dataset_api.remove_dataset(dataset_id)


def assert_write_protection_flag_for_dataset_op_rest(user, users, hosts, host,
                                                     space_name, item_name,
                                                     spaces, option):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    dataset_info = dataset_api.get_dataset(dataset_id)
    for flag in get_flags(option):
        err_msg = f'dataset does not have {flag} flag'
        assert flag in dataset_info.protection_flags, err_msg


def check_dataset_structure_in_op_rest(user, users, hosts, host, spaces,
                                       space_name, config):
    # function checks only if what is in config exists, does not
    # fail if there are more datasets
    subtree = yaml.load(config, yaml.Loader)
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    space_id = f'{spaces[space_name]}'
    state = 'attached'
    for item in subtree:
        [(excepted_dataset, excepted_dataset_subtree)] = item.items()
        datasets = dataset_api.list_space_top_datasets(space_id, state)
        for dataset in datasets.datasets:
            if dataset.name == excepted_dataset:
                check_structure_of_dataset_children_in_op_rest(
                                           dataset_api,
                                           dataset.dataset_id,
                                           excepted_dataset_subtree)
                break
        else:
            raise Exception(f'There is no dataset for item {excepted_dataset}')


def check_structure_of_dataset_children_in_op_rest(dataset_api, dataset_id,
                                                   excepted_datasets_subtree):
    for child in excepted_datasets_subtree:
        try:
            [(excepted_child_name, excepted_child_subtree)] = child.items()
        except AttributeError:
            excepted_child_name = child
            excepted_child_subtree = []
        dataset_children = dataset_api.list_dataset_children(dataset_id)
        for dataset in dataset_children.datasets:
            if dataset.name == excepted_child_name:
                check_structure_of_dataset_children_in_op_rest(
                    dataset_api, dataset.dataset_id, excepted_child_subtree)
                break
        else:
            raise Exception(f'There is no dataset for child item {excepted_child_name}')


def check_effective_protection_flags_for_file_in_op_rest(user, users, hosts,
                                                         host, item_name,
                                                         option, space_name):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    if space_name not in item_name:
        item_name = f"/{space_name}/" + item_name
    file_id = _lookup_file_id(item_name, client)
    summary = dataset_api.get_file_dataset_summary(file_id)
    for flag in get_flags(option):
        err_msg = f'dataset does not have {flag} flag for {item_name}'
        assert flag in summary.effective_protection_flags, err_msg


def set_protection_flags_for_dataset_in_op_rest(user, users, hosts, host,
                                                item_name, option, spaces,
                                                space_name):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    data = {"setProtectionFlags": get_flags(option)}
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    dataset_api.update_dataset(dataset_id, data)


def check_effective_protection_flags_for_dataset_in_op_rest(user, users, hosts,
                                                            host, item_name,
                                                            option, spaces,
                                                            space_name):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    dataset_info = dataset_api.get_dataset(dataset_id)
    for flag in get_flags(option):
        err_msg = f'dataset does not have {flag} flag for {item_name}'
        assert flag in dataset_info.effective_protection_flags, err_msg


def detach_dataset_in_op_rest(user, users, hosts, host, item_name, spaces,
                              space_name):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    data = {'state': "detached"}
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    dataset_api.update_dataset(dataset_id, data)


def assert_dataset_detached_in_op_rest(user, users, hosts, host, item_name,
                                       spaces, space_name):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    space_id = f'{spaces[space_name]}'
    state = 'detached'
    detached_datasets = dataset_api.list_space_top_datasets(space_id, state)
    for dataset in detached_datasets.datasets:
        if dataset.name == item_name:
            break
    else:
        raise Exception(f'Dataset for item {item_name} not found on detached'
                        f' view mode')


def reattach_dataset_in_op_rest(user, users, hosts, host, item_name, spaces,
                                space_name):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    data = {'state': "attached"}
    dataset_api = DatasetApi(client)
    state = 'detached'
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api,
                                state=state)
    dataset_api.update_dataset(dataset_id, data)

