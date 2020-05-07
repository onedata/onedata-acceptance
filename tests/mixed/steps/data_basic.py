"""This module contains gherkin steps to run mixed acceptance tests featuring
basic operations on data using web GUI and REST.
"""

__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.oneprovider.metadata import *
from tests.mixed.steps.oneclient.data_basic import *
from tests.mixed.steps.rest.oneprovider.data import *
from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.meta_steps.oneprovider.permissions import *
from tests.utils.path_utils import get_first_path_element


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create '
               'file named "(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*)'))
def create_file_in_op(client, user, users, space, name, hosts, tmp_memory, host,
                      selenium, op_container, result):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_item_in_op_gui(selenium, user, os.path.dirname(name),
                              'file', os.path.basename(name),
                              tmp_memory, op_container, result, space)
    elif client_lower == 'rest':
        create_file_in_op_rest(user, users, host, hosts, full_path, result)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        create_file_in_op_oneclient(user, full_path, users, result,
                                    oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create '
               'directory named "(?P<name>.*)" in "(?P<space>.*)" in '
               '(?P<host>.*)'))
def create_file_in_op(client, user, users, space, name, hosts, tmp_memory, host,
                      selenium, op_container, result):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_item_in_op_gui(selenium, user, os.path.dirname(name),
                              'directory', os.path.basename(name),
                              tmp_memory, op_container, result, space)
    elif client_lower == 'rest':
        create_dir_in_op_rest(user, users, host, hosts, full_path, result)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        create_dir_in_op_oneclient(user, full_path, users, result,
                                   oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to see '
               'items? named (?P<name_list>.*) in "(?P<space>.*)" in '
               '(?P<host>.*)'))
def see_item_in_op(client, user, users, result, name_list, space, host, hosts, 
                   selenium, tmp_memory, op_container):
    client_lower = client.lower()
    if client_lower == 'web gui':
        see_items_in_op_gui(selenium, user, '', name_list, tmp_memory, 
                            op_container, result, space)
    elif client_lower == 'rest':
        see_items_in_op_rest(user, users, host, hosts, name_list, 
                             result, space)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        see_items_in_op_oneclient(name_list, space, user, users, result,
                                  oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to '
                 'remove directory \(rmdir\) named "(?P<name>.*)" in '
                 '"(?P<space>.*)" in (?P<host>.*)'))
def remove_empty_dir_in_op(client, user, users, result, space, name, hosts,
                           selenium, op_container, tmp_memory, host):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_item_in_op_gui(selenium, user, name, tmp_memory, op_container, 
                              'succeds', space)
    elif client_lower == 'rest':
        remove_dir_in_op_rest(user, users, host, hosts, full_path)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        delete_empty_directory_in_op_oneclient(full_path, user, users, result,
                                               oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) removes directory '
                 '\(rmdir -p\) named "(?P<name>.*)" in "(?P<space>.*)" in '
                 '(?P<host>.*)'))
def remove_empty_dir_and_parents_in_op(client, user, users, space, name, hosts,
                                       selenium, op_container, tmp_memory, host):
    first_path_elem = get_first_path_element(name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_dir_and_parents_in_op_gui(selenium, user, first_path_elem,
                                         tmp_memory, op_container, 'succeds',
                                         space)
    elif client_lower == 'rest':
        remove_dir_in_op_rest(user, users, host, hosts,
                              '{}/{}'.format(space, first_path_elem))
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_dir_steps.delete_parents(user, '{}/{}'.format(space, name),
                                       oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) removes directory '
                 '\(rm -rf\) named "(?P<name>.*)" in "(?P<space>.*)" in '
                 '(?P<host>.*)'))
def remove_dir_in_op(client, user, users, space, name, hosts, selenium,
                     op_container, tmp_memory, host):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_item_in_op_gui(selenium, user, name, tmp_memory, op_container,
                              'succeds', space)
    elif client_lower == 'rest':
        remove_dir_in_op_rest(user, users, host, hosts, full_path)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_dir_steps.delete_non_empty(user, full_path, oneclient_host,
                                         users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) '
               'to remove file named "(?P<name>.*)" in "(?P<space>.*)" in '
               '(?P<host>.*)'))
