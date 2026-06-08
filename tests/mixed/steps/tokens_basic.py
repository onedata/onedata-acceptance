"""This module contains meta steps for operations on tokens."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.meta_steps.onezone.tokens import (
    assert_token_configuration_gui,
    choose_and_revoke_token_in_oz_gui,
    click_copy_button_in_token_view,
    consume_received_token,
    create_token_with_config,
)
from tests.gui.steps.onezone.spaces import (
    assert_new_created_space_has_appeared_on_spaces,
)
from tests.mixed.steps.rest.onezone.space_management import join_space_in_oz_using_rest
from tests.mixed.steps.rest.onezone.tokens import (
    assert_token_with_config_rest,
    create_token_with_config_rest,
    revoke_token_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@given(
    parsers.parse(
        "using {client}, {user} creates token with following configuration:\n{config}"
    )
)
@wt(
    parsers.parse(
        "using {client}, {user} creates token with following configuration:\n{config}"
    )
)
def create_token(
    client: Any,
    user: Any,
    config: Any,
    selenium: Any,
    users: Any,
    groups: Any,
    hosts: Any,
    tmp_memory: Any,
    tokens: Any,
    spaces: Any,
    clipboard: Any,
    displays: Any,
) -> Any:
    client_lower = client.lower()
    if client_lower == "web gui":
        create_token_with_config(
            selenium,
            user,
            config,
            users,
            groups,
            hosts,
            tmp_memory,
        )
        click_copy_button_in_token_view(selenium, user)
        tmp_memory[user]["token"] = clipboard.paste(display=displays[user])
    elif client_lower == "rest":
        create_token_with_config_rest(
            user, config, users, tokens, hosts, tmp_memory, groups, spaces
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.parse(
        "using {client}, {user} sees that created token "
        "configuration is as following:\n{config}"
    )
)
def assert_token(
    client: Any,
    user: Any,
    config: Any,
    selenium: Any,
    users: Any,
    groups: Any,
    hosts: Any,
    tmp_memory: Any,
    spaces: Any,
) -> Any:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_token_configuration_gui(
            selenium,
            user,
            config,
            users,
            groups,
            hosts,
            tmp_memory,
            spaces,
        )
    elif client_lower == "rest":
        assert_token_with_config_rest(
            user, config, users, hosts, tmp_memory, groups, spaces
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(parsers.parse("if {client} is web gui, {user} copies created token"))
def copy_token_if_gui(
    selenium: Any,
    client: Any,
    user: Any,
    displays: Any,
    clipboard: Any,
    tmp_memory: Any,
) -> Any:
    if client.lower() == "web gui":
        copy_token_gui(selenium, user, displays, clipboard, tmp_memory)


@wt(parsers.parse('using {client}, {user} copies created token named "{token_name}"'))
@wt(
    parsers.parse(
        'if {client} is web gui, {user} copies created token named "{token_name}"'
    )
)
def copy_named_token_if_gui(
    selenium: Any,
    client: Any,
    user: Any,
    displays: Any,
    clipboard: Any,
    tmp_memory: Any,
    tokens: Any,
    token_name: Any,
) -> Any:
    if client == "web gui":
        click_copy_button_in_token_view(selenium, user)
        token = clipboard.paste(display=displays[user])
        tmp_memory[user]["token"] = token
        tokens[token_name] = {"token": token}


@wt(parsers.parse("using web gui, {user} copies created token"))
def copy_token_gui(
    selenium: Any, user: Any, displays: Any, clipboard: Any, tmp_memory: Any
) -> Any:
    click_copy_button_in_token_view(selenium, user)
    tmp_memory[user]["token"] = clipboard.paste(display=displays[user])


@wt(parsers.parse('using {client}, {user} revokes token named "{token_name}"'))
@repeat_failed(timeout=WAIT_BACKEND)
def revoke_token_in_oz(
    client: Any,
    user: Any,
    token_name: Any,
    users: Any,
    hosts: Any,
    tokens: Any,
    selenium: Any,
) -> Any:
    client_lower = client.lower()
    if client_lower == "rest":
        zone_name = "onezone"
        revoke_token_rest(user, users, hosts, zone_name, tokens, token_name)
    elif client_lower == "web gui":
        choose_and_revoke_token_in_oz_gui(selenium, user, token_name)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.parse(
        "using {client}, {user} successfully joins space {"
        "space_name} with received token"
    )
)
def join_space_with_token(
    selenium: Any,
    user: Any,
    tmp_memory: Any,
    client: Any,
    users: Any,
    hosts: Any,
    space_name: Any,
) -> Any:
    client_lower = client.lower()
    if client_lower == "web gui":
        consume_received_token(selenium, user, tmp_memory)
        assert_new_created_space_has_appeared_on_spaces(selenium, user, space_name)
    elif client_lower == "rest":
        join_space_in_oz_using_rest(
            user, users, "onezone", hosts, space_name, tmp_memory
        )
        assert_new_created_space_has_appeared_on_spaces(selenium, user, space_name)
    else:
        raise NoSuchClientException(f"Client: {client} not found")
