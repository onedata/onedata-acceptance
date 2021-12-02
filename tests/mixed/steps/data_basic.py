"""This module contains gherkin steps to run mixed acceptance tests featuring
basic operations on data using web GUI and REST.
"""

__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.oneprovider.data import *
from tests.gui.steps.oneprovider.browser import double_click_on_item_in_browser
from tests.gui.meta_steps.oneprovider.metadata import (
    assert_metadata_in_op_gui, set_metadata_in_op_gui,
    remove_all_metadata_in_op_gui, assert_such_metadata_not_exist_in_op_gui)
from tests.gui.meta_steps.oneprovider.permissions import *
from tests.mixed.steps.oneclient.data_basic import *
from tests.mixed.steps.rest.oneprovider.data import *
from tests.mixed.steps.rest.oneprovider.metadata import *
from tests.utils.bdd_utils import wt, parsers
from tests.utils.path_utils import get_first_path_element


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create '
               'file named "(?P<name>.*)" in "(?P<space>.*)" in (?P<host>.*)'))
def create_file_in_op(client, user, users, space, name, hosts, tmp_memory, host,
                      selenium, op_container, result, modals, oz_page):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_item_in_op_gui(selenium, user, os.path.dirname(name),
                              'file', os.path.basename(name),
                              tmp_memory, op_container, result, space,
                              modals, oz_page)
    elif client_lower == 'rest':
        create_file_in_op_rest(user, users, host, hosts, full_path, result)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        create_file_in_op_oneclient(user, full_path, users, result,
                                    oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create '
               'file named "(?P<name>.*)" using received token in '
               '"(?P<space>.*)" in (?P<host>.*)'))
def create_file_in_op_with_token(client, user, users, space, name, hosts,
                                 tmp_memory, host, result, env_desc):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'rest':
        token = tmp_memory[user]['mailbox'].get('token', None)
        create_file_in_op_rest(user, users, host, hosts, full_path, result,
                               token)
    elif 'oneclient' in client_lower:
        create_file_in_op_oneclient_with_tokens(user, hosts, users, env_desc, tmp_memory,
                                                result, full_path, client_lower)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to see '
               r'item named "(?P<name>.*)" using received access token in '
               r'"(?P<space>.*)" in (?P<host>.*)'))
def assert_file_in_op_with_token(client, user, name, space, host, tmp_memory,
                                 users, hosts, env_desc, result):

    client_lower = client.lower()
    if client_lower == 'rest':
        see_item_in_op_rest_using_token(user, name, space, host, tmp_memory,
                                        users, hosts, result)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        see_items_in_op_oneclient(name, space, user, users, result,
                                  oneclient_host)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re(r'using (?P<client>.*) with identity token, (?P<user>\w+) ('
               r'?P<result>\w+) to create file named "(?P<name>.*)" using '
               'received token in "(?P<space>.*)" in (?P<host>.*)'))
def create_file_in_op_with_tokens(client, user, users, space, name, hosts,
                                  tmp_memory, host, result, env_desc, tokens):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'rest':
        access_token = tmp_memory[user]['mailbox'].get('token', None)
        identity_token = tokens[f'identity_token_of_{user}'].get('token', None)
        create_file_in_op_rest(user, users, host, hosts, full_path, result,
                               access_token=access_token,
                               identity_token=identity_token)
    elif 'oneclient' in client_lower:
        create_file_in_op_oneclient_with_tokens(user, hosts, users, env_desc,
                                                tmp_memory, result, full_path,
                                                client_lower)

    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to create '
               'directory named "/(?P<abs_path>.*)" in "(?P<space>.*)" in '
               '(?P<host>.*)'))
def create_dir_in_op(client, user, users, space, abs_path, hosts, tmp_memory,
                     host, selenium, op_container, result, modals, oz_page):
    full_path = '{}/{}'.format(space, abs_path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        if '/' in abs_path:
            go_to_filebrowser(selenium, user, oz_page, op_container,
                              tmp_memory, space)
            go_to_path_without_last_elem(selenium, user, tmp_memory, abs_path,
                                         op_container)
            create_item_in_op_gui(selenium, user, '',
                                  'directory', os.path.basename(abs_path),
                                  tmp_memory, op_container, result, space,
                                  modals, oz_page)
            change_cwd_using_breadcrumbs_in_data_tab_in_op(selenium, user,
                                                           'home',
                                                           op_container)
        else:
            create_item_in_op_gui(selenium, user, os.path.dirname(abs_path),
                                  'directory', os.path.basename(abs_path),
                                  tmp_memory, op_container, result, space,
                                  modals, oz_page)
    elif client_lower == 'rest':
        create_dir_in_op_rest(user, users, host, hosts, full_path, result)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        create_dir_in_op_oneclient(user, full_path, users, result,
                                   oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using web GUI, (?P<user>\w+) double clicks on item '
               'named "(?P<item_name>.*)" in "(?P<space>.*)"'))
