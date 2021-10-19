"""Utils to facilitate data operations in Oneprovider using REST API.
"""

__author__ = "Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json
from datetime import datetime
from functools import partial

import pytest
import yaml

from tests.gui.utils.generic import parse_seq
from cdmi_client import ContainerApi, DataObjectApi
from cdmi_client.rest import ApiException as CdmiException
from oneprovider_client import BasicFileOperationsApi
from oneprovider_client import FilePathResolutionApi
from oneprovider_client.rest import ApiException as OPException
from tests.mixed.oneprovider_client.api.dataset_api import DatasetApi
from tests.mixed.utils.common import *
from tests.mixed.utils.data import (check_files_tree, create_content,
                                    assert_ace, get_acl_metadata)
from tests.utils.acceptance_utils import time_attr, compare
from tests.utils.http_exceptions import HTTPError
from tests.mixed.oneprovider_client import QoSApi


def _lookup_file_id(path, user_client_op):
    resolve_file_path_api = FilePathResolutionApi(user_client_op)
    file_id = resolve_file_path_api.lookup_file_id(path).file_id
    return file_id


def _read_file(path, user, users, provider, hosts):
    cli = login_to_cdmi(user, users, hosts[provider]['hostname'])
    dao = DataObjectApi(cli)
    return dao.read_data_object(path)


def _list_files(path, user, users, provider, hosts):
    user_client_op = login_to_provider(user, users,
                                       hosts[provider]['hostname'])
    file_api = BasicFileOperationsApi(user_client_op)
    file_id = _lookup_file_id(path, user_client_op)
    return [file.name for file in file_api.list_children(file_id).children]


def assert_file_content_in_op_rest(path, text, user, users, provider, hosts):
    file_content = _read_file(path, user, users, provider, hosts)
    assert_msg = ('Expected file named {} content to be '
                  '{} but found {}'.format(path, text, file_content))
    assert file_content == text, assert_msg


def assert_space_content_in_op_rest(user, users, hosts, config, space_name,
                                    spaces, host):
    children = _list_files(space_name, user, users, host, hosts)
    cwd = '/' + space_name
    ls_fun = partial(_list_files, user=user, users=users, provider=host,
                     hosts=hosts)
    assert_file_content_fun = partial(assert_file_content_in_op_rest,
                                      user=user, users=users, provider=host,
                                      hosts=hosts)
    check_files_tree(yaml.load(config), children, cwd, ls_fun,
                     assert_file_content_fun)


def assert_num_of_files_in_path_in_op_rest(num, path, user, users, host,
                                           hosts):
    user_client_op = login_to_provider(user, users, hosts[host]['hostname'])
    file_api = BasicFileOperationsApi(user_client_op)
    file_id = _lookup_file_id(path, user_client_op)
    children = file_api.list_children(file_id).children
    assert_msg = ('Expected exactly {} items in {} but found '
                  '{} items'.format(num, path, len(children)))
    assert num == len(children), assert_msg


def create_dir_in_op_rest(user, users, host, hosts, path, result):
    client = login_to_cdmi(user, users, hosts[host]['hostname'])

    c_api = ContainerApi(client)
    if result == 'fails':
        with pytest.raises(CdmiException, message='Creating dir did not fail'):
            c_api.create_container(path)
    else:
        c_api.create_container(path)


def remove_dir_in_op_rest(user, users, host, hosts, path):
    client = login_to_cdmi(user, users, hosts[host]['hostname'])

    c_api = ContainerApi(client)
    c_api.delete_container(path)


def create_file_in_op_rest(user, users, host, hosts, path, result,
                           access_token=None, identity_token=None):
    client = login_to_cdmi(user, users, hosts[host]['hostname'],
                           access_token=access_token,
                           identity_token=identity_token)

    do_api = DataObjectApi(client)
    if result == 'fails':
        with pytest.raises(CdmiException, message='Creating file did not fail'):
            do_api.create_data_object(path, '')
    else:
        do_api.create_data_object(path, '')


