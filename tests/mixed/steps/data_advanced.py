"""This module contains gherkin steps to run mixed acceptance tests featuring
advanced operations on data using web GUI, REST and oneclient.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import cast

import pytest
from onezone_client import SpaceApi, UserApi

from tests.mixed.steps.oneclient.data_basic import (
    change_client_name_to_hostname,
    create_file_in_op_oneclient,
)
from tests.mixed.steps.rest.onezone.space_management import (
    create_spaces_in_oz_using_rest,
)
from tests.mixed.type_definitions import DataAdvancedTmpMemory as TmpMemory
from tests.mixed.type_definitions import MutableSpaces as Spaces
from tests.mixed.type_definitions import (
    SpaceAliases,
)
from tests.mixed.utils.common import NoSuchClientException, login_to_oz
from tests.oneclient.steps import multi_reg_file_steps
from tests.type_definitions import Hosts
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import Users


@wt(
    parsers.parse(
        'using {client}, {user} creates space named "{space_name}" with test alias'
        ' "{alias}" in "{host}" Onezone service'
    )
)
def create_space_with_alias_in_oz(
    client: str,
    user: str,
    space_name: str,
    alias: str,
    host: str,
    hosts: Hosts,
    users: Users,
    spaces: Spaces,
    space_aliases: SpaceAliases,
) -> None:
    if client.lower() == "rest":
        create_spaces_in_oz_using_rest(
            user,
            users,
            hosts,
            host,
            [space_name],
            spaces,
        )
        space_aliases[alias] = {"name": space_name, "sid": spaces[space_name]}
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.parse(
        "using {client}, {user} generates space support "
        'token for space with test alias "{alias}" in '
        '"{host}" Onezone service and sends it to '
        "{supporting_user}"
    )
)
def request_space_support_using_rest_for_space_with_alias(
    client: str,
    user: str,
    users: Users,
    alias: str,
    host: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    supporting_user: str,
    space_aliases: SpaceAliases,
) -> None:
    if client.lower() == "rest":
        user_client = login_to_oz(
            user, cast(str, users[user].password), hosts[host]["hostname"]
        )
        space_api = SpaceApi(user_client)
        token = space_api.create_space_support_token(space_aliases[alias]["sid"]).token
        tmp_memory[supporting_user]["mailbox"]["token"] = token
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r"using (?P<client>.*), (?P<user>\w+) creates "
        'file named "(?P<file_name>.*)" in space with test alias "(?P<alias>.*)" in'
        " (?P<host>.*)"
    )
)
def create_file_in_op_in_space_with_alias(
    client: str,
    user: str,
    users: Users,
    file_name: str,
    alias: str,
    request: pytest.FixtureRequest,
    space_aliases: SpaceAliases,
) -> None:
    client_lower = client.lower()
    if "oneclient" in client_lower:
        result = "succeds"
        oneclient_host = change_client_name_to_hostname(client_lower)
        full_path = create_path_for_item_in_space_with_alias(
            space_aliases, alias, file_name
        )
        create_file_in_op_oneclient(
            user, full_path, users, result, oneclient_host, request
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r'using (?P<client>.*), (?P<user>\w+) writes "(?P<content>.*)" to '
        'file named "(?P<file_name>.*)" in space with test alias "(?P<alias>.*)" in'
        " (?P<host>.*)"
    )
)
def write_to_file_in_op_in_space_with_alias(
    client: str,
    user: str,
    users: Users,
    file_name: str,
    alias: str,
    content: str,
    space_aliases: SpaceAliases,
) -> None:
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        full_path = create_path_for_item_in_space_with_alias(
            space_aliases, alias, file_name
        )
        multi_reg_file_steps.write_text(
            user, str(content), full_path, oneclient_host, users
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        r'using (?P<client>.*), (?P<user>\w+) reads "(?P<content>.*)" from '
        'file named "(?P<file_name>.*)" in space with test alias "(?P<alias>.*)" in'
        " (?P<host>.*)"
    )
)
def read_from_file_in_op_in_space_with_alias(
    client: str,
    user: str,
    users: Users,
    file_name: str,
    alias: str,
    content: str,
    space_aliases: SpaceAliases,
) -> None:
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        full_path = create_path_for_item_in_space_with_alias(
            space_aliases, alias, file_name
        )
        multi_reg_file_steps.read_text(
            user, str(content), full_path, oneclient_host, users
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) removes space with test alias "
        '"(?P<alias>.*)" in "(?P<host>.+?)" Onezone service'
    )
)
def remove_space_with_alias_in_oz(
    client: str,
    user: str,
    users: Users,
    host: str,
    hosts: Hosts,
    alias: str,
    space_aliases: SpaceAliases,
) -> None:
    client_lower = client.lower()
    if client_lower == "rest":
        user_client = login_to_oz(
            user, cast(str, users[user].password), hosts[host]["hostname"]
        )
        space_api = SpaceApi(user_client)
        space_api.remove_space(space_aliases[alias]["sid"])
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) renames space with test alias "
        '"(?P<alias>.*)" to "(?P<new_space_name>.*)" in "(?P<host>.+?)" Onezone service'
    )
)
def rename_space_with_alias_in_oz(
    client: str,
    user: str,
    users: Users,
    host: str,
    hosts: Hosts,
    alias: str,
    new_space_name: str,
    space_aliases: SpaceAliases,
) -> None:
    client_lower = client.lower()
    if client_lower == "rest":
        user_client = login_to_oz(
            user, cast(str, users[user].password), hosts[host]["hostname"]
        )
        user_api = UserApi(user_client)
        space_api = SpaceApi(user_client)
        space = user_api.get_user_space(space_aliases[alias]["sid"])
        space.name = new_space_name
        space_api.modify_space(space.space_id, space)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


def create_path_for_item_in_space_with_alias(
    space_aliases: SpaceAliases, alias: str, file_name: str
) -> str:
    if check_whether_space_names_repeats_for_alias(alias, space_aliases):
        return (
            f"{space_aliases[alias]["name"]}@{space_aliases[alias]["sid"]}/{file_name}"
        )
    return f"{space_aliases[alias]["name"]}/{file_name}"


def check_whether_space_names_repeats_for_alias(
    alias: str, space_aliases: SpaceAliases
) -> bool:
    space_name = space_aliases[alias]["name"]
    for k, v in space_aliases.items():
        if k != alias and v["name"] == space_name:
            return True
    return False