def go_to_dir(selenium, user, item_name, tmp_memory, op_container, space,
              oz_page):
    go_to_filebrowser(selenium, user, oz_page, op_container,
                      tmp_memory, space)
    double_click_on_item_in_browser(selenium, user, item_name, tmp_memory,
                                    op_container)


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to see '
               'item named (?P<name>.*) in "(?P<space>.*)" in '
               '(?P<host>.*)'))
def see_item_in_op(client, user, users, result, name, space, host, hosts,
                   selenium, tmp_memory, op_container, oz_page):
    client_lower = client.lower()
    if client_lower == 'web gui':
        item_name = name
        name_list = name.replace('"', '')
        path = ''
        if '/' in name_list:
            item_name = name_list.split('/')[-1]
            path = name_list.replace(item_name, '')[:-1]

        see_items_in_op_gui(selenium, user, path, item_name, tmp_memory,
                            op_container, result, space, oz_page)
    elif client_lower == 'rest':
        see_items_in_op_rest(user, users, host, hosts, name,
                             result, space)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        see_items_in_op_oneclient(name, space, user, users, result,
                                  oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to '
               r'remove directory \(rmdir\) named "(?P<name>.*)" in '
               '"(?P<space>.*)" in (?P<host>.*)'))
def remove_empty_dir_in_op(client, user, users, result, space, name, hosts,
                           selenium, op_container, tmp_memory, host,
                           modals, oz_page):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_item_in_op_gui(selenium, user, name, tmp_memory, op_container, 
                              'succeds', space, modals, oz_page)
    elif client_lower == 'rest':
        remove_dir_in_op_rest(user, users, host, hosts, full_path)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        delete_empty_directory_in_op_oneclient(full_path, user, users, result,
                                               oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) removes directory '
               r'\(rmdir -p\) named "(?P<name>.*)" in "(?P<space>.*)" in '
               '(?P<host>.*)'))
def remove_empty_dir_and_parents_in_op(client, user, users, space, name, hosts,
                                       selenium, op_container, tmp_memory,
                                       host, modals, oz_page):
    first_path_elem = get_first_path_element(name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_dir_and_parents_in_op_gui(selenium, user, first_path_elem,
                                         tmp_memory, op_container, 'succeds',
                                         space, modals, oz_page)
    elif client_lower == 'rest':
        remove_dir_in_op_rest(user, users, host, hosts,
                              '{}/{}'.format(space, first_path_elem))
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_dir_steps.delete_parents(user, '{}/{}'.format(space, name),
                                       oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) removes directory '
               r'\(rm -rf\) named "(?P<name>.*)" in "(?P<space>.*)" in '
               '(?P<host>.*)'))
def remove_dir_in_op(client, user, users, space, name, hosts, selenium,
                     op_container, tmp_memory, host, modals, oz_page):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_item_in_op_gui(selenium, user, name, tmp_memory, op_container,
                              'succeds', space, modals, oz_page)
    elif client_lower == 'rest':
        remove_dir_in_op_rest(user, users, host, hosts, full_path)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_dir_steps.delete_non_empty(user, full_path, oneclient_host,
                                         users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) '
               'to remove file named "(?P<name>.*)" in "(?P<space>.*)" in '
               '(?P<host>.*)'))
def remove_file_in_op(client, user, name, space, host, users, hosts,
                      tmp_memory, selenium, op_container, result,
                      modals, oz_page):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'web gui':
        remove_item_in_op_gui(selenium, user, name, tmp_memory, op_container, 
                              result, space, modals, oz_page)
    elif client_lower == 'rest':
        remove_file_in_op_rest(user, users, host, hosts, full_path, result)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        remove_file_in_op_oneclient(user, full_path, oneclient_host,
                                    users, result)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) '
               'to remove file named "(?P<name>.*)" using received token in '
               '"(?P<space>.*)" in (?P<host>.*)'))
