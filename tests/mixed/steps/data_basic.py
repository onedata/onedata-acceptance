"""This module contains gherkin steps to run mixed acceptance tests featuring
basic operations on data using web GUI and REST.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import when, then, given, parsers

from tests.mixed.utils.oneprovider.data import *
from tests.gui.meta_steps.oneprovider.data import *


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create'
                 ' directory named "(?P<name>.*)" in "(?P<space>.*)" in '
                 '(?P<host>.*) Oneprovider'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create'
                 ' directory named "(?P<name>.*)" in "(?P<space>.*)" in '
                 '(?P<host>.*) Oneprovider'))
def create_dir_in_op(client, user, users, space, name, hosts, selenium, op_page,
                     tmp_memory, host, result):
        
    if client.lower() == 'web gui':
        create_item_in_op_gui(selenium, user, '', 'directory', name, 
                              tmp_memory, op_page, result, space)
    elif client.lower() == 'rest':
        create_dir_in_op_rest(user, users, host, hosts, 
                              '{}/{}'.format(space, name), result)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create'
                 ' file named "(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*)'
                 ' Oneprovider'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create'
                 ' file named "(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*)'
                 ' Oneprovider'))
def create_file_in_op(client, user, users, space, name, hosts, tmp_memory, host,
                      selenium, op_page, result):
        
    if client.lower() == 'web gui':
        create_item_in_op_gui(selenium, user, '', 'file', name, 
                              tmp_memory, op_page, result, space)
    elif client.lower() == 'rest':
        create_file_in_op_rest(user, users, host, hosts, 
                               '{}/{}'.format(space, name), result)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to see '
                 'items? named (?P<name_list>.*) in "(?P<space>.*)" in '
                 '(?P<host>.*) Oneprovider'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to see '
                 'items? named (?P<name_list>.*) in "(?P<space>.*)" in '
                 '(?P<host>.*) Oneprovider'))
def see_item_in_op(client, user, users, result, name_list, space, host, hosts, 
                   selenium, tmp_memory, op_page):
        
    if client.lower() == 'web gui':
        see_items_in_op_gui(selenium, user, '', name_list, tmp_memory, 
                            op_page, result, space)
    elif client.lower() == 'rest':
        see_items_in_op_rest(user, users, host, hosts, name_list, 
                             result, space)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) removes directory named '
                 '"(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*) Oneprovider'))
def remove_dir_in_op(client, user, users, space, name, hosts, selenium, op_page,
                     tmp_memory, host):
        
    if client.lower() == 'web gui':
        remove_item_in_op_gui(selenium, user, name, tmp_memory, op_page, 
                              'succeds', space)
    elif client.lower() == 'rest':
        remove_dir_in_op_rest(user, users, host, hosts, 
                              '{}/{}'.format(space, name))
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) removes file named '
                 '"(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*) Oneprovider'))
def remove_file_in_op(client, user, users, space, name, hosts, tmp_memory, host,
                      selenium, op_page):
        
    if client.lower() == 'web gui':
        remove_item_in_op_gui(selenium, user, name, tmp_memory, op_page, 
                              'succeds', space)
    elif client.lower() == 'rest':
        remove_file_in_op_rest(user, users, host, hosts, 
                               '{}/{}'.format(space, name))
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) creates directory '
                 'structure in "(?P<space>.*)" space on (?P<host>.*) '
                 'Oneprovider as follow:\n(?P<config>(.|\s)*)'))
def create_directory_structure_in_op(selenium, user, op_page, config, space, 
                                     tmp_memory, users, hosts, host, client):

    if client.lower() == 'web gui':
        create_directory_structure_in_op_gui(selenium, user, op_page, 
                                             config, space, tmp_memory)
    elif client.lower() == 'rest':
        create_directory_structure_in_op_rest(user, users, hosts, host,
                                              config, space)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))

    tmp_memory['config'] = config


@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that directory '
                 'structure in "(?P<space>.*)" space is as previously created'))
def assert_directory_structure_in_op(client, selenium, user, op_page, oz_page, 
                                     tmp_memory, tmpdir, space, host, spaces, 
                                     hosts, users):
    config = tmp_memory['config']

    if client.lower() == 'web gui':
        assert_space_content_in_op_gui(config, selenium, user, op_page, 
                                       tmp_memory, tmpdir, space, oz_page, host,
                                       hosts)
    elif client.lower() == 'rest':
        assert_space_content_in_op_rest(user, users, hosts, config, space, 
                                        spaces, host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that (?P<path>.*?)'
                 ' in space "(?P<space>.*)" (has|have) (?P<priv>.*) privileges?'
                 ' set for (?P<type>.*?) (?P<name>.*) in (?P<num>.*) ACL record'
                 ' in (?P<host>.*) Oneprovider'))
def assert_ace_in_op(client, selenium, user, cdmi, op_page, space, path, host, 
                     hosts, users, num, priv, type, name, numerals, tmp_memory,
                     modals):

    if client.lower() == 'web gui':
        assert_ace_in_op_gui(selenium, user, priv, type, name, num, space, path,
                             op_page, tmp_memory, modals, numerals) 
    elif client.lower() == 'rest':
        assert_ace_in_op_rest(user, users, host, hosts, cdmi, numerals,
                              '/{}/{}'.format(space, path), num, priv, type, name)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) sets new ACE for '
                 '(?P<path>.*?) in space "(?P<space>.*)" with (?P<priv>.*) '
                 'privileges? set for (?P<type>.*?) (?P<name>.*)'
                 ' in (?P<host>.*) Oneprovider'))
def grant_acl_privileges_in_op(client, selenium, user, cdmi, op_page, space, path,
                             host, hosts, users, priv, type, name, numerals, 
                             groups, tmp_memory, modals):   

    if client.lower() == 'web gui':
        grant_acl_privileges_in_op_gui(selenium, user, path, priv, type, name, 
                                     op_page, tmp_memory, modals, space, 
                                     numerals) 
    elif client.lower() == 'rest':
        grant_acl_privileges_in_op_rest(user, users, host, hosts, cdmi, 
                                      '/{}/{}'.format(space, path), priv, type,
                                      name, groups)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) sets new (?P<tab_name>.*) metadata: (?P<val>.*) for (?P<path>.*?) in '
                 'space "(?P<space>.*)" in (?P<host>.*) Oneprovider'))
def set_metadata_in_op(client, selenium, user, tab_name, val, cdmi, op_page, 
                       space, path, host, hosts, users, tmp_memory):   

    if client.lower() == 'web gui':
        set_metadata_in_op_gui(selenium, user, path, tmp_memory, op_page, 's',
                               space, tab_name, val) 
    elif client.lower() == 'rest':
        set_metadata_in_op_rest(user, users, host, hosts, cdmi, 
                                      '/{}/{}'.format(space, path), tab_name, val)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that '
                 '(?P<tab_name>.*) metadata for (?P<path>.*?) is (?P<val>.*) '
                 'in space "(?P<space>.*)" in (?P<host>.*) Oneprovider'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that '
                 '(?P<tab_name>.*) metadata for (?P<path>.*?) is (?P<val>.*) '
                 'in space "(?P<space>.*)" in (?P<host>.*) Oneprovider'))
def assert_metadata_in_op(client, selenium, user, tab_name, val, cdmi, op_page,
                          space, path, host, hosts, users, tmp_memory):   

    if client.lower() == 'web gui':
        assert_metadata_in_op_gui(selenium, user, path, tmp_memory, op_page, 
                                  's', space, tab_name, val)
    elif client.lower() == 'rest':
        assert_metadata_in_op_rest(user, users, host, hosts, cdmi, 
                                      '/{}/{}'.format(space, path), tab_name, val)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) removes all (?P<path>.*) '
                 'metadata in space "(?P<space>\w+)" in (?P<host>.*) '
                 'Oneprovider'))
def remove_all_metadata_in_op(client, selenium, user, users, space, op_page, 
                              tmp_memory, path, host, hosts, cdmi):

    if client.lower() == 'web gui':
        remove_all_metadata_in_op_gui(selenium, user, space, op_page, 
                                      tmp_memory, path) 
    elif client.lower() == 'rest':
        remove_all_metadata_in_op_rest(user, users, host, hosts, cdmi, 
                                      '/{}/{}'.format(space, path))
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that '
                 '(?P<tab_name>.*) metadata for (?P<path>.*) in space '
                 '"(?P<space>.*)" does not contain (?P<val>.*) in '
                 '(?P<host>.*) Oneprovider'))
def assert_no_such_metadata_in_op(client, selenium, user, users, space, op_page,
                                  tmp_memory, path, host, hosts, cdmi, val, 
                                  tab_name):

    if client.lower() == 'web gui':
        assert_metadata_in_op_gui(selenium, user, path, tmp_memory, op_page, 
                                  'fails', space, tab_name, val) 
    elif client.lower() == 'rest':
        assert_no_such_metadata_in_op_rest(user, users, host, hosts, cdmi, 
                                      '/{}/{}'.format(space, path), tab_name, val)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))