def remove_file_in_op_rest(user, users, host, hosts, path, result):
    client = login_to_cdmi(user, users, hosts[host]['hostname'])

    do_api = DataObjectApi(client)
    if result == 'fails':
        with pytest.raises(CdmiException,
                           message='Removing file did not fail'):
            do_api.delete_data_object(path)
    else:
        do_api.delete_data_object(path)


def see_items_in_op_rest(user, users, host, hosts, path_list, result, space):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    file_api = BasicFileOperationsApi(client)
    for path in parse_seq(path_list):
        path = '{}/{}'.format(space, path)
        check_if_item_exists_or_not_exists(result, path, client, file_api)


def see_item_in_op_rest_using_token(user, name, space, host,
                                    tmp_memory, users, hosts, result):
    path = f'{space}/{name}'
    access_token = tmp_memory[user]['mailbox'].get('token', None)
    client = login_to_provider(user, users, hosts[host]['hostname'],
                               access_token=access_token)
    file_api = BasicFileOperationsApi(client)
    check_if_item_exists_or_not_exists(result, path, client, file_api)


def check_if_item_id_in_items(path, client, file_api):
    file_id = _lookup_file_id(path, client)
    file_api.list_children(file_id)


def check_if_item_exists_or_not_exists(result, path, client, file_api):
    if result == 'fails':
        with pytest.raises(OPException,
                           message=f'There is item {path}'):
            check_if_item_id_in_items(path, client, file_api)
    else:
        check_if_item_id_in_items(path, client, file_api)


def create_directory_structure_in_op_rest(user, users, hosts, host, config, 
                                          space):
    items = yaml.load(config)
    cwd = space
    create_content(user, users, cwd, items, create_item_in_op_rest, host,
                   hosts)


def create_item_in_op_rest(user, users, cwd, name, content, create_item_fun,
                           host, hosts):
    if name.startswith('dir'):
        create_dir_in_op_rest(user, users, host, hosts,
                              '{}/{}'.format(cwd, name), '')
    else:
        create_file_in_op_rest(user, users, host, hosts,
                               '{}/{}'.format(cwd, name), '')
    if not content:
        return
    cwd += '/' + name
    create_content(user, users, cwd, content, create_item_fun, host, hosts)


def assert_ace_in_op_rest(user, users, host, hosts, cdmi, numerals, path, num,
                          priv, item_type, name):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    ace = client.read_metadata(path)['metadata']['cdmi_acl'][numerals[num]]
    assert_ace(priv, item_type, ace, name, num, path)


def grant_acl_privileges_in_op_rest(user, users, host, hosts, cdmi, path, priv,
                                    item_type, name, groups):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    try:
        acl = client.read_metadata(path)['metadata']['cdmi_acl']
    except KeyError:
        acl = []
    acl = get_acl_metadata(acl, priv, item_type, groups, name, users, path)
    client.write_metadata(path, {'cdmi_acl': acl})


def assert_metadata_in_op_rest(user, users, host, hosts, cdmi, path, tab_name, 
                               val):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    metadata = client.read_metadata(path)['metadata']
    if tab_name.lower() == 'basic':
        (attr, val) = val.split('=')
        assert attr in metadata, f'{path} has no {attr} {tab_name} metadata'
        assert val == metadata[attr], (f'{path} has no {attr} = {val} '
                                       f'{tab_name}')
    else:        
        metadata = metadata[f'onedata_{tab_name.lower()}']
        if 'onedata_base64' in metadata:
            import base64
            metadata = metadata['onedata_base64']
            metadata = base64.b64decode(metadata.encode('ascii')).decode(
                'ascii')

        if tab_name.lower() == 'json':
            assert val == json.dumps(metadata), (f'{path} has no {val} {tab_name} '
                                                 f'metadata but "{metadata}"')
        else:
            assert val == metadata, (f'{path} has no {val} {tab_name} '
                                     f'metadata but "{metadata}"')


