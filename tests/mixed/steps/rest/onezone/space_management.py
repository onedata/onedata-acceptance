"""Utils and fixtures to facilitate operations on spaces in Onezone using
REST API.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Mapping, MutableMapping
from typing import Protocol, cast

from onezone_client import ProviderApi, SpaceApi, SpaceInviteToken, UserApi

from tests.conftest import Hosts
from tests.gui.utils.generic import parse_seq
from tests.mixed.steps.rest.onezone.common import (
    get_provider_with_name,
    get_space_with_name,
    get_user_space_with_name,
)
from tests.mixed.utils.common import login_to_oz
from tests.utils.entities_setup.spaces import _create_space

SpaceMap = MutableMapping[str, str]
Mailbox = MutableMapping[str, str]
TmpMemoryEntry = MutableMapping[str, Mailbox | str]
TmpMemory = MutableMapping[str, TmpMemoryEntry]


class UserLike(Protocol):
    password: str


class CredentialsLike(Protocol):
    username: str
    password: str


def create_spaces_in_oz_using_rest(
    user: str,
    users: Mapping[str, UserLike],
    hosts: Hosts,
    zone_name: str,
    space_list: list[str],
    spaces: SpaceMap,
) -> None:
    for space_name in space_list:
        space_id = _create_space(
            hosts[zone_name]["hostname"], user, users[user].password, space_name
        )
        spaces[space_name] = space_id


def leave_spaces_in_oz_using_rest(
    user: str,
    users: Mapping[str, UserLike],
    zone_name: str,
    hosts: Hosts,
    space_list: str,
    spaces: SpaceMap,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])
    user_api = UserApi(user_client)

    for space_name in parse_seq(space_list):
        user_api.leave_space(spaces[space_name])


def rename_spaces_in_oz_using_rest(
    user: str,
    users: Mapping[str, UserLike],
    zone_name: str,
    hosts: Hosts,
    space_list: str,
    new_names_list: str,
    spaces: SpaceMap,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])

    user_api = UserApi(user_client)
    space_api = SpaceApi(user_client)

    for space_name, new_space_name in zip(
        parse_seq(space_list), parse_seq(new_names_list)
    ):
        if space_name in spaces:
            space = user_api.get_user_space(spaces[space_name])
        else:
            space = get_user_space_with_name(user_client, space_name)
        space.name = new_space_name
        space_api.modify_space(space.space_id, space)


def remove_spaces_in_oz_using_rest(
    user: str,
    users: Mapping[str, UserLike],
    zone_name: str,
    hosts: Hosts,
    space_list: str,
    spaces: SpaceMap,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])
    space_api = SpaceApi(user_client)

    for space_name in parse_seq(space_list):
        if space_name in spaces:
            space_api.remove_space(spaces[space_name])
        else:
            space = get_user_space_with_name(user_client, space_name)
            space_api.remove_space(space.space_id)


def remove_provider_support_for_space_in_oz_using_rest(
    user: str,
    users: Mapping[str, UserLike],
    zone_name: str,
    hosts: Hosts,
    provider_alias: str,
    space_name: str,
    spaces: SpaceMap,
    admin_credentials: CredentialsLike,
) -> None:
    admin_client = login_to_oz(
        admin_credentials.username,
        admin_credentials.password,
        hosts[zone_name]["hostname"],
    )
    provider_name = hosts[provider_alias]["name"]
    provider = get_provider_with_name(admin_client, provider_name)
    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])
    space_api = SpaceApi(user_client)
    space_api.cease_support_by_provider(spaces[space_name], provider.provider_id)


def request_space_support_using_rest(
    user: str,
    users: Mapping[str, UserLike],
    space_name: str,
    zone_alias: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    receiver: str,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_alias]["hostname"])

    space_api = SpaceApi(user_client)
    space = get_user_space_with_name(user_client, space_name)
    token = space_api.create_space_support_token(space.space_id).token
    if "mailbox" in tmp_memory[receiver]:
        cast(Mailbox, tmp_memory[receiver]["mailbox"])["token"] = token
    else:
        tmp_memory[receiver]["mailbox"] = {"token": token}


def join_space_in_oz_using_rest(
    user_list: str,
    users: Mapping[str, UserLike],
    zone_name: str,
    hosts: Hosts,
    _space_name: str,
    tmp_memory: TmpMemory,
) -> None:
    for user in parse_seq(user_list):
        user_client = login_to_oz(
            user, users[user].password, hosts[zone_name]["hostname"]
        )
        user_api = UserApi(user_client)
        mailbox = cast(Mailbox, tmp_memory[user]["mailbox"])
        token = SpaceInviteToken(mailbox["token"])
        user_api.join_space(token)


def assert_spaces_have_appeared_in_oz_rest(
    user: str,
    users: Mapping[str, UserLike],
    hosts: Hosts,
    zone_name: str,
    space_list: str,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])

    for space_name in parse_seq(space_list):
        assert get_user_space_with_name(
            user_client, space_name
        ), f"There is no space named {space_name}"


def assert_there_are_no_spaces_in_oz_rest(
    user: str,
    users: Mapping[str, UserLike],
    zone_name: str,
    hosts: Hosts,
    space_list: str,
    spaces: SpaceMap,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])
    user_api = UserApi(user_client)
    user_spaces = user_api.list_user_spaces()

    for space_name in parse_seq(space_list):
        assert (
            spaces[space_name] not in user_spaces.spaces
        ), f"There is space named {space_name}"


def assert_spaces_have_been_renamed_in_oz_rest(
    user: str,
    users: Mapping[str, UserLike],
    zone_name: str,
    hosts: Hosts,
    space_list: str,
    new_names_list: str,
    spaces: SpaceMap,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])
    user_api = UserApi(user_client)

    for space_name, new_space_name in zip(
        parse_seq(space_list), parse_seq(new_names_list)
    ):
        space_name = user_api.get_user_space(spaces[space_name]).name
        assert (
            space_name == new_space_name
        ), f"Space should has name {new_space_name} but it has name {space_name}"


def assert_there_is_no_provider_for_space_in_oz_rest(
    user: str,
    users: Mapping[str, UserLike],
    zone_name: str,
    hosts: Hosts,
    space_name: str,
    spaces: SpaceMap,
    providers_alias_list: str,
    admin_credentials: CredentialsLike,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])
    space_api = SpaceApi(user_client)
    space_providers = space_api.list_space_providers(spaces[space_name])
    admin_client = login_to_oz(
        admin_credentials.username,
        admin_credentials.password,
        hosts[zone_name]["hostname"],
    )

    for provider_alias in parse_seq(providers_alias_list):
        provider_name = hosts[provider_alias]["name"]
        assert_msg = (
            f"Space {space_name} is supported by provider {provider_name} while"
            " it should not be"
        )
        assert (
            get_provider_with_name(admin_client, provider_name)
            not in space_providers.providers
        ), assert_msg


def assert_space_is_supported_by_provider_in_oz_rest(
    user: str,
    users: Mapping[str, UserLike],
    zone_host: str,
    hosts: Hosts,
    space_name: str,
    provider_alias: str,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_host]["hostname"])
    provider_name = hosts[provider_alias]["name"]

    provider_api = ProviderApi(user_client)
    space = get_user_space_with_name(user_client, space_name)

    providers = [provider_api.get_provider_details(pid).name for pid in space.providers]
    assert (
        provider_name in providers
    ), f"Provider {provider_name} does not support space {space_name}"


def assert_provider_does_not_support_space_in_oz_rest(
    user: str,
    users: Mapping[str, UserLike],
    zone_host: str,
    hosts: Hosts,
    space_name: str,
    provider_alias: str,
) -> None:
    user_client_oz = login_to_oz(
        user, users[user].password, hosts[zone_host]["hostname"]
    )

    space = get_user_space_with_name(user_client_oz, space_name)
    provider_name = hosts[provider_alias]["name"]
    assert (
        provider_name not in space.providers
    ), f"Provider {provider_name} supports space {space_name}"


def copy_id_of_space_rest(
    user: str,
    users: Mapping[str, UserLike],
    hosts: Hosts,
    space_name: str,
    tmp_memory: TmpMemory,
    onepanel_credentials: CredentialsLike,
    admin_credentials: CredentialsLike,
) -> None:
    if user == onepanel_credentials.username:
        user = admin_credentials.username
    user_client = login_to_oz(user, users[user].password, hosts["onezone"]["hostname"])
    space = get_space_with_name(user_client, space_name)
    tmp_memory["spaces"][space_name] = space.space_id