def remove_file_in_op(client, user, name, space, host, users, hosts,
                      tmp_memory, selenium, op_container, result):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_item_in_op_gui(selenium, user, name, tmp_memory, op_container, 
                              result, space)
    elif client_lower == 'rest':
        remove_file_in_op_rest(user, users, host, hosts, full_path, result)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        remove_file_in_op_oneclient(user, full_path, oneclient_host,
                                    users, result)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) '
                 'renames item named "(?P<old_name>.*)" to "(?P<new_name>.*)" '
                 'in "(?P<space>.*)" in (?P<host>.*)'))
def rename_item_in_op(client, user, users, result, space, old_name, new_name,
                      hosts, tmp_memory, host, selenium, op_container, cdmi, ):
    old_path = '{}/{}'.format(space, old_name)
    new_path = '{}/{}'.format(space, new_name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        rename_item(selenium, user, old_name, new_name, tmp_memory,
                    op_container, result, space)
    elif client_lower == 'rest':
        move_item_in_op_rest(old_path, new_path, result, cdmi, host, hosts,
                             user, users)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_file_steps.rename(user, old_path, new_path, oneclient_host,
                                users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that there '
               '(is 1|are (?P<num>\d+)) items? in "(?P<space>.*)" in '
               '(?P<host>.*)'))
def see_num_of_items_in_op(client, user, num, space, host, users,
                           hosts, tmp_memory, selenium, op_container,
                           oz_page, modals):
    num = int(num) if num is not None else 1
    client_lower = client.lower()
    if client_lower == 'web gui':
        see_num_of_items_in_path_in_op_gui(selenium, user, tmp_memory,
                                           op_container, '', space, num,
                                           oz_page, host, hosts, modals)
    elif client_lower == 'rest':
        assert_num_of_files_in_path_in_op_rest(num, space, user, users, host,
                                               hosts)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        assert_num_of_files_in_path_in_op_oneclient(num, space, user, users,
                                                    oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) writes "(?P<text>.*)" '
                 'to file named "(?P<file_name>.*)" in '
                 '"(?P<space>.*)" in (?P<host>.*)'))
def write_to_file_in_op(client, user, text, file_name, space, host, users,
                        hosts, cdmi):
    full_path = '{}/{}'.format(space, file_name)
    client_lower = client.lower()
    if client_lower == 'rest':
        write_to_file_in_op_rest(user, users, host, hosts, cdmi, full_path,
                                 text)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_reg_file_steps.write_text(user, text, full_path, oneclient_host,
                                        users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) reads "(?P<text>.*)" '
               'from file named "(?P<file_name>.*)" in '
               '"(?P<space>.*)" in (?P<host>.*)'))
def read_from_file_in_op(client, user, text, file_name, space, host, users,
                         hosts, selenium, oz_page, op_container, tmp_memory,
                         tmpdir, modals):
    full_path = '{}/{}'.format(space, file_name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_file_content_in_op_gui(text, file_name, space, selenium, user,
                                      users, host, hosts, oz_page, op_container,
                                      tmp_memory, tmpdir, modals)
    elif client_lower == 'rest':
        assert_file_content_in_op_rest(full_path, text, user, users,
                                       host, hosts)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_reg_file_steps.read_text(user, text, full_path, oneclient_host,
                                       users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) appends "(?P<text>.*)" '
                 'to file named "(?P<file_name>.*)" in '
                 '"(?P<space>.*)" in (?P<host>.*)'))
def append_to_file_in_op(client, user, text, file_name, space, host, users,
                         hosts, cdmi):
    full_path = '{}/{}'.format(space, file_name)
    client_lower = client.lower()
    if client_lower == 'rest':
        append_to_file_in_op_rest(user, users, host, hosts, cdmi, full_path,
                                  text)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_reg_file_steps.append(user, text, full_path, oneclient_host,
                                    users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) replaces '
                 '"(?P<old_text>.*)" with "(?P<new_text>.*)" '
                 'in file named "(?P<file_name>.*)" in '
                 '"(?P<space>.*)" in (?P<host>.*)'))
