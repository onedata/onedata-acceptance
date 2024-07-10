"""This module contains gherkin steps to run acceptance tests featuring
basic operations on user root dir in Onezone using REST API.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.utils.bdd_utils import wt, parsers
from oneprovider_client.rest import ApiException
from tests.utils.http_exceptions import HTTPBadRequest
from tests.mixed.steps.rest.oneprovider.data import (
    get_space_details_rest, remove_file_by_id_rest,
    create_empty_file_in_dir_rest)
from tests.mixed.steps.rest.oneprovider.qos import create_qos_requirement_in_op_by_id_rest
from tests.mixed.steps.rest.oneprovider.datasets import create_dataset_in_op_by_id_rest
from tests.mixed.steps.rest.oneprovider.metadata import add_json_metadata_to_file_rest
from tests.mixed.steps.oneclient.data_basic import change_client_name_to_hostname
from tests.oneclient.steps.multi_dir_steps import try_to_delete_root_dir, try_to_move_root_dir
from tests.oneclient.steps.multi_file_steps import try_to_create_file_in_root_dir


@wt(parsers.parse('using REST, {user} gets root dir ID of space "{space_name}" '
                  'in {host}'))
def get_user_root_id(users, user, hosts, host, space_name, spaces, tmp_memory):
    space_details = get_space_details_rest(users, user, hosts,
                                           host, spaces[space_name])
    if tmp_memory['space_root_dir']:
        tmp_memory['space_root_dir'][space_name] = space_details.dir_id
    else:
        tmp_memory['space_root_dir'] = {space_name: space_details.dir_id}


@wt(parsers.parse('using {client}, {user} fails to remove user root dir of '
                  'space "{space_name}" in {host}'))
def try_to_remove_user_root_dir(client, users, user, hosts, host, space_name,
                                tmp_memory):
    if client.lower() == 'rest':
        try:
            remove_file_by_id_rest(users, user, hosts, host,
                               tmp_memory['space_root_dir'][space_name])
            raise Exception('Space root dir was deleted!')
        except ApiException as e:
            err_msg = 'Operation failed with POSIX error: eperm.'
            assert err_msg in str(e), f'Unexpected error occurred {e}'
    elif 'oneclient' in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            try_to_delete_root_dir(user, oneclient_host, users)
            raise Exception('Space root dir was deleted!')
        except PermissionError as e:
            assert 'Operation not permitted' in str(e)
    else:
        raise Exception(f'unknown client {client}')


@wt(parsers.parse('using {client}, {user} fails to create file "{file_name}" '
                  'in root dir of "{space_name}" in {host}'))
def try_to_create_file_in_user_root_dir(client, users, user, hosts, host,
                                        tmp_memory, space_name, file_name):
    if client.lower() == 'rest':
        try:
            create_empty_file_in_dir_rest(
                users, user, hosts, host, tmp_memory['space_root_dir'][space_name],
                file_name)
            raise Exception('file created in user root dir, but creation '
                            'should have failed')
        except ApiException:
            pass
    elif 'oneclient' in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            try_to_create_file_in_root_dir(user, oneclient_host, users, file_name)
            raise Exception('file created in user root dir, but creation '
                            'should have failed')
        except PermissionError as e:
            assert 'Operation not permitted' in str(e)


@wt(parsers.parse('using REST, {user} fails to add qos requirement '
                  '"{expression}" to user root dir of "{space_name}" in {host}'))
def try_to_create_qos_in_user_root_dir(user, users, hosts, host, tmp_memory,
                                       expression, space_name):
    try:
        create_qos_requirement_in_op_by_id_rest(
            user, users, hosts, host, expression,
            tmp_memory['space_root_dir'][space_name])
        raise Exception('qos requirement added to user root dir, but adding '
                        'should have failed')
    except ApiException:
        pass


@wt(parsers.parse('using REST, {user} fails to add json metadata '
                  '"{expression}" to user root dir of "{space_name}" in {host}'))
def try_to_create_json_metadata_in_user_root_dir(user, users, hosts, host,
                                                 tmp_memory, expression, space_name):
    try:
        add_json_metadata_to_file_rest(user, users, hosts, host, expression,
                                       tmp_memory['space_root_dir'][space_name])
        raise Exception('json metadata added to user root dir, but adding '
                        'should have failed')
    except ApiException:
        pass


@wt(parsers.parse('using REST, {user} fails to establish dataset to '
                  'user root dir of "{space_name}" in {host}'))
def try_to_establish_dataset_to_user_root_dir(user, users, hosts, host,
                                              tmp_memory, space_name):
    try:
        create_dataset_in_op_by_id_rest(user, users, hosts, host,
                                        tmp_memory['space_root_dir'][space_name], '')
        raise Exception('established dataset of user root dir, but establishing'
                        ' should have failed')
    except ApiException:
        pass


@wt(parsers.parse('using {client}, {user} fails to move '
                  'user root dir of "{space_name}" in {host}'))
def try_to_move_user_root_dir(client, user, users, hosts, host, tmp_memory,
                              space_name, cdmi):
    if client.lower() == 'rest':
        try:
            client = cdmi(hosts[host]['ip'], users[user].token)
            client.move_item_by_id(tmp_memory['space_root_dir'][space_name], '/new_name')
            raise Exception('moved user root dir, but moving '
                            'should have failed')
        except HTTPBadRequest as e:
            pass
    elif 'oneclient' in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            try_to_move_root_dir(user, oneclient_host, users, 'new_name')
            raise Exception('moved user root dir, but moving '
                            'should have failed')

        except PermissionError as e:
            assert 'Operation not permitted' in str(e)
    else:
        raise Exception(f'unknown client {client}')
