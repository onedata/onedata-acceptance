"""This module contains gherkin steps for group management rest tests in Onezone.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import pytest

from tests.gui.utils.generic import parse_seq
from tests.mixed.onezone_client import UserApi, GroupCreateRequest, GroupApi
from tests.mixed.onezone_client.rest import ApiException
from tests.mixed.steps.rest.onezone.common import get_group
from tests.mixed.utils.common import login_to_oz
from tests.utils.bdd_utils import parsers, wt


@wt(parsers.re('(?P<user>\w+) creates groups? (?P<group_list>.*) using '
               'REST'))
def create_groups_using_rest(user, users, hosts, group_list, host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    user_api = UserApi(user_client)

    for group_name in parse_seq(group_list):
        user_api.create_user_group(GroupCreateRequest(name=group_name))


@wt(parsers.re('(?P<user>\w+) sees groups? (?P<group_list>.*) using REST'))
def see_groups_using_rest(user, users, hosts, group_list, host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    for group_name in parse_seq(group_list):
        assert get_group(group_name, user_client), 'There is no ' \
                                            'group named {}'.format(group_name)


@wt(parsers.re(r'(?P<user>\w+) does not see groups? (?P<group_list>.*) '
               'using REST'))
def fail_to_see_groups_using_rest(user, users, hosts, group_list, host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    for group_name in parse_seq(group_list):
        assert not get_group(group_name, user_client), 'There is ' \
                                            'group named {}'.format(group_name)


@wt(parsers.re(r'(?P<user>\w+) renames groups? (?P<group_list>.*) to'
               ' (?P<new_names>.*) using REST'))
def rename_groups_using_rest(user, users, hosts, group_list, new_names,
                             host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    for group_name, new_name in zip(parse_seq(group_list), parse_seq(new_names)):
        group = get_group(group_name, user_client)
        data = {'name': new_name}
        group_api.modify_group(group.group_id, data)


@wt(parsers.re('(?P<user>\w+) fails to rename groups? (?P<group_list>.*)'
               ' to (?P<new_names>.*) using REST'))
def fail_to_rename_groups_using_rest(user, users, hosts, group_list, new_names,
                                     host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    for group_name, new_name in zip(parse_seq(group_list), parse_seq(new_names)):
        group = get_group(group_name, user_client)
        data = {'name': new_name}
        with pytest.raises(ApiException, message = 'Renaming group {} to {} ' \
                           'did not fail'.format(group_name, new_name)):
            group_api.modify_group(group.group_id, data)


@wt(parsers.re('(?P<user>\w+) fails to remove groups? (?P<group_list>.*)'
               ' using REST'))
def fail_to_remove_groups_using_rest(user, users, hosts, group_list,
                                     host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    for group_name in parse_seq(group_list):
        group = get_group(group_name, user_client)
        with pytest.raises(ApiException, message = 'Removing group {} did '
                           'not fail'.format(group_name)):
            group_api.remove_group(group.group_id)


@wt(parsers.re('(?P<user>\w+) removes groups? (?P<group_list>.*) using'
               ' REST'))
def remove_groups_using_rest(user, users, hosts, group_list, user_clients,
                             host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    for group_name in parse_seq(group_list):
        group = get_group(group_name, user_client)
        group_api.remove_group(group.group_id)


@wt(parsers.re(r'(?P<user>\w+) leaves groups? (?P<group_list>.*) using '
               'REST'))
def leave_groups_using_rest(user, users, hosts, group_list, host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    user_api = UserApi(user_client)
    for group_name in parse_seq(group_list):
        group = get_group(group_name, user_client)
        user_api.leave_group(group.group_id)


@wt(parsers.re(r'(?P<user>\w+) adds groups? (?P<group_list>.*) as subgroup'
               ' to group "(?P<parent>.*)" using REST'))
def add_subgroups_using_rest(user, users, hosts, group_list, parent,
                             host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    for group_name in parse_seq(group_list):
        parent_id = get_group(parent, user_client).group_id
        child_id = get_group(group_name, user_client).group_id
        token = group_api.create_child_group_token(parent_id)
        group_api.join_parent_group(child_id, data=token)


def fail_to_add_subgroups_using_rest(user, users, hosts, group_list, parent, 
                                    host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    for group_name in parse_seq(group_list):
        parent_id = get_group(parent, user_client).group_id
        child_id = get_group(group_name, user_client).group_id
        token = group_api.create_child_group_token(parent_id)
        with pytest.raises(ApiException, message = 'Adding group {} as' \
                    ' subgroup to {} did not fail'.format(group_name, parent)):
            group_api.join_parent_group(child_id, data=token)


@wt(parsers.re(r'(?P<user1>\w+) invites (?P<user2>\w+) to join group'
               ' "(?P<group_name>.*)" using REST'))
def create_group_token_using_rest(user1, user2, group_name, tmp_memory, users,
                                  hosts, host='onezone'):
    user_client = login_to_oz(user1, users[user1].password, hosts[host]['hostname'])
    group = get_group(group_name, user_client)
    group_api = GroupApi(user_client)
    token = group_api.create_user_group_invite_token(group.group_id)
    tmp_memory[user2]['mailbox']['token'] = token.token


@wt(parsers.re(r'(?P<user>\w+) joins group he was invited to using REST'))
def join_group_using_rest(user, tmp_memory, hosts, users, host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    data = {'token': tmp_memory[user]['mailbox']['token']}
    UserApi(user_client).join_group(data)


@wt(parsers.re(r'(?P<user>\w+) using REST sees that users? (?P<user_list>.*) '
               'belongs? to groups? (?P<group_list>.*)'))
def assert_users_in_groups_using_rest(user, user_list, group_list, users, hosts,
                                      host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    for group_name in parse_seq(group_list):
        group = get_group(group_name, user_client)
        users_id = group_api.list_group_users(group.group_id).users

        for user_name in parse_seq(user_list):
            assert users[user_name].id in users_id


@wt(parsers.re(r'(?P<user>\w+) sees groups? (?P<group_list>.*) as subgroup'
               ' to group "(?P<parent>.*)" using REST'))
def assert_subgroups_using_rest(user, users, hosts, group_list, parent,
                                host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    subgroups = group_api.list_child_groups(get_group(parent, user_client).group_id)
    subgroups_names = [group.name for group in [group_api.get_group(g) \
                       for g in subgroups.groups]]
    for child in parse_seq(group_list):
        assert child in subgroups_names


@wt(parsers.re(r'(?P<user>\w+) removes groups? (?P<group_list>.*) as '
               r'subgroup of group "(?P<parent_name>.*)" using REST'))
def remove_subgroups_using_rest(user, users, hosts, group_list,
                                        parent_name, host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    parent = get_group(parent_name, user_client)
    for group_name in parse_seq(group_list):
        group = get_group(group_name, user_client)
        group_api.remove_child_group(parent.group_id,group.group_id)


@wt(parsers.re(r'(?P<user>\w+) fails to see groups? (?P<group_list>.*) as '
               'subgroup to group "(?P<parent>.*)" using REST'))
def fail_to_see_subgroups_using_rest(user, users, group_list, parent, hosts,
                                     host='onezone'):
    user_client = login_to_oz(user, users[user].password, hosts[host]['hostname'])
    group_api = GroupApi(user_client)
    subgroups = group_api.list_child_groups(get_group(parent, user_client).group_id)
    subgroups_names = [group.name for group in [group_api.get_group(g) \
                       for g in subgroups.groups]]
    for child in parse_seq(group_list):
        assert child not in subgroups_names
