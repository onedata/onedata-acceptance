"""This module contains gherkin steps to run mixed acceptance tests featuring
advanced operations on data using web GUI, REST and oneclient.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from onezone_client import SpaceApi, UserApi

from tests.mixed.steps.oneclient.data_basic import (
    change_client_name_to_hostname,
    create_file_in_op_oneclient,
)
from tests.mixed.steps.rest.onezone.space_management import (
    create_spaces_in_oz_using_rest,
)
from tests.mixed.utils.common import NoSuchClientException, login_to_oz
from tests.oneclient.steps import multi_reg_file_steps
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.parse(
        'using {client}, {user} creates space named "{space_name}" with test alias'
        ' "{alias}" in "{host}" Onezone service'
    )
)
def create_space_with_alias_in_oz(
    client, user, space_name, alias, host, hosts, users, spaces, space_aliases
):
    if client.lower() == "rest":
        create_spaces_in_oz_using_rest(user, users, hosts, host, [space_name], spaces)
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
    client, user, users, alias, host, hosts, tmp_memory, supporting_user, space_aliases
):
    if client.lower() == "rest":
        user_client = login_to_oz(user, users[user].password, hosts[host]["hostname"])
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
    client, user, users, file_name, alias, request, space_aliases
):
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
    client, user, users, file_name, alias, content, space_aliases
):
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
    client, user, users, file_name, alias, content, space_aliases
):
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
    client, user, users, host, hosts, alias, space_aliases
):
    client_lower = client.lower()
    if client_lower == "rest":
        user_client = login_to_oz(user, users[user].password, hosts[host]["hostname"])
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
    client, user, users, host, hosts, alias, new_space_name, space_aliases
):
    client_lower = client.lower()
    if client_lower == "rest":
        user_client = login_to_oz(user, users[user].password, hosts[host]["hostname"])
        user_api = UserApi(user_client)
        space_api = SpaceApi(user_client)
        space = user_api.get_user_space(space_aliases[alias]["sid"])
        space.name = new_space_name
        space_api.modify_space(space.space_id, space)
    else:
        raise NoSuchClientException(f"Client: {client} not found")


def create_path_for_item_in_space_with_alias(space_aliases, alias, file_name):
    if check_whether_space_names_repeats_for_alias(alias, space_aliases):
        return (
            f"{space_aliases[alias]["name"]}@{space_aliases[alias]["sid"]}/{file_name}"
        )
    return f"{space_aliases[alias]["name"]}/{file_name}"


def check_whether_space_names_repeats_for_alias(alias, space_aliases):
    space_name = space_aliases[alias]["name"]
    for k, v in space_aliases.items():
        if k != alias and v["name"] == space_name:
            return True
    return False
