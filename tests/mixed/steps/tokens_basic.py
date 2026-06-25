"""This module contains meta steps for operations on tokens."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Mapping
from typing import cast

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
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.mixed.steps.rest.onezone.space_management import join_space_in_oz_using_rest
from tests.mixed.steps.rest.onezone.tokens import (
    UserLike,
    assert_token_with_config_rest,
    create_token_with_config_rest,
    revoke_token_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.type_definitions import Hosts, SeleniumDrivers, Tokens, Users
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
    client: str,
    user: str,
    config: str,
    selenium: SeleniumDrivers,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    tokens: Tokens,
    spaces: dict[str, str],
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
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
            user,
            config,
            cast(Mapping[str, UserLike], users),
            tokens,
            hosts,
            tmp_memory,
            groups,
            spaces,
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
    client: str,
    user: str,
    config: str,
    selenium: SeleniumDrivers,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    spaces: dict[str, str],
) -> None:
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
            user,
            config,
            cast(Mapping[str, UserLike], users),
            hosts,
            tmp_memory,
            groups,
            spaces,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(parsers.parse("if {client} is web gui, {user} copies created token"))
def copy_token_if_gui(
    selenium: SeleniumDrivers,
    client: str,
    user: str,
    displays: dict[str, str],
    clipboard: Clipboard,
    tmp_memory: TmpMemory,
) -> None:
    if client.lower() == "web gui":
        copy_token_gui(selenium, user, displays, clipboard, tmp_memory)


@wt(parsers.parse('using {client}, {user} copies created token named "{token_name}"'))
@wt(
    parsers.parse(
        'if {client} is web gui, {user} copies created token named "{token_name}"'
    )
)
def copy_named_token_if_gui(
    selenium: SeleniumDrivers,
    client: str,
    user: str,
    displays: dict[str, str],
    clipboard: Clipboard,
    tmp_memory: TmpMemory,
    tokens: Tokens,
    token_name: str,
) -> None:
    if client == "web gui":
        click_copy_button_in_token_view(selenium, user)
        token = clipboard.paste(display=displays[user])
        tmp_memory[user]["token"] = token
        tokens[token_name] = {"token": token}


@wt(parsers.parse("using web gui, {user} copies created token"))
def copy_token_gui(
    selenium: SeleniumDrivers,
    user: str,
    displays: dict[str, str],
    clipboard: Clipboard,
    tmp_memory: TmpMemory,
) -> None:
    click_copy_button_in_token_view(selenium, user)
    tmp_memory[user]["token"] = clipboard.paste(display=displays[user])


@wt(parsers.parse('using {client}, {user} revokes token named "{token_name}"'))
@repeat_failed(timeout=WAIT_BACKEND)
def revoke_token_in_oz(
    client: str,
    user: str,
    token_name: str,
    users: Users,
    hosts: Hosts,
    tokens: Tokens,
    selenium: SeleniumDrivers,
) -> None:
    client_lower = client.lower()
    if client_lower == "rest":
        zone_name = "onezone"
        revoke_token_rest(
            user,
            cast(Mapping[str, UserLike], users),
            hosts,
            zone_name,
            tokens,
            token_name,
        )
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
    selenium: SeleniumDrivers,
    user: str,
    tmp_memory: TmpMemory,
    client: str,
    users: Users,
    hosts: Hosts,
    space_name: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        consume_received_token(selenium, user, tmp_memory)
        assert_new_created_space_has_appeared_on_spaces(selenium, user, space_name)
    elif client_lower == "rest":
        join_space_in_oz_using_rest(
            user,
            cast(Mapping[str, UserLike], users),
            "onezone",
            hosts,
            space_name,
            tmp_memory,
        )
        assert_new_created_space_has_appeared_on_spaces(selenium, user, space_name)
    else:
        raise NoSuchClientException(f"Client: {client} not found")