def remove_file_using_token_in_op(client, user, name, space, host, users, hosts,
                                  tmp_memory, result, env_desc):
    full_path = '{}/{}'.format(space, name)
    client_lower = client.lower()
    if client_lower == 'rest':
        remove_file_using_token_in_op_rest(user, users, host, hosts, full_path,
                                           result, tmp_memory)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        remove_file_in_op_oneclient(user, full_path, oneclient_host,
                                    users, result)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) '
               r'renames item named "(?P<old_name>.*)" to "(?P<new_name>.*)" '
               r'in "(?P<space>.*)" in (?P<host>.*)'))
def rename_item_in_op(client, user, users, space, old_name, new_name,
                      hosts, tmp_memory, host, selenium, op_container, cdmi,
                      modals, oz_page):
    old_path = '{}/{}'.format(space, old_name)
    new_path = '{}/{}'.format(space, new_name)
    client_lower = client.lower()
    result = 'succeeds'
    if client_lower == 'web gui':
        rename_item(selenium, user, old_name, new_name, tmp_memory,
                    result, space, modals, oz_page, op_container)
    elif client_lower == 'rest':
        move_item_in_op_rest(old_path, new_path, result, cdmi, host, hosts,
                             user, users)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.rename(user, old_path, new_path, oneclient_host,
                                users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) '
               r'renames item named "(?P<old_name>.*)" to "(?P<new_name>.*)" '
               r'using received access token in "(?P<space>.*)" '
               r'in (?P<host>.*)'))
def rename_item_in_op_using_token(client, user, users, space, old_name,
                                  new_name, hosts, tmp_memory, host, cdmi, env_desc):
    old_path = f'{space}/{old_name}'
    new_path = f'{space}/{new_name}'
    client_lower = client.lower()

    if client_lower == 'rest':
        result = 'succeds'
        move_item_in_op_rest_using_token(old_path, new_path, result, host,
                                         hosts, user, users, tmp_memory, cdmi)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.rename(user, old_path, new_path, oneclient_host,
                                users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that there '
               r'(is 1|are (?P<num>\d+)) items? in "(?P<space>.*)" in '
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
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_num_of_files_in_path_in_op_oneclient(num, space, user, users,
                                                    oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) writes "(?P<text>.*)" '
               r'to file named "(?P<file_name>.*)" in '
               r'"(?P<space>.*)" in (?P<host>.*)'))
def write_to_file_in_op(client, user, text, file_name, space, host, users,
                        hosts, cdmi):
    full_path = '{}/{}'.format(space, file_name)
    client_lower = client.lower()
    if client_lower == 'rest':
        write_to_file_in_op_rest(user, users, host, hosts, cdmi, full_path,
                                 text)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_reg_file_steps.write_text(user, text, full_path, oneclient_host,
                                        users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) reads "(?P<text>.*)" '
               'from file named "(?P<file_name>.*)" in '
               '"(?P<space>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
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
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_reg_file_steps.read_text(user, text, full_path, oneclient_host,
                                       users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) appends "(?P<text>.*)" '
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
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_reg_file_steps.append(user, text, full_path, oneclient_host,
                                    users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) replaces '
               '"(?P<old_text>.*)" with "(?P<new_text>.*)" '
               'in file named "(?P<file_name>.*)" in '
               '"(?P<space>.*)" in (?P<host>.*)'))
def replace_in_file_in_op(client, user, old_text, new_text, file_name, space,
                          host, users):
    full_path = '{}/{}'.format(space, file_name)
    client_lower = client.lower()
    if 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_reg_file_steps.replace(user, old_text, new_text, full_path,
                                     oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to move '
               '"(?P<src_path>.*)" to "(?P<dst_path>.*)" '
               'in (?P<host>.*)'))
def move_file_in_op(client, user, result, src_path, dst_path, host, users,
                    cdmi, hosts):
    client_lower = client.lower()
    if client_lower == 'rest':
        move_item_in_op_rest(src_path, dst_path, result, cdmi, host, hosts,
                             user, users)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        move_item_in_op_oneclient(user, src_path, dst_path, users, result,
                                  oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) copies '
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
        oneclient_host = change_client_name_to_hostname(client_lower)
        copy_item_in_op_oneclient(item_type, src_path, dst_path,
                                  user, users, oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) creates directory '
               'structure in "(?P<space>.*)" space on (?P<host>.*) '
               r'as follow:\n(?P<config>(.|\s)*)'))
