"""Module implements pytest-bdd steps for authorization and mounting oneclient."""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Mapping
from typing import cast

from tests.oneclient.steps.multi_auth_steps import assert_spaces_found_for_each_client
from tests.type_definitions import EnvDesc, Hosts
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.user_utils import Users


@given(parsers.re(r"oneclient mounted using (?P<token>(token|bad token)) by (?P<user>\w+)"))
def default_mount(user: str, token: str, hosts: Hosts, users: Users, env_desc: EnvDesc) -> None:
    users[user].mount_client(
        "oneclient-1",
        "client1",
        cast(Mapping[str, Mapping[str, str]], hosts),
        env_desc,
        token,
    )


@wt(
    parsers.re(r"(?P<spaces>.*) (is|are) mounted for (?P<user>\w+)"),
    converters={"spaces": list_parser},
)
def assert_spaces_mounted_for_user(spaces: list[str], user: str, users: Users) -> None:
    assert_spaces_found_for_each_client(spaces, user, ["client1"], users)
