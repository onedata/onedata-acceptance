"""Module implements pytest-bdd steps for authorization and mounting oneclient."""

__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"
# pylint: disable=cell-var-from-loop, deprecated-method

from collections.abc import Mapping
from typing import cast

from tests.gui.utils.generic import ELEMENTS_SEQUENCE_PATTERN, parse_elements_sequence
from tests.type_definitions import EnvDesc, Hosts
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, parsers, then
from tests.utils.user_utils import Users
from tests.utils.utils import assert_


@given(
    parsers.re(
        rf"oneclients (?P<client_ids>{ELEMENTS_SEQUENCE_PATTERN})\n"
        rf"mounted on client_hosts (?P<client_hosts>{ELEMENTS_SEQUENCE_PATTERN}) "
        rf"respectively,\nusing (?P<tokens>.*) by "
        rf"(?P<user_names>{ELEMENTS_SEQUENCE_PATTERN})"
    ),
    converters={
        "client_hosts": parse_elements_sequence,
        "client_ids": parse_elements_sequence,
        "user_names": parse_elements_sequence,
    },
)
def multi_mount(
    user_names: list[str],
    client_ids: list[str],
    client_hosts: list[str],
    tokens: str,
    hosts: Hosts,
    users: Users,
    env_desc: EnvDesc,
) -> None:
    params = zip(
        user_names,
        client_ids,
        client_hosts,
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