def set_metadata_in_op_rest(user, users, host, hosts, cdmi, path, tab_name, 
                            val):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    if tab_name == 'basic':
        (attr, val) = val.split('=')
    else:
        attr = 'onedata_{}'.format(tab_name.lower())
        if tab_name.lower() == 'json':
            val = json.loads(val)
    client.write_metadata(path, {attr: val})
    

def remove_all_metadata_in_op_rest(user, users, host, hosts, cdmi, path):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    client.write_metadata(path, {})


def assert_no_such_metadata_in_op_rest(user, users, host, hosts, cdmi, path, 
                                       tab_name, val):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    metadata = client.read_metadata(path)['metadata']
    if tab_name == 'basic':
        attr, val = val.split('=')
    else:
        attr = 'onedata_{}'.format(tab_name.lower())
    try:
        metadata = metadata[attr]
    except KeyError:
        pass
    else:
        if tab_name.lower() == 'json':
            val = json.loads(val)
            for key in val:
                assert (key not in metadata or
                        metadata[key] != val[key]), ('There is {} {} metadata'
                                                     .format(val, tab_name))
        else:
            assert val != metadata, 'There is {} {} metadata'.format(val, 
                                                                     tab_name)


def write_to_file_in_op_rest(user, users, host, hosts, cdmi, path,
                             text, offset=0):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    client.write_to_file(path, text, offset)


def append_to_file_in_op_rest(user, users, host, hosts, cdmi, path,
                              text):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    metadata = client.read_metadata(path)['metadata']
    try:
        file_size = int(metadata['cdmi_size'])
    except KeyError:
        assert False, 'File {} has no size metadata'.format(path)
    else:
        client.write_to_file(path, text, file_size)


def move_item_in_op_rest(src_path, dst_path, result, cdmi, host, hosts, user,
                         users):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    if result == 'fails':
        with pytest.raises(HTTPError):
            client.move_item(src_path, dst_path)
    else:
        client.move_item(src_path, dst_path)


def move_item_in_op_rest_using_token(src_path, dst_path, result, host, hosts,
                                     user, users, tmp_memory, cdmi):
    access_token = tmp_memory[user]['mailbox'].get('token', None)
    client = cdmi(hosts[host]['hostname'], access_token)
    if result == 'fails':
        with pytest.raises(HTTPError):
            client.move_item(src_path, dst_path)
    else:
        client.move_item(src_path, dst_path)


def copy_item_in_op_rest(src_path, dst_path, cdmi, host, hosts, user,
                         users):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    client.copy_item(src_path, dst_path)


def assert_posix_permissions_in_op_rest(path, perms, user, users, host, hosts):
    user_client_op = login_to_provider(user, users,
                                       hosts[host]['hostname'])
    file_api = BasicFileOperationsApi(user_client_op)
    file_id = _lookup_file_id(path, user_client_op)
    file_attrs = file_api.get_attrs(file_id, attribute='mode')
    try:
        file_perms = int(file_attrs.mode) % 1000
    except KeyError:
        assert False, 'File {} has no mode metadata'.format(path)

    assert file_perms == int(perms), ('Expected file POSIX permissions '
                                      'for {} to be {} but got {}'
                                      .format(path, perms, file_perms))


def set_posix_permissions_in_op_rest(path, perm, user, users, host, hosts,
                                     result):
    user_client_op = login_to_provider(user, users,
                                       hosts[host]['hostname'])
    file_api = BasicFileOperationsApi(user_client_op)
    file_id = _lookup_file_id(path, user_client_op)

    if result == 'fails':
        with pytest.raises(OPException):
            file_api.set_attr(file_id, attribute={'mode': perm})
    else:
        file_api.set_attr(file_id, attribute={'mode': perm})


