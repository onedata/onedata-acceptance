"""This module contains gherkin steps to run acceptance tests featuring
basic operations on special dirs in Onezone using REST API, oneclient.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import transform, parse_seq
from oneprovider_client.rest import ApiException
from tests.utils.http_exceptions import HTTPForbidden, HTTPBadRequest
from tests.mixed.steps.rest.oneprovider.data import (
    get_space_details_rest, remove_file_by_id_rest,
    create_empty_file_in_dir_rest, create_share_rest, get_share_details_rest)
from tests.mixed.steps.rest.oneprovider.qos import create_qos_requirement_in_op_by_id_rest
from tests.mixed.steps.rest.oneprovider.datasets import create_dataset_in_op_by_id_rest
from tests.mixed.steps.rest.oneprovider.metadata import add_json_metadata_to_file_rest
from tests.mixed.steps.oneclient.data_basic import change_client_name_to_hostname
from tests.oneclient.steps.multi_dir_steps import (
    try_to_delete_root_dir, try_to_move_root_dir, delete_dir_by_id, move_dir_by_id)
from tests.oneclient.steps.multi_file_steps import (
    try_to_create_file_in_root_dir, create_file_in_dir_by_id)


@wt(parsers.parse('using REST, {user} gets ID of the user root directory from '
                  'the space "{space_name}" details in {host}'))
def get_user_root_dir_id(users, user, hosts, host, space_name, spaces, tmp_memory):
    space_details = get_space_details_rest(users, user, hosts,
                                           host, spaces[space_name])
    if tmp_memory['user_root_dir']:
        tmp_memory['user_root_dir'][user] = space_details.dir_id
    else:
        tmp_memory['user_root_dir'] = {user: space_details.dir_id}


@wt(parsers.parse('using REST, {user} gets ID of the archives directory from '
                  'the space "{space_name}" details in {host}'))
def get_archives_dir_id(users, user, hosts, host, space_name, spaces, tmp_memory):
    space_details = get_space_details_rest(users, user, hosts,
                                           host, spaces[space_name])
    if tmp_memory['archives_dir']:
        tmp_memory['archives_dir'][user] = space_details.archives_dir_id
    else:
        tmp_memory['archives_dir'] = {user: space_details.archives_dir_id}


@wt(parsers.parse('using REST, {user} gets ID of the trash directory from '
                  'the space "{space_name}" details in {host}'))
def get_trash_dir_id(users, user, hosts, host, space_name, spaces, tmp_memory):
    space_details = get_space_details_rest(users, user, hosts,
                                           host, spaces[space_name])
    if tmp_memory['trash_dir']:
        tmp_memory['trash_dir'][user] = space_details.trash_dir_id
    else:
        tmp_memory['trash_dir'] = {user: space_details.trash_dir_id}


@wt(parsers.parse('using REST, {user} gets ID of the shares directory from '
                  'the share details in the space "{space_name}" in {host}'))
def get_shares_dir_id(users, user, hosts, host, space_name, spaces, tmp_memory):
    get_user_root_dir_id(users, user, hosts, host, space_name, spaces,
                         tmp_memory)
    share_id = create_share_rest(
        users, user, hosts, host, tmp_memory['user_root_dir'][user],
        'test_share').share_id
    share_details = get_share_details_rest(users, user, hosts, host, share_id)
    if tmp_memory['shares_dir']:
        tmp_memory['shares_dir'][user] = share_details.root_file_id
    else:
        tmp_memory['shares_dir'] = {user: share_details.root_file_id}


@wt(parsers.parse('using {client}, {user} fails to remove the {name} '
                  'directory in {host}'))
def try_to_remove_special_dir(client, users, user, hosts, host, tmp_memory, name):
    try_to_remove_special_dir_by_id(
        client, users, user, hosts, host, tmp_memory[f'{transform(name)}_dir'][user],
        err_msg=f'{name} dir was deleted!')


def try_to_remove_special_dir_by_id(client, users, user, hosts, host, dir_id,
                                    err_msg=''):
    if client.lower() == 'rest':
        try:
            remove_file_by_id_rest(users, user, hosts, host, dir_id)
            raise Exception(err_msg)
        except ApiException as e:
            ex_err_msg = 'Operation failed with POSIX error: eperm.'
            assert ex_err_msg in str(e), f'Unexpected error occurred {e}'
    elif 'oneclient' in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            delete_dir_by_id(user, oneclient_host, users, dir_id)
            raise Exception(err_msg)
        except PermissionError as e:
            assert 'Operation not permitted' in str(e)
    else:
        raise Exception(f'unknown client {client}')


@wt(parsers.parse('using {client}, {user} fails to remove the user root '
                  'directory using file path in {host}'))
def try_to_remove_user_root_dir_by_path(client, users, user):
    if 'oneclient' in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            try_to_delete_root_dir(user, oneclient_host, users)
            raise Exception('Space root dir was deleted!')
        except PermissionError as e:
            assert 'Operation not permitted' in str(e)
    else:
        raise Exception(f'unknown client {client}')


@wt(parsers.parse('using {client}, {user} fails to move the '
                  '{name} directory in {host}'))
def try_to_move_special_dir(client, user, users, hosts, host, tmp_memory,
                            cdmi, name):
    try_to_move_special_dir_by_id(
        client, user, users, hosts, host, tmp_memory[f'{transform(name)}_dir'][user],
        cdmi, err_msg=f'Moved {name} dir, but moving should have failed')


def try_to_move_special_dir_by_id(client, user, users, hosts, host, dir_id,
                                  cdmi, err_msg=None):
    if client.lower() == 'rest':
        try:
            client = cdmi(hosts[host]['ip'], users[user].token)
            client.move_item_by_id(dir_id, '/new_name')
            raise Exception(err_msg)
        except HTTPForbidden as e:
            ex_err_msg = 'Operation failed with POSIX error: eperm.'
            assert ex_err_msg in str(e), f'Unexpected error occurred {e}'
    elif 'oneclient' in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            move_dir_by_id(user, oneclient_host, users, dir_id, 'new_name')
            raise Exception(err_msg)
        except PermissionError as e:
            assert 'Operation not permitted' in str(e)
    else:
        raise Exception(f'unknown client {client}')


@wt(parsers.parse('using {client}, {user} fails to move the '
                  'user root directory using file path in {host}'))
def try_to_move_user_root_dir_by_path(client, user, users):
    if 'oneclient' in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            try_to_move_root_dir(user, oneclient_host, users, 'new_name')
            raise Exception('moved user root dir, but moving '
                            'should have failed')
        except PermissionError as e:
            assert 'Operation not permitted' in str(e)
    else:
        raise Exception(f'unknown client {client}')


@wt(parsers.parse('using {client}, {user} fails to create file "{file_name}" '
                  'in the {name} directory in {host}'))
def try_to_create_file_in_special_dir(client, users, user, hosts, host,
                                      tmp_memory, file_name, name):
    try_to_create_file_in_special_dir_by_id(
        client, users, user, hosts, host,
        tmp_memory[f'{transform(name)}_dir'][user], file_name,
        err_msg=f'File created in {name} dir, but creation should have failed')


def try_to_create_file_in_special_dir_by_id(client, users, user, hosts, host,
                                            dir_id, file_name, err_msg=''):
    if client.lower() == 'rest':
        try:
            create_empty_file_in_dir_rest(
                users, user, hosts, host, dir_id,
                file_name)
            raise Exception(err_msg)
        except ApiException as e:
            ex_err_msg = 'Operation failed with POSIX error: eperm.'
            assert ex_err_msg in str(e), f'Unexpected error occurred {e}'
    elif 'oneclient' in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            create_file_in_dir_by_id(user, oneclient_host, users, dir_id, file_name)
            raise Exception(err_msg)
        except PermissionError as e:
            assert 'Operation not permitted' in str(e)


@wt(parsers.parse('using {client}, {user} fails to create file "{file_name}" '
                  'in the user root directory using file path in {host}'))
def try_to_create_file_in_user_root_dir_by_path(client, users, user, file_name):
    if 'oneclient' in client.lower():
        try:
            oneclient_host = change_client_name_to_hostname(client.lower())
            try_to_create_file_in_root_dir(user, oneclient_host, users, file_name)
            raise Exception('file created in user root dir, but creation '
                            'should have failed')
        except PermissionError as e:
            assert 'Operation not permitted' in str(e)


@wt(parsers.parse('using REST, {user} fails to add QoS requirement '
                  '"{expression}" to the {name} directory in {host}'))
def try_to_add_qos_to_special_dir(user, users, hosts, host, tmp_memory,
                                  expression, name):
    try_to_add_qos_to_special_dir_by_id(
        user, users, hosts, host, tmp_memory[f'{transform(name)}_dir'][user], expression,
        err_msg=f'Qos requirement added to {name} dir, but adding '
                'should have failed')


def try_to_add_qos_to_special_dir_by_id(user, users, hosts, host, dir_id,
                                        expression, err_msg=''):
    try:
        create_qos_requirement_in_op_by_id_rest(
            user, users, hosts, host, expression,
            dir_id)
        raise Exception(err_msg)
    except ApiException as e:
        ex_err_msg = 'You are not authorized to perform this operation.'
        assert ex_err_msg in str(e)


@wt(parsers.parse('using REST, {user} fails to add json metadata '
                  '\'{expression}\' to the {name} directory in {host}'))
def try_to_add_json_metadata_to_special_dir(user, users, hosts, host,
                                            tmp_memory, expression, name):
    try_to_add_json_metadata_to_special_dir_by_id(
        user, users, hosts, host, tmp_memory[f'{transform(name)}_dir'][user], expression,
        err_msg=f'Json metadata added to {name} dir, but adding '
                'should have failed')


def try_to_add_json_metadata_to_special_dir_by_id(
        user, users, hosts, host, dir_id, expression, err_msg=''):
    try:
        add_json_metadata_to_file_rest(user, users, hosts, host, expression,
                                       dir_id)
        raise Exception(err_msg)
    except ApiException as e:
        ex_err_msg = 'You are not authorized to perform this operation.'
        assert ex_err_msg in str(e)


@wt(parsers.parse('using REST, {user} fails to establish dataset on the '
                  '{name} directory in {host}'))
def try_to_establish_dataset_on_special_dir(user, users, hosts, host,
                                            tmp_memory, name):
    try_to_establish_dataset_on_special_dir_by_id(
        user, users, hosts, host, tmp_memory[f'{transform(name)}_dir'][user],
        err_msg=f'Established dataset on {name} dir, but establishing should '
                'have failed')


def try_to_establish_dataset_on_special_dir_by_id(user, users, hosts, host,
                                                  dir_id, err_msg=''):
    try:
        create_dataset_in_op_by_id_rest(user, users, hosts, host,
                                        dir_id, '')
        raise Exception(err_msg)
    except ApiException as e:
        ex_err_msg = 'You are not authorized to perform this operation.'
        assert ex_err_msg in str(e)
