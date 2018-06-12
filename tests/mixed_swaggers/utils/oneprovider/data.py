"""Utils and fixtures to facilitate data operations in Oneprovider
using REST API.
"""

__author__ = "Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import when, then, given, parsers
from tests.mixed_swaggers.utils.common import *
from tests.gui.utils.generic import parse_seq
import yaml
import os
import pytest
import json
from tests.mixed_swaggers.cdmi_client import ContainerApi, DataObjectApi
from tests.mixed_swaggers.onepprovider_client import DataApi
from tests.mixed_swaggers.cdmi_client.rest import ApiException as CdmiException
from tests.mixed_swaggers.onepprovider_client.rest import ApiException as OPException


def assert_space_content_in_op_rest(user, users, hosts, config, space_name,
                                    spaces, host):
    user_client_op = login_to_provider(user, users, hosts[host]['hostname'])
    data_api = DataApi(user_client_op)

    children = [file.path for file in data_api.list_files(space_name)]
    cwd = '/' + space_name
    _check_files_tree(yaml.load(config), children, cwd, user, users, hosts,
                      spaces, data_api, host)


def _check_files_tree(subtree, children, cwd, user, users, hosts, spaces,
                      data_api, provider):
    for item in subtree:
        try:
            [(item_name, item_desc)] = item.items()
        except AttributeError:
            assert os.path.join(cwd, item) in children, \
                '{} not found in {}'.format(item, cwd)
            if item.startswith('dir'):
                item_children = [file.path for file in data_api.list_files(
                    os.path.join(cwd, item)
                )]
                assert len(item_children) == 0, \
                    'Directory {} in {} is not empty'.format(item, cwd)
        else:
            assert os.path.join(cwd, item_name) in children, \
                '{} not found in {}'.format(item_name, cwd)

            # if item is directory go deeper
            if item_name.startswith('dir'):
                item_children = [file.path for file in data_api.list_files(
                    os.path.join(cwd, item_name)
                )]
                if isinstance(item_desc, int):
                    assert len(item_children) == item_desc, \
                        'Directory {} in {} has wrong number of children. ' \
                        'Expected: {}, got: {}'.format(item_name, cwd,
                                                       item_desc,
                                                       len(item_children))
                else:
                    _check_files_tree(item_desc, item_children,
                                      os.path.join(cwd, item_name), user,
                                      users, hosts, spaces, data_api, provider)
            else:
                cli = login_to_cdmi(user, users, hosts[provider]['hostname'])
                dao = DataObjectApi(cli)
                file_content = dao.read_data_object(os.path.join(cwd,
                                                                 item_name))
                assert file_content == str(item_desc), \
                    'File {} in {} has wrong content. Expected: {}, got: {}'. \
                    format(item_name, cwd, item_desc, file_content)


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


def create_file_in_op_rest(user, users, host, hosts, path, result):
    client = login_to_cdmi(user, users, hosts[host]['hostname'])

    do_api = DataObjectApi(client)
    if result == 'fails':
        with pytest.raises(CdmiException, message='Creating file did not fail'):
            do_api.create_data_object(path, '')
    else:
        do_api.create_data_object(path, '')


def remove_file_in_op_rest(user, users, host, hosts, path):
    client = login_to_cdmi(user, users, hosts[host]['hostname'])

    do_api = DataObjectApi(client)
    do_api.delete_data_object(path)


def see_items_in_op_rest(user, users, host, hosts, path_list, result, space):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    d_api = DataApi(client)
    for path in parse_seq(path_list):
        path = '{}/{}'.format(space, path)
        if result == 'fails':
            with pytest.raises(OPException, 
                               message='There is item {}'.format(path)):
                d_api.list_files(path)
        else:
            d_api.list_files(path)


def create_directory_structure_in_op_rest(user, users, hosts, host, config, 
                                          space):
    items = yaml.load(config)
    cwd = space
    _create_content(user, users, hosts, cwd, items, host)


def _create_item(user, users, hosts, cwd, name, content, host):
    if name.startswith('dir'):
        create_dir_in_op_rest(user, users, host, hosts, 
                              '{}/{}'.format(cwd, name), '')
    else:
        create_file_in_op_rest(user, users, host, hosts, 
                               '{}/{}'.format(cwd, name), '')
    if not content:
        return
    cwd += '/' + name
    _create_content(user, users, hosts, cwd, content, host)


def _create_content(user, users, hosts, cwd, content, host):        
    for item in content:
        try:
            [(name, content)] = item.items()
        except AttributeError:
            name = item
            content = None
        _create_item(user, users, hosts, cwd, name, content, host)


