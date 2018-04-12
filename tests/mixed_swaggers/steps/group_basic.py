"""This module contains gherkin steps to run mixed acceptance tests featuring 
basic operation on groups using web GUI and swagger.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import when, given, then, parsers
from tests.gui.utils.generic import parse_seq
from tests.mixed_swaggers.utils.onezone.group_management import *
from tests.mixed_swaggers.utils.common import NoSuchClientException
from tests.gui.meta_steps.oneprovider.groups import *


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) creates groups? '
                 '(?P<group_list>.*) in "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) creates groups? '
                 '(?P<group_list>.*) in "(?P<host>.*)" Onezone service'))
def create_groups(client, user, group_list, host, hosts, request,
                  users, selenium, op_page, tmp_memory):
    
    if client == "rest":
        create_groups_using_rest(user, users, hosts, group_list, host)
    elif client == "web gui":
        create_groups_using_op_gui(selenium, user, op_page, group_list, tmp_memory)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) sees( that)?'
                 ' groups? named (?P<group_list>.*?)( ha(s|ve) appeared)? in'
                 ' "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees( that)?'
                 ' groups? named (?P<group_list>.*?)( ha(s|ve) appeared)? in'
                 ' "(?P<host>.*)" Onezone service'))
def assert_groups(client, user, group_list, host, hosts, users, selenium, 
                  op_page):

    if client == "rest":
        see_groups_using_rest(user, users, hosts, group_list, host)
    elif client == "web gui":
        see_groups_using_op_gui(selenium, user, op_page, group_list)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))
    

@when(parsers.re('using (?P<client>.*), (?P<user>\w+) renames groups? '
                 '(?P<group_list>.*)to (?P<new_names>.*) in '
                 '"(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) renames groups? '
                 '(?P<group_list>.*) to (?P<new_names>.*) in '
                 '"(?P<host>.*)" Onezone service'))
def rename_groups(client, user, group_list, new_names, host, hosts, users, 
                  selenium, op_page, tmp_memory):
    
    if client == "rest":
        rename_groups_using_rest(user, users, hosts, group_list, new_names, host)
    elif client == "web gui":
        rename_groups_using_op_gui(selenium, user, op_page, group_list, new_names,
                                tmp_memory)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) does not see '
                 'groups? named (?P<group_list>.*) in "(?P<host>.*)" '
                 'Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) does not see '
                 'groups? named (?P<group_list>.*) in "(?P<host>.*)" '
                 'Onezone service'))
def fail_to_see_groups(client, user, group_list, host, hosts, users, 
                       selenium, op_page):

    if client == "rest":
        fail_to_see_groups_using_rest(user, users, hosts, group_list, host)
    elif client == "web gui":
        fail_to_see_groups_using_op_gui(selenium, user, op_page, group_list)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) removes groups? '
                 '(?P<group_list>.*) in "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) removes groups? '
                 '(?P<group_list>.*) in "(?P<host>.*)" Onezone service'))
def remove_groups(client, user, group_list, host, hosts, users, selenium, 
                  op_page):
    
    if client == "rest":
        remove_groups_using_rest(user, users, hosts, group_list, host)
    elif client == "web gui":
        remove_groups_using_op_gui(selenium, user, op_page, group_list)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) leaves groups? '
                 '(?P<group_list>.*) in "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) leaves groups? '
                 '(?P<group_list>.*) in "(?P<host>.*)" Onezone service'))
def leave_groups(client, user, group_list, host, hosts, users, selenium, 
                 op_page, tmp_memory):
    
    if client == "rest":
        leave_groups_using_rest(user, users, hosts, group_list, host)
    elif client == "web gui":
        leave_groups_using_op_gui(selenium, user, op_page, group_list, tmp_memory)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) adds groups? '
                 '(?P<group_list>.*) as subgroup to group "(?P<parent>.*)" in'
                 ' "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) adds groups? '
                 '(?P<group_list>.*) as subgroup to group "(?P<parent>.*)" in'
                 ' "(?P<host>.*)" Onezone service'))
def add_subgroups(client, user, group_list, host, hosts, users, 
                  selenium, op_page, tmp_memory, parent, displays, clipboard):
    
    if client == "rest":
        add_subgroups_using_rest(user, users, hosts, group_list, parent, host)
    elif client == "web gui":
        add_subgroups_using_op_gui(selenium, user, op_page, parent, group_list, 
                                tmp_memory, displays, clipboard)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) removes subgroups? '
                 '(?P<group_list>.*) from group "(?P<parent>.*)" in'
                 ' "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) removes subgroups? '
                 '(?P<group_list>.*) from group "(?P<parent>.*)" in'
                 ' "(?P<host>.*)" Onezone service'))
def remove_subgroups(client, user, group_list, host, hosts, 
                     users, selenium, op_page, tmp_memory, parent):
    
    if client == "rest":
        remove_subgroups_using_rest(user, users, hosts, group_list, parent, host)
    elif client == "web gui":
        remove_subgroups_using_op_gui(selenium, user, op_page, group_list, tmp_memory,
                                   parent)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) sees groups? '
                 '(?P<group_list>.*) as subgroup to group "(?P<parent>.*)" '
                 'in "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) sees groups? '
                 '(?P<group_list>.*) as subgroup to group "(?P<parent>.*)" '
                 'in "(?P<host>.*)" Onezone service'))
def assert_subgroups(client, user, group_list, host, hosts, 
                     users, selenium, op_page, parent):
    
    if client == "rest":
        assert_subgroups_using_rest(user, users, hosts, group_list, parent, host)
    elif client == "web gui":
        assert_subgroups_using_op_gui(selenium, user, op_page, group_list, parent)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) does not see groups? '
                 '(?P<group_list>.*) as subgroup to group "(?P<parent>.*)"'
                 ' in "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) does not see groups? '
                 '(?P<group_list>.*) as subgroup to group "(?P<parent>.*)"'
                 ' in "(?P<host>.*)" Onezone service'))
def fail_to_see_subgroups(client, user, group_list, host, hosts, 
                 users, selenium, op_page, parent):
    
    if client == "rest":
        fail_to_see_subgroups_using_rest(user, users, group_list, parent, hosts,
                                         host)
    elif client == "web gui":
        fail_to_see_subgroups_using_op_gui(selenium, user, op_page, group_list, 
                                           parent)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user1>\w+) invites '
                 '(?P<user2>\w+) to group "(?P<group>.*)" in "(?P<host>.*)" '
                 'Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user1>\w+) invites '
                 '(?P<user2>\w+) to group "(?P<group>.*)" in "(?P<host>.*)" '
                 'Onezone service'))
def invite_to_group(client, user1, user2, group, host, hosts,
                    users, selenium, op_page, tmp_memory, displays, clipboard):
    
    if client == "rest":
        create_group_token_using_rest(user1, user2, group, tmp_memory, users, hosts, host)
    elif client == "web gui":
        create_group_token_using_op_gui(selenium, user1, user2, op_page, group, 
                                     tmp_memory, displays, clipboard)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) joins group he '
                 'was invited to in "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) joins group he '
                 'was invited to in "(?P<host>.*)" Onezone service'))
def join_group(client, user, host, hosts, users, selenium, 
               op_page, tmp_memory):
    
    if client == "rest":
        join_group_using_rest(user, tmp_memory, hosts, users, host)
    elif client == "web gui":
        join_group_using_op_gui(selenium, user, op_page, tmp_memory)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) fails to rename'
                 ' groups? (?P<group_list>.*) to (?P<new_names>.*) in'
                 ' "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) fails to rename'
                 ' groups? (?P<group_list>.*) to (?P<new_names>.*) in'
                 ' "(?P<host>.*)" Onezone service'))
def fail_to_rename_groups(client, user, group_list, host, hosts, users, 
                          selenium, op_page, request,tmp_memory, new_names):

    if client == "rest":
        fail_to_rename_groups_using_rest(user, users, hosts, group_list,
                                         new_names, host)
    elif client == "web gui":
        fail_to_rename_groups_using_op_gui(selenium, user, op_page, group_list,
                                           new_names, tmp_memory)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) fails to remove'
                 ' groups? (?P<group_list>.*?) in "(?P<host>.*)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>\w+) fails to remove'
                 ' groups? (?P<group_list>.*?) in "(?P<host>.*)" Onezone service'))
def fail_to_remove_groups(client, user, group_list, request, host, hosts, users,
                          selenium, op_page, tmp_memory):

    if client == "rest":
        fail_to_remove_groups_using_rest(user, users, hosts, group_list, host)
    elif client == "web gui":
        fail_to_remove_groups_using_op_gui(selenium, user, op_page, group_list,
                                           tmp_memory)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>\w+) fails to join'
                 ' groups? (?P<group_list>.*?) as subgroup to group '
                 '"(?P<parent>.*?)" in "(?P<host>.*)" Onezone service'))
def fail_to_add_subgroups(client, user, group_list, host, hosts, users, 
                          selenium, op_page, parent, tmp_memory, displays, 
                          clipboard):

    if client == "rest":
        fail_to_add_subgroups_using_rest(user, users, hosts, group_list,
                                         parent, host)
    elif client == "web gui":
        fail_to_add_subgroups_using_op_gui(selenium, user, op_page, parent,
                                           group_list, tmp_memory, displays,
                                           clipboard)
    else:
        raise NoSuchClientException("Client: {} not found.".format(client))