def assert_files_time_relation_in_op_rest(path, path2, time1_name, time2_name,
                                          comparator, host, hosts, user,
                                          users, cdmi):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    metadata1 = client.read_metadata(path)['metadata']
    metadata2 = client.read_metadata(path2)['metadata']
    attr1 = time_attr(time1_name, 'cdmi')
    attr2 = time_attr(time2_name, 'cdmi')
    date_fmt = '%Y-%m-%dT%H:%M:%SZ'

    try:
        time1 = datetime.strptime(metadata1[attr1], date_fmt)
        time2 = datetime.strptime(metadata2[attr2], date_fmt)
    except KeyError as ex:
        assert False, 'File {} has no {} metadata'.format(path, ex.args[0])

    assert compare(time1, time2, comparator), ('Time comparison failed. \n'
                                               'Time1: {} = {} \n'
                                               'Time2: {} = {} \n'
                                               'Comparator: {}'
                                               .format(time1_name, time1,
                                                       time2_name, time2,
                                                       comparator))


def assert_time_relation_in_op_rest(path, time1_name, time2_name,
                                    comparator, host, hosts, user, users, cdmi):
    assert_files_time_relation_in_op_rest(path, path, time1_name, time2_name,
                                          comparator, host, hosts, user,
                                          users, cdmi)


def create_qos_requirement_in_op_rest(user, users, hosts, host, expression,
                                      space_name, file_name):
    path = f'{space_name}/{file_name}'
    client = login_to_provider(user, users, hosts[host]['hostname'])
    qos_api = QoSApi(client)
    file_id = _lookup_file_id(path, client)
    data = {
            "fileId": file_id,
            "expression": expression
            }
    qos_api.add_qos_requirement(data)


def assert_qos_file_status_in_op_rest(user, users, hosts, host, space_name,
                                      file_name, option):
    path = f'{space_name}/{file_name}'
    client = login_to_provider(user, users, hosts[host]['hostname'])
    qo_s_api = QoSApi(client)
    file_id = _lookup_file_id(path, client)
    qos = qo_s_api.get_file_qos_summary(file_id).to_dict()['requirements']
    if not qos and option == 'has some':
        raise Exception('there is no qos file status for "{file_name}" in space'
                        ' "{space_name}"')
    elif qos and option == 'has not':
        raise Exception('there is qos file status for "{file_name}" in space'
                        ' "{space_name}"')


def delete_qos_requirement_in_op_rest(user, users, hosts, host, space_name,
                                      file_name):
    path = f'{space_name}/{file_name}'
    client = login_to_provider(user, users, hosts[host]['hostname'])
    qo_s_api = QoSApi(client)
    file_id = _lookup_file_id(path, client)
    qos = qo_s_api.get_file_qos_summary(file_id).to_dict()['requirements']
    for qos_id in qos:
        qo_s_api.remove_qos_requirement(qos_id)


def create_dataset_in_op_rest(user, users, hosts, host, space_name, item_name,
                              option):
    path = f'{space_name}/{item_name}'
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    file_id = _lookup_file_id(path, client)
    data = {"rootFileId": f"{file_id}"}
    if ' data' in option:
        data["protectionFlags"] = ["data_protection"]
    if 'metadata' in option:
        if "protectionFlags" in data:
            data["protectionFlags"].append("metadata_protection")
        else:
            data["protectionFlags"] = ["metadata_protection"]
    dataset_api.establish_dataset(data)


def assert_dataset_for_item_in_op_rest(user, users, hosts, host, space_name,
                                       item_name, spaces, option):
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
    data = ' data'
    metadata = ' metadata'
    if data in option:
        err_msg = 'dataset does not have data protection flag'
        data_flag = 'data_protection'
        assert data_flag in dataset_info.protection_flags, err_msg
    if metadata in option:
        err_msg = 'dataset does not have metadata protection flag'
        metadata_flag = 'metadata_protection'
        assert metadata_flag in dataset_info.protection_flags, err_msg


