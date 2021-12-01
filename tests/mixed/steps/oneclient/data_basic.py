"""This module contains implementation of mixed oneclient steps for data
management.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json
import os
from functools import partial

import yaml

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.utils.generic import parse_seq
from tests.mixed.utils.data import (
    check_files_tree, create_content, assert_ace, get_acl_metadata)
from tests.oneclient.steps import (
    multi_dir_steps, multi_reg_file_steps, multi_file_steps)
from tests.utils.acceptance_utils import failure
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


# because oneclient is not working without ls on mountpoint
def ls_on_mountpoint(users, user, oneclient_host):
    user1 = users[user]
    client = user1.clients[oneclient_host]
    path = client._mount_path
    client.ls(path=path)


def change_client_name_to_hostname(client_name):
    return client_name.replace('oneclient', 'client')


@wt(parsers.parse('{user} mounts oneclient using received token'))
def mount_new_oneclient_with_token(user, hosts, users, env_desc, tmp_memory):
    token = tmp_memory[user]['mailbox']['token']
    users[user].mount_client('oneclient-1', 'client1', hosts, env_desc, token)


def mount_new_oneclient_with_token_fail(user, hosts, users, env_desc, tmp_memory,
                                        client='oneclient'):
    if 'oneclient' in client:
        token = tmp_memory[user]['mailbox']['token']
        users[user].mount_client('oneclient-1', 'client1', hosts, env_desc, token)
        failure(user, users)


def mount_new_oneclient_result(user, hosts, users, env_desc, tmp_memory, result,
                               client='oneclient'):
    if result == 'succeeds':
        mount_new_oneclient_with_token(user, hosts, users, env_desc, tmp_memory)
    else:
        mount_new_oneclient_with_token_fail(user, hosts, users, env_desc,
                                            tmp_memory, client=client)


def create_dir_in_op_oneclient(user, full_path, users, result, host):
    if result == 'fails':
        multi_dir_steps.fail_to_create(user, full_path, host, users)
    else:
        multi_dir_steps.create(user, full_path, host, users)


def create_file_in_op_oneclient(user, path, users, result, host):
    if result == 'fails':
        multi_file_steps.create_reg_file_fail(user, path, host, users)
    else:
        multi_file_steps.create_reg_file(user, path, host, users)


def create_file_in_op_oneclient_with_tokens(user, hosts, users, env_desc, tmp_memory,
                                            result, full_path, client_lower):
    try:
        mount_new_oneclient_result(user, hosts, users, env_desc, tmp_memory, result,
                                   client='oneclient')

        # because oneclient is not working without ls on mountpoint
        ls_on_mountpoint(users, user, 'client1')

        if result == 'succeeds':
            oneclient_host = change_client_name_to_hostname(client_lower)
            create_file_in_op_oneclient(user, full_path, users, result,
                                        oneclient_host)
    except AssertionError as e:
        if result == 'fails':
            oneclient_host = change_client_name_to_hostname(client_lower)
            create_file_in_op_oneclient(user, full_path, users, result,
                                        oneclient_host)
        else:
            raise e


def see_items_in_op_oneclient(items, space, user, users, result, host):
    for item in parse_seq(items):
        last_elem_in_path = os.path.basename(item)
        if last_elem_in_path.startswith('dir'):
            full_path = '{}/{}'.format(space, item)
            if result == 'fails':
                multi_dir_steps.cannot_list_dir(user, full_path, host, users)
            else:
                multi_dir_steps.list_dir(user, full_path, host, users)
        else:
            if result == 'fails':
                multi_file_steps.stat_absent(user, space, item, host, users)
            else:
                multi_file_steps.stat_present(user, space, item, host, users)


def assert_num_of_files_in_path_in_op_oneclient(num, path, user, users, host):
    items = multi_dir_steps.list_dirs_base(user, path, host, users)
    assert_msg = ('Expected exactly {} items in {} but found '
                  '{} items'.format(num, path, len(items)))
    assert len(items) == num, assert_msg


def create_directory_structure_in_op_oneclient(user, users, config, space,
                                               host, hosts):
    items = yaml.load(config)
    cwd = space
    create_content(user, users, cwd, items, create_item_in_op_oneclient, host,
                   hosts)


def create_item_in_op_oneclient(user, users, cwd, name, content,
                                create_item_fun, host, hosts):
    if name.startswith('dir'):
        multi_dir_steps.create(user, '{}/{}'.format(cwd, name), host, users)
    else:
        multi_file_steps.create_reg_file(user, '{}/{}'.format(cwd, name), host,
                                         users)
    if not content:
        return
    cwd += '/' + name
    create_content(user, users, cwd, content, create_item_fun, host, hosts)


def assert_file_content_in_op_oneclient(path, text, user, users, host):
    multi_reg_file_steps.read_text(user, text, path, host, users)


def ls_dir_in_op_oneclient(path, user, users, host):
    return multi_dir_steps.list_dirs_base(user, path, host, users)


def assert_space_content_in_op_oneclient(config, space_name, user, users,
                                         host):
    children = ls_dir_in_op_oneclient(space_name, user, users, host)
    cwd = space_name
    ls_fun = partial(ls_dir_in_op_oneclient, user=user, users=users, host=host)
    assert_file_content_fun = partial(assert_file_content_in_op_oneclient,
                                      user=user, users=users, host=host)
    check_files_tree(yaml.load(config), children, cwd, ls_fun,
                     assert_file_content_fun)


def delete_empty_directory_in_op_oneclient(path, user, users, result, host):
    if result == 'fails':
        multi_dir_steps.fail_to_delete_empty(user, path, host, users)
    else:
        multi_dir_steps.delete_empty(user, path, host, users)


def copy_item_in_op_oneclient(item_type, src_path, dst_path, user, users,
                              host):
    if item_type == 'directory':
        multi_dir_steps.copy_dir(user, src_path, dst_path, host, users)
    else:
        multi_reg_file_steps.copy_reg_file(user, src_path, dst_path, host,
                                           users)


def move_item_in_op_oneclient(user, src_path, dst_path, users, result, host):
    if result == 'fails':
        multi_file_steps.rename_fail(user, src_path, dst_path, host, users)
    else:
        multi_file_steps.rename(user, src_path, dst_path, host, users)


@repeat_failed(timeout=WAIT_BACKEND)
def assert_posix_permissions_in_op_oneclient(user, path, perm, host, users):
    multi_file_steps.check_mode(user, path, perm, host, users)


def set_posix_permissions_in_op_oneclient(user, path, perm, host, users,
                                          result):
    if result == 'fails':
        multi_file_steps.change_mode_fail(user, path, perm, host, users)
    else:
        multi_file_steps.change_mode(user, path, perm, host, users)


def set_metadata_in_op_oneclient(attr_val, attr_type, path, user, users,
                                 host):
    if attr_type == 'basic':
        (attr, attr_val) = attr_val.split('=')
    else:
        attr = 'onedata_{}'.format(attr_type.lower())

    multi_file_steps.set_xattr(user, path, attr, attr_val, host, users)


def assert_metadata_in_op_oneclient(attr_val, attr_type, path, user, users,
                                    host):
    if attr_type == 'basic':
        attr, val = attr_val.split('=')
        multi_file_steps.check_string_xattr(user, path, attr, val, host, users)
    elif attr_type.lower() == 'json':
        multi_file_steps.check_json_xattr(user, path, 'onedata_json', attr_val,
                                          host, users)
    else:
        multi_file_steps.check_string_xattr(user, path, 'onedata_rdf',
                                            attr_val, host, users)


def remove_all_metadata_in_op_oneclient(user, users, host, path):
    multi_file_steps.remove_xattr(user, path, 'onedata_rdf', host, users)
    multi_file_steps.remove_xattr(user, path, 'onedata_json', host, users)
    multi_file_steps.remove_all_xattr(user, path, host, users)


def assert_no_such_metadata_in_op_oneclient(user, users, host, path,
                                            tab_name, val):
    metadata = multi_file_steps.get_metadata(user, path, host, users)
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
                assert key not in metadata or metadata[key] != val[key], \
                    'There is {} {} metadata'.format(val, tab_name)
        else:
            assert val != metadata, 'There is {} {} metadata'.format(val,
                                                                     tab_name)


def assert_ace_in_op_oneclient(user, users, host, path, num, priv, item_type,
                               name, numerals):
    ace = multi_file_steps.get_metadata(user, path, host, users)['cdmi_acl']
    ace = json.loads(ace)[numerals[num]]
    assert_ace(priv, item_type, ace, name, num, path)


def grant_acl_privileges_in_op_oneclient(user, users, host, path, priv,
                                         item_type, groups, name):
    try:
        acl = multi_file_steps.get_metadata(user, path, host, users)['cdmi_acl']
        acl = json.loads(acl)
    except KeyError:
        acl = []
    acl = get_acl_metadata(acl, priv, item_type, groups, name, users, path)
    multi_file_steps.set_xattr(user, path, 'cdmi_acl', json.dumps(acl), host,
                               users)


def remove_file_in_op_oneclient(user, path, host, users, res):
    if res == 'fails':
        multi_file_steps.delete_file_fail(user, path, host, users)
    else:
        multi_file_steps.delete_file(user, path, host, users)
