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
from tests.mixed.cdmi_client import ContainerApi, DataObjectApi
from tests.mixed.cdmi_client.rest import ApiException as CdmiException
from tests.mixed.oneprovider_client import BasicFileOperationsApi
from tests.mixed.oneprovider_client import FilePathResolutionApi
from tests.mixed.oneprovider_client.api_client import ApiException
from tests.mixed.oneprovider_client.rest import ApiException as OPException
from tests.mixed.utils.common import *
from tests.mixed.utils.data import (
    check_files_tree, create_content, assert_ace, get_acl_metadata)
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

        if result == 'fails':
            with pytest.raises(OPException, 
                               message='There is item {}'.format(path)):
                file_id = _lookup_file_id(path, client)
                file_api.list_children(file_id)
        else:
            file_id = _lookup_file_id(path, client)
            file_api.list_children(file_id)


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
        with pytest.raises(ApiException):
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
    qo_s_api = QoSApi(client)
    file_id = _lookup_file_id(path, client)
    data = {
            "fileId": file_id,
            "expression": expression
            }
    qo_s_api.add_qos_requirement(data)


def assert_qos_file_status_in_op_rest(user, users, hosts, host, space_name,
                                      file_name, option):
    path = f'{space_name}/{file_name}'
    client = login_to_provider(user, users, hosts[host]['hostname'])
    qo_s_api = QoSApi(client)
    file_id = _lookup_file_id(path, client)
    qos = qo_s_api.get_file_qos_summary(file_id).to_dict()['requirements']
    if not qos and option == 'sees':
        raise Exception('there is no qos file status for "{file_name}" in space'
                        ' "{space_name}"')
    elif qos and option == 'does not see':
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
