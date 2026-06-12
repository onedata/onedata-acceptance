"""Module implements pytest-bdd steps for authorization and mounting oneclient."""

__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"
# pylint: disable=cell-var-from-loop, deprecated-method

from collections.abc import Mapping
from typing import cast

from tests.conftest import EnvDesc, Hosts, Users
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, parsers, then
from tests.utils.utils import assert_


@given(
    parsers.re(
        "oneclients (?P<client_ids>.*)\n"
        "mounted on client_hosts (?P<client_hosts>.*) respectively,\n"
        "using (?P<tokens>.*) by (?P<user_names>.*)"
    )
)
def multi_mount(
    user_names: str,
    client_ids: str,
    client_hosts: str,
    tokens: str,
    hosts: Hosts,
    users: Users,
    env_desc: EnvDesc,
) -> None:
    params = zip(
        list_parser(user_names),
        list_parser(client_ids),
        list_parser(client_hosts),
        list_parser(tokens),
    )

    for username, client_id, client_host, token in params:
        user = users[username]
        user.mount_client(
            client_host,
            client_id,
            cast(Mapping[str, Mapping[str, str]], hosts),
            env_desc,
            token,
        )


@then(
    parsers.re(
        r"(?P<spaces>.*) are mounted for (?P<user_name>\w+) on (?P<client_nodes>.*)"
    )
)
def check_spaces(spaces: str, user_name: str, client_nodes: str, users: Users) -> None:
    expected_spaces = list_parser(spaces)
    client_node_names = list_parser(client_nodes)

    for client_node in client_node_names:
        user = users[user_name]
        client = user.clients[client_node]
        spaces_in_client = client.list_spaces()

        def condition() -> None:
            for space in expected_spaces:
                assert space in spaces_in_client, (
                    f"Space {expected_spaces} not found in spaces list"
                    f" {spaces_in_client} on client {client_node}"
                )

        assert_(client.perform, condition)