def replace_in_file_in_op(client, user, old_text, new_text, file_name, space,
                          host, users):
    full_path = '{}/{}'.format(space, file_name)
    client_lower = client.lower()
    if 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_reg_file_steps.replace(user, old_text, new_text, full_path,
                                     oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to move '
                 '"(?P<src_path>.*)" to "(?P<dst_path>.*)" '
                 'in (?P<host>.*)'))
def move_file_in_op(client, user, result, src_path, dst_path, host, users,
                    cdmi, hosts):
    client_lower = client.lower()
    if client_lower == 'rest':
        move_item_in_op_rest(src_path, dst_path, result, cdmi, host, hosts,
                             user, users)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        move_item_in_op_oneclient(user, src_path, dst_path, users, result,
                                  oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) copies '
                 '(?P<item_type>(directory|file)) named '
                 '"(?P<src_path>.*)" to "(?P<dst_path>.*)" '
                 'in (?P<host>.*)'))
def copy_item_in_op(client, user, item_type, src_path, dst_path, host, users,
                    cdmi, hosts):
    client_lower = client.lower()
    if client_lower == 'rest':
        copy_item_in_op_rest(src_path, dst_path, cdmi, host, hosts, user,
                             users)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        copy_item_in_op_oneclient(item_type, src_path, dst_path,
                                  user, users, oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) creates directory '
                 'structure in "(?P<space>.*)" space on (?P<host>.*) '
                 'as follow:\n(?P<config>(.|\s)*)'))
def create_directory_structure_in_op(selenium, user, op_container, config, space, 
                                     tmp_memory, users, hosts, host, client):
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_directory_structure_in_op_gui(selenium, user, op_container, 
                                             config, space, tmp_memory)
    elif client_lower == 'rest':
        create_directory_structure_in_op_rest(user, users, hosts, host,
                                              config, space)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        create_directory_structure_in_op_oneclient(user, users, config, space,
                                                   oneclient_host, hosts)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))

    tmp_memory['config'] = config


@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that (?P<time1>.*) '
                 'time of item named "(?P<file_name>.*)" in "(?P<space>.*)" '
                 'space is (?P<comparator>.*) (to|than) '
                 '(?P<time2>.*) time in (?P<host>.*)'))
def assert_time_relation(user, time1, file_name, space, comparator, time2,
                         client, users, host, hosts, cdmi):
    client_lower = client.lower()
    full_path = '{}/{}'.format(space, file_name)
    if client_lower == 'rest':
        assert_time_relation_in_op_rest(full_path, time1, time2, comparator,
                                        host, hosts, user, users, cdmi)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_file_steps.check_time(user, time1, time2, comparator, full_path,
                                    oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.*) sees that '
                 '(?P<time_name>.*) time of item named "(?P<file_path>.*)" '
                 'in "(?P<space>.*)" space is not earlier than '
                 '(?P<time>[0-9]*) seconds ago in (?P<host>.*)'))
def assert_mtime_not_earlier_than(client, file_path, selenium, user,
                                  space, op_container, time, tmp_memory):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_mtime_not_earlier_than_op_gui(file_path, selenium, time, user,
                                             space, op_container, tmp_memory)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that directory '
               'structure in "(?P<space>.*)" space in (?P<host>.*) is as '
               'previously created'))
def assert_directory_structure_in_op(client, selenium, user, op_container, oz_page, 
                                     tmp_memory, tmpdir, space, host, spaces, 
                                     hosts, users, modals):
    config = tmp_memory['config']
    client_lower = client.lower()

    if client_lower == 'web gui':
        assert_space_content_in_op_gui(config, selenium, user, op_container, 
                                       tmp_memory, tmpdir, space, oz_page, host,
                                       hosts, modals)
    elif client_lower == 'rest':
        assert_space_content_in_op_rest(user, users, hosts, config, space, 
                                        spaces, host)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        assert_space_content_in_op_oneclient(config, space, user, users,
                                             oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that directory '
                 'structure in "(?P<space>.*)" space in (?P<host>.*) is as '
                 'follow:\n(?P<config>(.|\s)*)'))
