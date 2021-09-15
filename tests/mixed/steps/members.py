"""This module contains gherkin steps to run acceptance tests featuring members
management in Onezone using REST API mixed with web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.steps.modal import (
    assert_error_modal_with_text_appeared, assert_alert_text_in_modal)
from tests.gui.steps.onezone.members import (
    set_privileges_in_members_subpage, click_element_in_members_list,
    assert_privileges_in_members_subpage, click_on_option_in_members_list_menu,
    assert_member_is_in_parent_members_list)
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu)
from tests.mixed.utils.common import NoSuchClientException, login_to_oz
from tests.mixed.onezone_client import SpaceApi
from tests.mixed.onezone_client.rest import ApiException
import yaml


privileges_translation = {
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

privileges_groups = {
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


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) fails to set following '
               'privileges for "(?P<member_name>.*)" '
               '(?P<member_type>user|group) in space "(?P<space_name>.*)" in '
               r'"(?P<host>.+?)" Onezone service:\n(?P<config>(.|\s)*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_set_privileges_in_space_in_oz(client, user, member_name,
                                          member_type, config, hosts, selenium,
                                          onepanel, oz_page, space_name, users,
                                          spaces, host):
    client_lower = client.lower()
    if client_lower == 'web gui':
        option = 'Members'
        list_type = 'users'
        where = 'space'
        text = 'insufficient privileges'
        click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                      space_name, option,
                                                      oz_page)
        click_element_in_members_list(selenium, user, member_name,
                                      oz_page, where, list_type, onepanel)
        set_privileges_in_members_subpage(selenium, user, member_name,
                                          member_type, where, config, onepanel,
                                          oz_page)
        assert_error_modal_with_text_appeared(selenium, user, text)
    elif client_lower == 'rest':
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

    else:
        raise NoSuchClientException(f'Client: {client} not found')


def translate_privileges(config, grant, revoke):
    privileges = yaml.load(config)
    for (privileges_group, privileges_group_items) in privileges.items():
        if privileges_group_items['granted'] == 'Partially':
            items = privileges_group_items['privilege subtypes'].items()
            for (privilege, granted) in items:
                if granted:
                    grant.append(privilege)
                else:
                    revoke.append(privilege)
        elif not privileges_group_items['granted']:
            revoke.extend(privileges_groups[privileges_group])
        else:
            grant.extend(privileges_groups[privileges_group])

    for i in range(len(grant)):
        grant[i] = privileges_translation[grant[i]]
    for i in range(len(revoke)):
        revoke[i] = privileges_translation[revoke[i]]


@wt(parsers.re(r'using (?P<client>.*), (?P<user>.+?) sees following privileges'
               r' of "(?P<member_name>.*)" (?P<member_type>user|group) in space'
               r' "(?P<space_name>.*)" in "(?P<host>.+?)" Onezone service:'
               r'\n(?P<config>(.|\s)*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_privileges_in_space_in_oz(client, selenium, user, space_name, hosts,
                                     oz_page, member_name, onepanel, users,
                                     member_type, config, spaces, host):
    client_lower = client.lower()
    if client_lower == 'web gui':
        option = 'Members'
        list_type = 'users'
        where = 'space'
        click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                      space_name, option,
                                                      oz_page)
        click_element_in_members_list(selenium, user, member_name,
                                      oz_page, where, list_type, onepanel)
        assert_privileges_in_members_subpage(selenium, user, member_name,
                                             member_type, where, config,
                                             onepanel, oz_page)
    elif client_lower == 'rest':
        user_client_oz = login_to_oz(user, users[user].password,
                                     hosts[host]['hostname'])
        space_api = SpaceApi(user_client_oz)

        user_privileges = (space_api
                           .list_user_space_privileges(spaces[space_name],
                                                       users[member_name].id)
                           .to_dict()['privileges'])
        grant = []
        revoke = []
        translate_privileges(config, grant, revoke)
        grant.sort()
        user_privileges.sort()
        assert user_privileges == grant, (f'users privileges {user_privileges}'
                                          f' does not match expected '
                                          f'privileges: {grant}')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) fails to invite '
               '"(?P<member_name>.*)" to "(?P<space_name>.*)" space members'
               ' page in "(?P<host>.+?)" Onezone service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_create_invitation_in_space_in_oz(client, selenium, user, space_name,
                                             oz_page, onepanel, popups, modals,
                                             users, hosts, member_name, spaces,
                                             host):
    client_lower = client.lower()
    if client_lower == 'web gui':
        option = 'Members'
        button = 'Invite user using token'
        where = 'space'
        member = 'users'
        modal = 'Invite using token'
        text = 'This resource could not be loaded'
        click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                      space_name, option,
                                                      oz_page)
        click_on_option_in_members_list_menu(selenium, user, button,
                                             where, member, oz_page, onepanel,
                                             popups)
        assert_alert_text_in_modal(selenium, user, modals, modal, text)

    if client_lower == 'rest':
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


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) does not see '
               '"(?P<member_name>.*)" on "(?P<space_name>.*)" space members '
               'page in "(?P<host>.+?)" Onezone service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_user_in_space_in_oz(client, selenium, user, member_name,
                                   space_name, oz_page, onepanel, users, hosts,
                                   host, spaces):
    client_lower = client.lower()
    if client_lower == 'web gui':
        option = 'does not see'
        member_type = 'user'
        parent_type = 'space'
        assert_member_is_in_parent_members_list(selenium, user, option,
                                                member_name, member_type,
                                                space_name, parent_type,
                                                oz_page, onepanel)

    elif client_lower == 'rest':
        user_client_oz = login_to_oz(user, users[user].password,
                                     hosts[host]['hostname'])
        space_api = SpaceApi(user_client_oz)
        users_id_list = (space_api.list_space_users(spaces[space_name])
                         .to_dict()['users'])
        assert users[member_name].id not in users_id_list, (
            f'user {member_name} is in space {space_name}')


