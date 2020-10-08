"""This module contains meta steps for operations on tokens.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.gui.meta_steps.onezone.tokens import (
    create_token_with_config, click_copy_button_in_token_view,
    revoke_token_in_oz_gui, assert_token_configuration,
    assert_token_configuration_gui)
from tests.mixed.steps.rest.onezone.tokens import (
    create_token_with_config_rest, revoke_token_rest,
    assert_token_with_config_rest)
from tests.mixed.utils.common import NoSuchClientException
from tests.utils.bdd_utils import wt, parsers


@wt(parsers.parse('using {client}, {user} creates token with '
                  'following configuration:\n{config}'))
def create_token(client, user, config, selenium, oz_page, popups, users,
                 groups, hosts, tmp_memory, tokens, spaces):
    client_lower = client.lower()
    if client_lower == 'web gui':
        create_token_with_config(selenium, user, config, oz_page, popups,
                                 users, groups, hosts, tmp_memory)
    elif client_lower == 'rest':
        create_token_with_config_rest(user, config, users, tokens, hosts,
                                      tmp_memory, groups, spaces)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.parse('using {client}, {user} sees that created token '
                  'configuration is as following:\n{config}'))
def assert_token(client, user, config, selenium, oz_page, users,
                 groups, hosts, tmp_memory, tokens, spaces):
    client_lower = client.lower()
    if client_lower == 'web gui':
        assert_token_configuration_gui(selenium, user, config, oz_page, users,
                                       groups, hosts, tmp_memory)
    elif client_lower == 'rest':
        assert_token_with_config_rest(user, config, users, hosts,
                                      tmp_memory, groups, spaces)
    else:
        raise NoSuchClientException('Client: {} not found'.format(client))


@wt(parsers.parse('if {client} is web gui, {user} copies created token'))
def copy_token_if_gui(selenium, oz_page, client, user, displays, clipboard,
                      tmp_memory):
    if client == 'web gui':
        click_copy_button_in_token_view(selenium, user, oz_page)
        tmp_memory[user]['token'] = clipboard.paste(display=displays[user])


@wt(parsers.parse('if {client} is web gui, {user} copies created token '
                  'named "{token_name}"'))
def copy_named_token_if_gui(selenium, oz_page, client, user, displays,
                            clipboard, tmp_memory, tokens, token_name):
    if client == 'web gui':
        click_copy_button_in_token_view(selenium, user, oz_page), token_name
        token = clipboard.paste(display=displays[user])
        tmp_memory[user]['token'] = token
        tokens[token_name] = {'token': token}


@wt(parsers.parse('using web gui, {user} copies created token'))
def copy_token_gui(selenium, oz_page, user, displays, clipboard, tmp_memory):
    click_copy_button_in_token_view(selenium, user, oz_page)
    tmp_memory[user]['token'] = clipboard.paste(display=displays[user])


@wt(parsers.parse('using {client}, {user} revokes token named "{token_name}"'))
def revoke_token_in_oz(client, user, token_name, users, hosts, tokens,
                       selenium, oz_page, popups):
    if client == 'rest':
        zone_name = 'onezone'
        revoke_token_rest(user, users, hosts, zone_name, tokens, token_name)
    elif client == 'web gui':
        revoke_token_in_oz_gui(selenium, user, token_name, oz_page, popups)
    else:
        raise NoSuchClientException(f'Client: {client} not found')