def assert_directory_structure_in_op(client, selenium, user, op_container, oz_page,
                                     tmp_memory, tmpdir, space, host, spaces,
                                     hosts, users, config, modals):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_space_content_in_op_gui(config, selenium, user, op_container,
                                       tmp_memory, tmpdir, space, oz_page,
                                       host, hosts, modals)
    elif client_lower == 'rest':
        assert_space_content_in_op_rest(user, users, hosts, config, space,
                                        spaces, host)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        assert_space_content_in_op_oneclient(config, space, user, users,
                                             oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that (?P<path>.*?)'
                 ' in space "(?P<space>.*)" (has|have) (?P<priv>.*) '
                 'privileges? set for (?P<type>.*?) (?P<name>.*) in '
                 '(?P<num>.*) ACL record in (?P<host>.*)'))
def assert_ace_in_op(client, selenium, user, cdmi, op_container, space, path, host, 
                     hosts, users, num, priv, type, name, numerals, tmp_memory,
                     modals):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_ace_in_op_gui(selenium, user, priv, type, name, num, space,
                             path, op_container, tmp_memory, modals, numerals)
    elif client_lower == 'rest':
        assert_ace_in_op_rest(user, users, host, hosts, cdmi, numerals,
                              full_path, num, priv, type,
                              name)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        assert_ace_in_op_oneclient(user, users, oneclient_host, full_path, num,
                                   priv, type, name, numerals)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) sets new ACE for '
                 '(?P<path>.*?) in space "(?P<space>.*)" with (?P<priv>.*) '
                 'privileges? set for (?P<type>.*?) (?P<name>.*)'
                 ' in (?P<host>.*)'))
def grant_acl_privileges_in_op(client, selenium, user, cdmi, op_container, space,
                               path, host, hosts, users, priv, type, name,
                               numerals, groups, tmp_memory, popups, modals):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        grant_acl_privileges_in_op_gui(selenium, user, path, priv, type, name, 
                                      op_container, tmp_memory, popups, space,
                                      numerals, modals)
    elif client_lower == 'rest':
        grant_acl_privileges_in_op_rest(user, users, host, hosts, cdmi, 
                                        full_path, priv,
                                        type, name, groups)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        grant_acl_privileges_in_op_oneclient(user, users, oneclient_host,
                                             full_path, priv, type, groups,
                                             name)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) sets new '
                 '(?P<tab_name>.*) metadata: (?P<val>.*) for "(?P<path>.*?)"'
                 ' (?P<item>file|directory) in space "(?P<space>.*)" in (?P<host>.*)'))
def set_metadata_in_op(client, selenium, user, tab_name, val, cdmi, op_container, 
                       space, path, host, hosts, users, tmp_memory, modals, oz_page):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        set_metadata_in_op_gui(selenium, user, path, tmp_memory, op_container, 's',
                               space, tab_name, val, modals, oz_page, 'file')
    elif client_lower == 'rest':
        set_metadata_in_op_rest(user, users, host, hosts, cdmi, full_path,
                                tab_name, val)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        set_metadata_in_op_oneclient(val, tab_name, full_path, user, users,
                                     oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that '
               '(?P<tab_name>.*) metadata for "(?P<path>.*?)" '
               '(?P<item>file|directory) is '
               '(?P<val>.*) in space "(?P<space>.*)" in (?P<host>.*)'))
def assert_metadata_in_op(client, selenium, user, tab_name, val, cdmi, op_container,
                          space, path, host, hosts, users, tmp_memory, item, modals,
                          oz_page):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_metadata_in_op_gui(selenium, user, path, tmp_memory, op_container, 
                                  's', space, tab_name, val, modals, oz_page,
                                  item)
    elif client_lower == 'rest':
        assert_metadata_in_op_rest(user, users, host, hosts, cdmi, 
                                   full_path, tab_name, val)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        assert_metadata_in_op_oneclient(val, tab_name, full_path, user, users,
                                        oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) removes all '
                 '"(?P<path>.*)" (?P<item>file|directory) '
                 'metadata in space "(?P<space>\w+)" '
                 'in (?P<host>.*)'))
