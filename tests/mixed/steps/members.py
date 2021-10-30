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
from tests.mixed.utils.common import NoSuchClientException
from tests.gui.meta_steps.onezone.members import *
from tests.mixed.steps.rest.onezone.members import *
from tests.gui.meta_steps.onezone.spaces import add_group_to_space_or_group


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
        fail_to_set_privileges_using_op_gui(user, space_name, member_name,
                                            member_type, config, selenium,
                                            onepanel, oz_page)

    elif client_lower == 'rest':
        fail_to_set_privileges_using_rest(user, users, hosts, host, spaces,
                                          space_name, member_name, config)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


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
        assert_privileges_in_space_using_op_gui(user, space_name, member_name,
                                                member_type, config, selenium,
                                                onepanel, oz_page)
    elif client_lower == 'rest':
        assert_privileges_in_space_using_rest(user, users, hosts, host, spaces,
                                              space_name, member_name, config)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


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
        fail_to_create_invitation_in_space_using_op_gui(user, space_name,
                                                        popups, modals,
                                                        selenium, onepanel,
                                                        oz_page)
    elif client_lower == 'rest':
        fail_to_create_invitation_in_space_using_rest(user, users, hosts, host,
                                                      spaces, space_name,
                                                      member_name)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) does not see '
               '"(?P<member_name>.*)" user on "(?P<space_name>.*)" space '
               'members page in "(?P<host>.+?)" Onezone service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_user_in_space_in_oz(client, selenium, user, member_name,
                                   space_name, oz_page, onepanel, users, hosts,
                                   host, spaces):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_not_user_in_space_using_op_gui(user, space_name, member_name,
                                              selenium, onepanel, oz_page)

    elif client_lower == 'rest':
        assert_not_user_in_space_using_rest(user, users, hosts, host, spaces,
                                            space_name, member_name)

    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) adds "(?P<group_name>.*)" '
               'to space named "(?P<space_name>.*)" in "(?P<host>.+?)" '
               'Onezone service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_group_to_space_in_oz(client, selenium, user, space_name, oz_page,
                             group_name, onepanel, popups, modals, users,
                             hosts, host, spaces):
    client_lower = client.lower()
    if client_lower == 'web gui':
        where = 'space'
        add_group_to_space_or_group(user, group_name, space_name, selenium,
                                    oz_page, onepanel, popups, where, modals)
    elif client_lower == 'rest':
        add_group_to_space_using_rest(user, users, hosts, host, group_name,
                                      spaces, space_name)

    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re('using (?P<client>.*), (?P<user>.+?) sees "(?P<group_name>.*)" '
               'group on "(?P<space_name>.*)" space members page in '
               '"(?P<host>.+?)" Onezone service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_in_space_in_oz(client, user, group_name, space_name, host,
                                selenium, oz_page, onepanel, users, hosts,
                                spaces):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_group_in_space_using_op_gui(selenium, user, space_name, oz_page,
                                           group_name, onepanel)
    elif client_lower == 'rest':
        assert_group_in_space_using_rest(user, users, hosts, host, group_name,
                                         spaces, space_name)

    else:
        raise NoSuchClientException(f'Client: {client} not found')