ACL_MASK = {
    'object':{        
        0x00001 : 'read',
        0x00002 : 'write',
        0x00004 : 'append data',
        0x00008 : 'read metadata',
        0x00010 : 'write metadata',
        0x00020 : 'execute',
        0x00040 : 'delete element',
        0x00080 : 'read attributes',
        0x00100 : 'write attributes',
        0x10000 : 'delete',
        0x20000 : 'read acl',
        0x40000 : 'change acl',
        0x80000 : 'change owner'
    },
    'container':{        
        0x00001 : 'list files',
        0x00002 : 'add files',
        0x00004 : 'add subdirectory',
        0x00008 : 'read metadata',
        0x00010 : 'write metadata',
        0x00020 : 'traverse directory',
        0x00040 : 'delete subdirectory',
        0x00080 : 'read attributes',
        0x00100 : 'write attributes',
        0x10000 : 'delete',
        0x20000 : 'read acl',
        0x40000 : 'change acl',
        0x80000 : 'change owner'
    }
}


def assert_ace_in_op_rest(user, users, host, hosts, cdmi, numerals, path, num, 
                          priv, type, name):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    ace = client.read_metadata(path)['metadata']['cdmi_acl'][numerals[num]]
    priv = parse_seq(priv)
    if 'deny' in priv:
        acetype = '0x1'  
        priv.remove('deny')
    else:
        acetype = '0x0'
    aceflags = '0x40' if type == 'group' else '0x0'
    type = 'container' if path.split('/')[-1].startswith('dir') else 'object'
    mask = int(ace['acemask'], 16)
    keys = ACL_MASK[type].keys()
    set_priv = [ACL_MASK[type][key] for key in keys if mask & key == key]
    set_priv.sort()
    assert ace['identifier'].startswith(name), ('Identifier in {} ACE is not {}'
                                                ''.format(num, name))
    assert ace['acetype'] == acetype,  'Type in {} ACE is not {}'.format(num, acetype)
    assert ace['aceflags'] == aceflags, ('{} ACE is set for {}'.format(num, 
                                         'group' if aceflags else 'user'))
    assert set_priv == sorted(priv), ('Privileges in {} ACE are not correct'
                                      ''.format(num))


def grant_acl_privileges_in_op_rest(user, users, host, hosts, cdmi, path, priv, 
                                  type, name, groups):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    try:
        acl = client.read_metadata(path)['metadata']['cdmi_acl']
    except KeyError:
        acl = []
    acl.append({})
    ace = acl[-1]
    priv = parse_seq(priv)
    if 'deny' in priv:
        acetype = '0x1'  
        priv.remove('deny')
    else:
        acetype = '0x0'
    if type == 'group':
        aceflags = '0x40'
        name_id = groups[name]
    else:
        aceflags = '0x0'
        name_id = users[name].id
    type = 'container' if path.split('/')[-1].startswith('dir') else 'object'
    path += '/' if type == 'container' else ''
    ace['identifier'] = '{}#{}'.format(name, name_id)
    ace['acetype'] = acetype
    acemask = 0
    for p in ACL_MASK[type]:
        if ACL_MASK[type][p] in priv:
            acemask |= p
    ace['acemask'] = hex(acemask)
    ace['aceflags'] = aceflags
    content_type = 'application/cdmi-{}'.format(type)
    client.write_metadata(path, { 'cdmi_acl' : acl }, content_type)


def assert_metadata_in_op_rest(user, users, host, hosts, cdmi, path, tab_name, 
                               val):    
    client = cdmi(hosts[host]['hostname'], users[user].token)
    metadata = client.read_metadata(path)['metadata']
    if tab_name.lower() == 'basic':
        (attr, val) = val.split('=')
        assert attr in metadata, '{} has no {} {} metadata'.format(path, attr, 
                                                                   tab_name)
        assert val == metadata[attr], '{} has no {} = {} {}'.format(path, attr,
                                                                val, tab_name)
    else:        
        metadata = metadata['onedata_{}'.format(tab_name.lower())]
        if tab_name.lower() == 'json':
            assert val == json.dumps(metadata), \
                        '{} has no {} {} metadata'.format(path, val, tab_name)
        else:
            assert val == metadata, \
                        '{} has no {} {} metadata'.format(path, val, tab_name)


def set_metadata_in_op_rest(user, users, host, hosts, cdmi, path, tab_name, 
                            val):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    if tab_name == 'basic':
        (attr, val) = val.split('=')
    else:
        attr = 'onedata_{}'.format(tab_name.lower())
        if tab_name.lower() == 'json':
            val = json.loads(val)
    type = 'container' if path.split('/')[-1].startswith('dir') else 'object'
    if type == 'container':
        path += '/' 
    content_type = 'application/cdmi-{}'.format(type)
    client.write_metadata(path, {attr : val}, content_type)
    

def remove_all_metadata_in_op_rest(user, users, host, hosts, cdmi, path):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    type = 'container' if path.split('/')[-1].startswith('dir') else 'object'
    if type == 'container':
        path += '/' 
    content_type = 'application/cdmi-{}'.format(type)
    client.write_metadata(path, {}, content_type)


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
                assert key not in metadata or metadata[key] != val[key], \
                    'There is {} {} metadata'.format(val, tab_name)
        else:
            assert val != metadata, 'There is {} {} metadata'.format(val, 
                                                                     tab_name)
