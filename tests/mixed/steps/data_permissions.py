"""This module contains gherkin steps to run mixed acceptance tests featuring
basic operations on permissions on data using web GUI and REST.
"""

__author__ = "Michal Stanisz, Michal Cwiertnia, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import re

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.meta_steps.oneprovider.permissions import (
    grant_acl_privileges_in_op_gui, assert_ace_in_op_gui,
    assert_posix_permissions_in_op_gui, set_posix_permissions_in_op_gui)
from tests.mixed.steps.data_basic import change_client_name_to_hostname
from tests.mixed.steps.oneclient.data_basic import (
    grant_acl_privileges_in_op_oneclient, assert_ace_in_op_oneclient,
    assert_posix_permissions_in_op_oneclient,
    set_posix_permissions_in_op_oneclient)
from tests.mixed.steps.rest.oneprovider.data import (
    grant_acl_privileges_in_op_rest, assert_ace_in_op_rest,
    assert_posix_permissions_in_op_rest, set_posix_permissions_in_op_rest)
from tests.mixed.utils.common import NoSuchClientException
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


def _remove_parent_acl_from_string(priv):
    return re.sub('[a-zA-Z]+:', '', priv)


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sets new ACE for '
               '(?P<path>.*?) in space "(?P<space>.*)" with (?P<priv>.*) '
               'privileges? set for (?P<type>.*?) (?P<name>.*) '
               'in (?P<host>.*)'))
def grant_acl_privileges_in_op(client, selenium, user, cdmi, op_container, space,
                               path, host, hosts, users, priv, type, name,
                               groups, tmp_memory, popups, modals,
                               oz_page):
    full_path = f'{space}/{path}'
    client_lower = client.lower()

    if client_lower == 'web gui':
        grant_acl_privileges_in_op_gui(selenium, user, path, priv, name,
                                       op_container, tmp_memory, popups, space,
                                       oz_page, modals)
    elif client_lower == 'rest':
        priv = _remove_parent_acl_from_string(priv)
        grant_acl_privileges_in_op_rest(user, users, host, hosts, cdmi,
                                        full_path, priv,
                                        type, name, groups)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        priv = _remove_parent_acl_from_string(priv)
        grant_acl_privileges_in_op_oneclient(user, users, oneclient_host,
                                             full_path, priv, type, groups,
                                             name)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees that (?P<path>.*?)'
               ' in space "(?P<space>.*)" (has|have) (?P<priv>.*) '
               'privileges? set for (?P<type>.*?) (?P<name>.*) in '
               '(?P<num>.*) ACL record in (?P<host>.*)'))
def assert_ace_in_op(client, selenium, user, cdmi, op_container, space, path, host,
                     hosts, users, num, priv, type, name, numerals, tmp_memory,
                     modals, oz_page, popups):
    full_path = f'{space}/{path}'
    client_lower = client.lower()

    if client_lower == 'web gui':
        assert_ace_in_op_gui(selenium, user, priv, type, name, num, space,
                             path, tmp_memory, modals, numerals, oz_page,
                             op_container, popups)
    elif client_lower == 'rest':
        priv = _remove_parent_acl_from_string(priv)
        assert_ace_in_op_rest(user, users, host, hosts, cdmi, numerals,
                              full_path, num, priv, type,
                              name)
    elif 'oneclient' in client_lower:
        priv = _remove_parent_acl_from_string(priv)
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_ace_in_op_oneclient(user, users, oneclient_host, full_path, num,
                                   priv, type, name, numerals)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) sees '
               'that POSIX permission for item named "(?P<item_path>.*)" in '
               '"(?P<space>.*)" is "(?P<mode>.*)" in (?P<host>.*)'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_posix_permissions_in_op(client, user, item_path, space, mode,
                                   host, selenium, op_container, tmp_memory,
                                   modals, users, hosts, oz_page, popups):
    full_path = f'{space}/{item_path}'
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_posix_permissions_in_op_gui(selenium, user, space, item_path,
                                           mode, oz_page, op_container,
                                           tmp_memory, modals, popups)
    elif client_lower == 'rest':
        assert_posix_permissions_in_op_rest(full_path, mode, user, users,
                                            host, hosts)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_posix_permissions_in_op_oneclient(user, full_path, mode,
                                                 oneclient_host, users)
    else:
        raise NoSuchClientException(f'Client: {client} not found')


@wt(parsers.re(r'using (?P<client>.*), (?P<user>\w+) (?P<result>\w+) to set '
               '"(?P<mode>.*)" POSIX permission for item named '
               '"(?P<item_path>.*)" in "(?P<space>.*)" in (?P<host>.*)'))
def set_posix_permissions_in_op(client, user, item_path, space, mode, result,
                                host, selenium, op_container, tmp_memory, modals,
                                users, hosts, oz_page, popups):
    full_path = f'{space}/{item_path}'
    client_lower = client.lower()
    if client_lower == 'web gui':
        set_posix_permissions_in_op_gui(selenium, user, space, item_path,
                                        mode, op_container, tmp_memory,
                                        modals, oz_page, popups)
    elif client_lower == 'rest':
        set_posix_permissions_in_op_rest(full_path, mode, user, users, host,
                                         hosts, result)
    elif 'oneclient' in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        set_posix_permissions_in_op_oneclient(user, full_path, mode,
                                              oneclient_host, users, result)
    else:
        raise NoSuchClientException(f'Client: {client} not found')

