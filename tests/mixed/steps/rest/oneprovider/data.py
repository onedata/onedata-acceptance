"""Utils to facilitate data operations in Oneprovider using REST API.
"""

__author__ = "Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from datetime import datetime
from functools import partial

import pytest
import yaml

from tests import OP_REST_PORT
from tests.gui.utils.generic import parse_seq
from cdmi_client import ContainerApi, DataObjectApi
from cdmi_client.rest import ApiException as CdmiException
from oneprovider_client import BasicFileOperationsApi
from oneprovider_client import FilePathResolutionApi
from oneprovider_client import SpaceApi
from oneprovider_client import ShareApi
from oneprovider_client.rest import ApiException as OPException
from tests.mixed.utils.common import *
from tests.mixed.utils.data import (check_files_tree, create_content,
                                    assert_ace, get_acl_metadata)
from tests.utils.acceptance_utils import time_attr, compare
from tests.utils.http_exceptions import HTTPError
from tests.utils.rest_utils import http_post, get_provider_rest_path


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
    check_files_tree(yaml.load(config, yaml.Loader), children, cwd, ls_fun,
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
        with pytest.raises(CdmiException):
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
        with pytest.raises(CdmiException):
            do_api.create_data_object(path, '')
    else:
        do_api.create_data_object(path, '')


def remove_file_in_op_rest(user, users, host, hosts, path, result):
    client = login_to_cdmi(user, users, hosts[host]['hostname'])

    do_api = DataObjectApi(client)
    if result == 'fails':
        with pytest.raises(CdmiException):
            do_api.delete_data_object(path)
    else:
        do_api.delete_data_object(path)


def remove_file_using_token_in_op_rest(user, users, host, hosts, path, result,
                                       tmp_memory):
    access_token = tmp_memory[user]['mailbox'].get('token', None)
    client = login_to_cdmi(user, users, hosts[host]['hostname'],
                           access_token=access_token)
    do_api = DataObjectApi(client)
    if result == 'fails':
        with pytest.raises(CdmiException):
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
        with pytest.raises(OPException):
            check_if_item_id_in_items(path, client, file_api)
    else:
        check_if_item_id_in_items(path, client, file_api)


def create_directory_structure_in_op_rest(user, users, hosts, host, config, 
                                          space, request):
    items = yaml.load(config, yaml.Loader)
    cwd = space
    create_content(user, users, cwd, items, create_item_in_op_rest, host,
                   hosts, request)


def create_item_in_op_rest(user, users, cwd, name, content, create_item_fun,
                           host, hosts, request):
    if name.startswith('dir'):
        create_dir_in_op_rest(user, users, host, hosts,
                              '{}/{}'.format(cwd, name), '')
    else:
        create_file_in_op_rest(user, users, host, hosts,
                               '{}/{}'.format(cwd, name), '')
    if not content:
        return
    cwd += '/' + name
    create_content(user, users, cwd, content, create_item_fun, host, hosts, request)


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
    file_attrs = file_api.get_attrs(file_id, data={'attributes': ['posix_permissions']})
    try:
        file_perms = int(file_attrs.posix_permissions) % 1000
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


def get_time_for_file_in_op_rest(path, user, users, cdmi, host, hosts,
                                 time_name):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    metadata = client.read_metadata(path)['metadata']
    attr = time_attr(time_name, 'cdmi')
    date_fmt = '%Y-%m-%dT%H:%M:%SZ'

    try:
        time = datetime.strptime(metadata[attr], date_fmt)
    except KeyError as ex:
        raise Exception(f'File {path} has no {ex.args[0]} metadata')

    return time


def compare_file_time_with_copied_time_in_op_rest(path, user, users, cdmi, host,
                                                  hosts, time_name1, time2,
                                                  comparator, time_name2):
    time1 = get_time_for_file_in_op_rest(path, user, users, cdmi, host, hosts,
                                         time_name1)
    err_msg = (f'Time comparison failed. \nTime1: {time_name1} = {time1} \n'
               f'Time2: {time_name2} = {time2} \nComparator: {comparator}')
    assert compare(time1, time2, comparator), err_msg


def assert_files_time_relation_in_op_rest(path, path2, time1_name, time2_name,
                                          comparator, host, hosts, user,
                                          users, cdmi):
    time1 = get_time_for_file_in_op_rest(path, user, users, cdmi, host, hosts,
                                         time1_name)
    time2 = get_time_for_file_in_op_rest(path2, user, users, cdmi, host, hosts,
                                         time2_name)

    err_msg = (f'Time comparison failed. \nTime1: {time1_name} = {time1} \n'
               f'Time2: {time2_name} = {time2} \nComparator: {comparator}')

    assert compare(time1, time2, comparator), err_msg


def assert_time_relation_in_op_rest(path, time1_name, time2_name,
                                    comparator, host, hosts, user, users, cdmi):
    assert_files_time_relation_in_op_rest(path, path, time1_name, time2_name,
                                          comparator, host, hosts, user,
                                          users, cdmi)


def upload_file_rest(users, user, hosts, host, path, file_name, parent_id):
    if path == '':
        data = None
    else:
        with open(path, 'rb') as f:
            data = f.read()
    provider_hostname = hosts[host]['hostname']
    # standard urllib2 cannot handle streaming bytes
    response = http_post(
        ip=provider_hostname, port=OP_REST_PORT,
        path=get_provider_rest_path('data', parent_id,
                                    f'children?name={file_name}'),
        headers={'X-Auth-Token': users[user].token,
                 'Content-Type': 'application/octet-stream'},
        data=data)


def get_space_details_rest(users, user, hosts, host, space_id):
    user_client_op = login_to_provider(user, users, hosts[host]['hostname'])
    space_api = SpaceApi(user_client_op)
    space_details = space_api.get_space(space_id)
    return space_details


def get_share_details_rest(users, user, hosts, host, share_id):
    user_client_op = login_to_provider(user, users, hosts[host]['hostname'])
    share_api = ShareApi(user_client_op)
    share_details = share_api.get_share(share_id)
    return share_details


def create_share_rest(users, user, hosts, host, file_id,  name):
    user_client_op = login_to_provider(user, users, hosts[host]['hostname'])
    share_api = ShareApi(user_client_op)
    share_id = share_api.create_share(data={
        "name": name,
        "rootFileId": file_id})
    return share_id


def remove_file_by_id_rest(users, user, hosts, host, file_id):
    user_client_op = login_to_provider(user, users, hosts[host]['hostname'])
    file_api = BasicFileOperationsApi(user_client_op)
    file_api.remove_file(file_id)


def create_empty_file_in_dir_rest(users, user, hosts, host, dir_id, name):
    upload_file_rest(users, user, hosts, host, '', name, dir_id)
