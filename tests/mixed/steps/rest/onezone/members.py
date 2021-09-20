"""Steps for members management creation using REST API.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.mixed.utils.common import login_to_oz
from tests.mixed.onezone_client import SpaceApi
from tests.mixed.onezone_client.rest import ApiException
from tests.mixed.steps.rest.onezone.common import get_group
import yaml

PRIVILEGES_TRANSLATION = {
    'View space': 'space_view',
    'Modify space': 'space_update',
    'Remove space': 'space_delete',
    'View privileges': 'space_view_privileges',
    'Set privileges': 'space_set_privileges',
    'Read files': 'space_read_data',
    'Write files': 'space_write_data',
    'Register files': 'space_register_files',
    'Manage shares': 'space_manage_shares',
    'View database views': 'space_view_views',
    'Manage database views': 'space_manage_views',
    'Query database views': 'space_query_views',
    'View statistics': 'space_view_statistics',
    'View changes stream': 'space_view_changes_stream',
    'View transfers': 'space_view_transfers',
    'Schedule replication': 'space_schedule_replication',
    'Cancel replication': 'space_cancel_replication',
    'Schedule eviction': 'space_schedule_eviction',
    'Cancel eviction': 'space_cancel_eviction',
    'View QoS': 'space_view_qos',
    'Manage QoS': 'space_manage_qos',
    'Add user': 'space_add_user',
    'Remove user': 'space_remove_user',
    'Add group': 'space_add_group',
    'Remove group': 'space_remove_group',
    'Add support': 'space_add_provider',
    'Remove support': 'space_remove_provider',
    'Add harvester': 'space_add_harvester',
    'Remove harvester': 'space_remove_harvester',
    'Manage datasets': 'space_manage_datasets',
    'View archives': 'space_view_archives',
    'Create archives': 'space_create_archives',
    'Remove archives': 'space_remove_archives',
    'Recall archives': 'space_recall_archives',
    'View workflow executions': 'space_view_atm_workflow_executions',
    'Schedule workflow executions': 'space_schedule_atm_workflow_executions',
    'Cancel workflow executions': 'space_cancel_atm_workflow_executions'
}

PRIVILEGES_GROUPS = {
    'Space management': ['View space', 'Modify space', 'Remove space',
                         'View privileges', 'Set privileges'],
    'Data management': ['Read files', 'Write files', 'Register files',
                        'Manage shares', 'View database views',
                        'Manage database views', 'Query database views',
                        'View statistics', 'View changes stream'],
    'Transfer management': ['View transfers', 'Schedule replication',
                            'Cancel replication', 'Schedule eviction',
                            'Cancel eviction'],
    'QoS management': ['View QoS', 'Manage QoS'],
    'User management': ['Add user', 'Remove user'],
    'Group management': ['Add group', 'Remove group'],
    'Support management': ['Add support', 'Remove support'],
    'Harvester management': ['Add harvester', 'Remove harvester'],
    'Dataset & archive management': ['Manage datasets', 'View archives',
                                     'Create archives', 'Remove archives',
                                     'Recall archives'],
    'Automation management': ['View workflow executions',
                              'Schedule workflow executions',
                              'Cancel workflow executions']
}

DEFAULT_GRANT = ['space_read_data', 'space_view', 'space_view_transfers',
                 'space_write_data']


def translate_privileges(config, grant, revoke):
    privileges = yaml.load(config)
    for (privileges_group, privileges_group_items) in privileges.items():
        if privileges_group_items['granted'] == 'Partially':
            items = privileges_group_items['privilege subtypes'].items()
            for (privilege, granted) in items:
                if granted:
                    if privilege not in grant:
                        grant.append(privilege)
                else:
                    revoke.append(privilege)
        elif not privileges_group_items['granted']:
            revoke.extend(PRIVILEGES_GROUPS[privileges_group])
        else:
            grant.extend(PRIVILEGES_GROUPS[privileges_group])

    for i in range(len(grant)):
        grant[i] = PRIVILEGES_TRANSLATION[grant[i]]
    for i in range(len(revoke)):
        revoke[i] = PRIVILEGES_TRANSLATION[revoke[i]]

    for privilege in DEFAULT_GRANT:
        if privilege not in revoke and privilege not in grant:
            grant.append(privilege)


def fail_to_set_privileges_using_rest(user, users, hosts, host, spaces,
                                      space_name, member_name, config):
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts[host]['hostname'])
    space_api = SpaceApi(user_client_oz)
    grant = []
    revoke = []
    translate_privileges(config, grant, revoke)
    data = {"grant": grant, "revoke": revoke}
    try:
        space_api.update_user_space_privileges(spaces[space_name],
                                               users[member_name].id, data)
        raise Exception('function: space_api.update_user_space_privileges'
                        ' worked but it should not, because of lack in '
                        'privileges')
    except ApiException as err:
        if err.status == 403:
            pass


def assert_privileges_in_space_using_rest(user, users, hosts, host, spaces,
                                          space_name, member_name, config):
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts[host]['hostname'])
    space_api = SpaceApi(user_client_oz)

    user_privileges = (space_api.list_user_space_privileges(
        spaces[space_name], users[member_name].id).to_dict()['privileges'])
    grant = []
    revoke = []
    translate_privileges(config, grant, revoke)
    grant.sort()
    user_privileges.sort()
    assert grant == user_privileges, (
        f'users privileges {user_privileges} does not match expected '
        f'privileges: {grant}')


def fail_to_create_invitation_in_space_using_rest(user, users, hosts, host,
                                                  spaces, space_name,
                                                  member_name):
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts[host]['hostname'])
    space_api = SpaceApi(user_client_oz)
    try:
        space_api.add_space_user(spaces[space_name], users[member_name].id)
        raise Exception('function: space_api.add_space_user worked but it'
                        ' should not, because of lack in privileges')
    except ApiException as err:
        if err.status == 403:
            pass


def assert_not_user_in_space_using_rest(user, users, hosts, host, spaces,
                                        space_name, member_name):
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts[host]['hostname'])
    space_api = SpaceApi(user_client_oz)
    users_id_list = (space_api.list_space_users(spaces[space_name])
                     .to_dict()['users'])
    assert users[member_name].id not in users_id_list, (
        f'user {member_name} is in space {space_name}')


def add_group_to_space_using_rest(user, users, hosts, host, group_name, spaces,
                                  space_name):
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts[host]['hostname'])
    space_api = SpaceApi(user_client_oz)
    group = get_group(group_name, user_client_oz)
    space_api.add_group_to_space(spaces[space_name], group.group_id)


def assert_group_in_space_using_rest(user, users, hosts, host, group_name,
                                     spaces, space_name):
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts[host]['hostname'])
    space_api = SpaceApi(user_client_oz)
    group = get_group(group_name, user_client_oz).to_dict()['group_id']
    space_groups = space_api.list_space_groups(spaces[space_name]).to_dict()[
        'groups']
    err_msg = f'"{group_name}" not in space "{space_name}" members page'
    assert group in space_groups, err_msg