def create_directory_structure_in_op(selenium, user, op_container, config, space, 
                                     tmp_memory, users, hosts, host, client,
                                     modals, oz_page, popups):
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_directory_structure_in_op_gui(selenium, user, op_container, 
                                             config, space, tmp_memory,
                                             modals, oz_page, popups)
    elif client_lower == 'rest':
        create_directory_structure_in_op_rest(user, users, hosts, host,
                                              config, space)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        create_directory_structure_in_op_oneclient(user, users, config, space,
                                                   oneclient_host, hosts)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))

    tmp_memory['config'] = config


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that (?P<time1>.*) '
               'time of item named "(?P<file_name>.*)" in "(?P<space>.*)" '
               'space is (?P<comparator>.*) '
               '(?P<time2>.*) time in (?P<host>.*)'))
def assert_time_relation(user, time1, file_name, space, comparator, time2,
                         client, users, host, hosts, cdmi):
    client_lower = client.lower()
    full_path = '{}/{}'.format(space, file_name)
    comparator = re.sub(r'( than| to)', '', comparator)
    if client_lower == 'rest':
        assert_time_relation_in_op_rest(full_path, time1, time2, comparator,
                                        host, hosts, user, users, cdmi)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.check_time(user, time1, time2, comparator, full_path,
                                    oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that (?P<time1>.*) '
               'time of item named "(?P<file_name>.*)" is (?P<comparator>.*) '
               '(than|to) (?P<time2>.*) time of item named '
               '"(?P<file2_name>.*)" in "(?P<space>.*)" space in (?P<host>.*)'))
def assert_files_time_relation(user, time1, file_name, space, comparator, time2,
                               client, file2_name, users, host, hosts, cdmi):
    client_lower = client.lower()
    full_path = '{}/{}'.format(space, file_name)
    full_path2 = '{}/{}'.format(space, file2_name)
    if client_lower == 'rest':
        assert_files_time_relation_in_op_rest(full_path, full_path2, time1,
                                              time2, comparator, host, hosts,
                                              user, users, cdmi)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.check_files_time(user, time1, time2, comparator,
                                          full_path, full_path2,
                                          oneclient_host, users)
    else:
        raise NoSuchClientException(f'Client: {client} is not supported '
                                    f'for this assertion')


@wt(parsers.re('using (?P<client>.*), (?P<user>.*) sees that '
               '(?P<time_name>.*) time of item named "(?P<file_path>.*)" '
               'in current space is not earlier than '
               '(?P<time>[0-9]*) seconds ago in (?P<host>.*)'))
def assert_mtime_not_earlier_than(client, file_path, selenium, user,
                                  op_container, time, tmp_memory):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_mtime_not_earlier_than_op_gui(file_path, time, user, tmp_memory,
                                             selenium, op_container)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that directory '
               'structure in "(?P<space>.*)" space in (?P<host>.*) is as '
               'previously created'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_directory_structure_in_op(client, selenium, user, op_container, oz_page,
                                     tmp_memory, tmpdir, space, host, spaces,
                                     hosts, users, modals):
    config = tmp_memory['config']
    client_lower = client.lower()

    if client_lower == 'web gui':
        assert_space_content_in_op_gui(config, selenium, user, op_container,
                                       tmp_memory, tmpdir, space, oz_page, host,
                                       hosts)
    elif client_lower == 'rest':
        assert_space_content_in_op_rest(user, users, hosts, config, space,
                                        spaces, host)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_space_content_in_op_oneclient(config, space, user, users,
                                             oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that directory '
               r'structure in "(?P<space>.*)" space in (?P<host>.*) is as '
               r'follow:\n(?P<config>(.|\s)*)'))
def assert_directory_structure_in_op(client, selenium, user, op_container, oz_page,
                                     tmp_memory, tmpdir, space, host, spaces,
                                     hosts, users, config, modals):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_space_content_in_op_gui(config, selenium, user, op_container,
                                       tmp_memory, tmpdir, space, oz_page,
                                       host, hosts)
    elif client_lower == 'rest':
        assert_space_content_in_op_rest(user, users, hosts, config, space,
                                        spaces, host)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_space_content_in_op_oneclient(config, space, user, users,
                                             oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sets new '
               '(?P<tab_name>.*) metadata: (?P<val>.*) for "(?P<path>.*?)"'
               ' (?P<item>file|directory) in space "(?P<space>.*)" '
               'in (?P<host>.*)'))