def remove_all_metadata_in_op(client, selenium, user, users, space, op_container, 
                              tmp_memory, path, host, hosts, cdmi, oz_page,
                              modals, item):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_all_metadata_in_op_gui(selenium, user, space, op_container, 
                                      tmp_memory, path, oz_page, modals, item)
    elif client_lower == 'rest':
        remove_all_metadata_in_op_rest(user, users, host, hosts, cdmi, 
                                       full_path)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        remove_all_metadata_in_op_oneclient(user, users, oneclient_host,
                                            full_path)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that '
                 '(?P<tab_name>.*) metadata for "(?P<path>.*)" '
                 '(?P<item>file|directory) in space '
                 '"(?P<space>.*)" does not contain (?P<val>.*) in '
                 '(?P<host>.*)'))
def assert_no_such_metadata_in_op(client, selenium, user, users, space, op_container,
                                  tmp_memory, path, host, hosts, cdmi, val, 
                                  tab_name, item, modals, oz_page):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_metadata_in_op_gui(selenium, user, path, tmp_memory, op_container, 
                                  'fails', space, tab_name, val, modals, oz_page)
    elif client_lower == 'rest':
        assert_no_such_metadata_in_op_rest(user, users, host, hosts, cdmi, 
                                           full_path, tab_name, val)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        assert_no_such_metadata_in_op_oneclient(user, users, oneclient_host,
                                                full_path, tab_name, val)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) uploads "(?P<path>.*)" '
                 'to "(?P<space>.*)" in (?P<host>.*)'))
def upload_file_to_op(client, selenium, user, path, space, host, hosts,
                      tmp_memory, op_container):
    client_lower = client.lower()
    if client_lower == 'web gui':
        upload_file_to_op_gui(path, selenium, user, space, op_container, tmp_memory)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) sees '
               'that POSIX permission for item named "(?P<item_path>.*)" in '
               '"(?P<space>.*)" is "(?P<mode>.*)" in (?P<host>.*)'))
def assert_posix_permissions_in_op(client, user, item_path, space, mode,
                                   host, selenium, op_container, tmp_memory, modals,
                                   users, hosts):
    full_path = '{}/{}'.format(space, item_path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_posix_permissions_in_op_gui(selenium, user, space, item_path,
                                           mode, op_container, tmp_memory,
                                           modals)
    elif client_lower == 'rest':
        assert_posix_permissions_in_op_rest(full_path, mode, user, users,
                                            host, hosts)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        assert_posix_permissions_in_op_oneclient(user, full_path, mode,
                                                 oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to set '
               '"(?P<mode>.*)" POSIX permission for item named '
               '"(?P<item_path>.*)" in "(?P<space>.*)" in (?P<host>.*)'))
def set_posix_permissions_in_op(client, user, item_path, space, mode, result,
                                host, selenium, op_container, tmp_memory, modals,
                                users, hosts):
    full_path = '{}/{}'.format(space, item_path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        set_posix_permissions_in_op_gui(selenium, user, space, item_path,
                                        mode, result, op_container, tmp_memory,
                                        modals)
    elif client_lower == 'rest':
        set_posix_permissions_in_op_rest(full_path, mode, user, users, host,
                                         hosts, result)
    elif 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        set_posix_permissions_in_op_oneclient(user, full_path, mode,
                                              oneclient_host, users, result)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) sees that owner\'s UID '
               'and GID for "(?P<path>.*)" in space "(?P<space>[\w-]+)" '
               'are (?P<res>equal|not equal) to (?P<uid>[\d]+) and '
               '(?P<gid>[\d]+) respectively'))
def assert_file_stats(client, user, path, space, uid, gid, res, users):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_file_steps.assert_file_ownership(user, full_path, res, uid, gid,
                                               oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re('using (?P<client>.*), (?P<user>\w+) opens "(?P<path>.*)" '
               'in space "(?P<space>[\w-]+)" in (?P<host>.*)'))
def assert_file_stats(client, user, path, space, users):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if 'oneclient' in client_lower:
        oneclient_host = client_lower.replace('oneclient', 'client')
        multi_reg_file_steps.open(user, full_path, '664', oneclient_host,
                                  users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))