def check_if_item_in_dataset_structure(datasets, item_name, dataset_api,
                                       check_children=False,
                                       item_subtree=None):
    for dataset in datasets.datasets:
        if dataset.name == item_name:
            if check_children:
                check_children_of_dataset_in_op_rest(dataset, dataset_api,
                                                     item_subtree)
            break
    else:
        raise Exception(f'There is no dataset for item {item_name}')


def check_children_of_dataset_in_op_rest(dataset, dataset_api, item_subtree):
    for child in item_subtree:
        try:
            [(child_name, child_subtree)] = child.items()
            dataset_id = dataset.dataset_id
            dataset_children = dataset_api.list_dataset_children(dataset_id)
            check_children = True
            check_if_item_in_dataset_structure(dataset_children, child_name,
                                               dataset_api,
                                               check_children=check_children,
                                               item_subtree=child_subtree)

        except AttributeError:
            dataset_id = dataset.dataset_id
            dataset_children = dataset_api.list_dataset_children(dataset_id)
            check_if_item_in_dataset_structure(dataset_children, child,
                                               dataset_api)


def check_dataset_structure_in_op_rest(user, users, hosts, host, spaces,
                                       space_name, config):
    subtree = yaml.load(config)
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    space_id = f'{spaces[space_name]}'
    state = 'attached'
    for item in subtree:
        [(item_name, item_subtree)] = item.items()
        datasets = dataset_api.list_space_top_datasets(space_id, state)
        check_children = True
        check_if_item_in_dataset_structure(datasets, item_name,
                                           dataset_api,
                                           check_children=check_children,
                                           item_subtree=item_subtree)


def check_effective_protection_flags_for_file_in_op_rest(user, users, hosts,
                                                         host, item_name,
                                                         option):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    dataset_api = DatasetApi(client)
    if 'space1' not in item_name:
        item_name = "/space1/" + item_name
    file_id = _lookup_file_id(item_name, client)
    summary = dataset_api.get_file_dataset_summary(file_id)
    data = ' data'
    metadata = 'metadata'
    if data in option:
        kind = 'data_protection'
        err_msg = f'No data protection flag for {item_name}'
        assert kind in summary.effective_protection_flags, err_msg

    if metadata in option:
        kind = 'metadata_protection'
        err_msg = f'No matadata protection flag for {item_name}'
        assert kind in summary.effective_protection_flags, err_msg


def set_protection_flags_for_dataset_in_op_rest(user, users, hosts, host,
                                                item_name, option, spaces,
                                                space_name):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    toggle_data = ' data'
    toggle_metadata = 'metadata'
    data = {"setProtectionFlags": []}
    if toggle_data in option:
        data["setProtectionFlags"].append("data_protection")
    if toggle_metadata in option:
        data["setProtectionFlags"].append("metadata_protection")
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    dataset_api.update_dataset(dataset_id, data)


def check_effective_protection_flags_for_dataset_in_op_rest(user, users, hosts,
                                                            host, item_name,
                                                            option, spaces,
                                                            space_name):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    data = ' data'
    metadata = 'metadata'
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    dataset_information = dataset_api.get_dataset(dataset_id)

    if data in option:
        kind = 'data_protection'
        err_msg = f'No data protection flag for {item_name}'
        assert kind in dataset_information.effective_protection_flags, err_msg
    if metadata in option:
        kind = 'metadata_protection'
        err_msg = f'No metadata protection flag for {item_name}'
        assert kind in dataset_information.effective_protection_flags, err_msg


def detach_dataset_in_op_rest(user, users, hosts, host, item_name, spaces,
                              space_name):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    data = {'state': "detached"}
    dataset_api = DatasetApi(client)
    dataset_id = get_dataset_id(item_name, spaces, space_name, dataset_api)
    dataset_api.update_dataset(dataset_id, data)


def assert_dataset_detached_in_op_rest(user, users, hosts, host, item_name, spaces, space_name):
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