def set_metadata_in_op(client, selenium, user, tab_name, val, cdmi, op_container,
                       space, path, host, hosts, users, tmp_memory, modals,
                       oz_page, item):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        tab_name = tab_name.upper() if tab_name != 'basic' else tab_name
        set_metadata_in_op_gui(selenium, user, path, tmp_memory, op_container, 's',
                               space, tab_name, val, modals, oz_page, item)
    elif client_lower == 'rest':
        set_metadata_in_op_rest(user, users, host, hosts, cdmi, full_path,
                                tab_name, val)
    elif 'oneclient' in client_lower:
        if tab_name.lower() == 'rdf':
            val = val.replace('"', '\\"')
            val = '"' + val + '"'
        oneclient_host = change_client_name_to_hostname(client_lower)
        set_metadata_in_op_oneclient(val, tab_name, full_path, user, users,
                                     oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that '
               '(?P<tab_name>.*) metadata for "(?P<path>.*?)" '
               '(?P<item>file|directory) is '
               '(?P<val>.*) in space "(?P<space>.*)" in (?P<host>.*)'))
def assert_metadata_in_op(client, selenium, user, tab_name, val, cdmi, op_container,
                          space, path, host, hosts, users, tmp_memory, item, modals,
                          oz_page):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if client_lower == 'web gui':
        tab_name = tab_name.upper() if tab_name != 'basic' else tab_name
        assert_metadata_in_op_gui(selenium, user, path, tmp_memory, op_container,
                                  's', space, tab_name, val, modals, oz_page,
                                  item)
    elif client_lower == 'rest':
        assert_metadata_in_op_rest(user, users, host, hosts, cdmi,
                                   full_path, tab_name, val)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_metadata_in_op_oneclient(val, tab_name, full_path, user, users,
                                        oneclient_host)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) removes all '
               r'"(?P<path>.*)" (?P<item>file|directory) '
               r'metadata in space "(?P<space>\w+)" '
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
        oneclient_host = change_client_name_to_hostname(client_lower)
        remove_all_metadata_in_op_oneclient(user, users, oneclient_host,
                                            full_path)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that '
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
        tab_name = tab_name.upper() if tab_name != 'basic' else tab_name
        assert_such_metadata_not_exist_in_op_gui(selenium, user, path,
                                                 tmp_memory, op_container,
                                                 space, tab_name, val, modals,
                                                 oz_page, item)
    elif client_lower == 'rest':
        assert_no_such_metadata_in_op_rest(user, users, host, hosts, cdmi,
                                           full_path, tab_name, val)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_no_such_metadata_in_op_oneclient(user, users, oneclient_host,
                                                full_path, tab_name, val)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) uploads "(?P<path>.*)" '
               'to "(?P<space>.*)" in (?P<host>.*)'))
def upload_file_to_op(client, selenium, user, path, space, host, hosts,
                      tmp_memory, op_container, oz_page, popups):
    client_lower = client.lower()
    if client_lower == 'web gui':
        successfully_upload_file_to_op_gui(path, selenium, user, space,
                                           op_container, tmp_memory, oz_page,
                                           popups)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) uploads local file '
               r'"(?P<path>.*)" to "(?P<space>.*)"'))
def upload_local_file_to_op(client, selenium, user, path, tmpdir,
                            op_container, popups, space, oz_page,
                            tmp_memory):
    client_lower = client.lower()
    if client_lower == 'web gui':
        go_to_filebrowser(selenium, user, oz_page, op_container,
                          tmp_memory, space)
        upload_file_to_cwd_in_data_tab(selenium, user, path, tmpdir,
                                       op_container, popups)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that owner\'s UID '
               r'and GID for "(?P<path>.*)" in space "(?P<space>[\w-]+)" '
               r'are (?P<res>equal|not equal) to (?P<uid>[\d]+) and '
               r'(?P<gid>[\d]+) respectively'))
def assert_file_stats(client, user, path, space, uid, gid, res, users):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.assert_file_ownership(user, full_path, res, uid, gid,
                                               oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that owner\'s UID '
               r'for "(?P<path>.*)" in space "(?P<space>.*)" '
               r'is (?P<res>equal|not equal) to (?P<uid>.*)'))
def assert_file_uid_stat(client, user, path, space, uid, res, users):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_file_steps.assert_file_uid(user, full_path, res, uid,
                                         oneclient_host, users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) opens "(?P<path>.*)" '
               r'in space "(?P<space>[\w-]+)" in (?P<host>.*)'))
def assert_file_stats(client, user, path, space, users):
    full_path = '{}/{}'.format(space, path)
    client_lower = client.lower()
    if 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        multi_reg_file_steps.open(user, full_path, '664', oneclient_host,
                                  users)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.parse('using web GUI, {user} sees that {owner} is owner of '
                  '"{file_name}"'))
def check_file_owner_web_gui(selenium, user, owner, file_name, tmp_memory,
                             modals):
    check_file_owner(selenium, user, owner, file_name, tmp_memory, modals)
