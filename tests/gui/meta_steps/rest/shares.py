"""Meta steps for share management using REST API helpers."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import yaml

from tests.gui.steps.rest.shares import (
    add_user_to_handle_service_using_rest,
    create_share_for_file_using_rest,
    get_first_handle_service_id,
)
from tests.gui.utils.generic import transform
from tests.type_definitions import Hosts
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.entities_setup.spaces import create_empty_file, get_file_id_by_rest
from tests.utils.user_utils import Users


@given(
    parsers.parse(
        'using REST, user {user} creates "{share_name}" share of '
        '"{item_path}" supported by "{provider}" provider'
    )
)
@wt(
    parsers.parse(
        'using REST, user {user} creates "{share_name}" share of '
        '"{item_path}" supported by "{provider}" provider'
    )
)
def create_share_using_rest(
    item_path: str,
    provider: str,
    user: str,
    share_name: str,
    hosts: Hosts,
    users: Users,
    shares: dict[str, str],
) -> None:
    provider_hostname = hosts[provider]["hostname"]
    access_token = users[user].token
    file_id = get_file_id_by_rest(item_path, provider_hostname, access_token)
    shares[share_name] = create_share_for_file_using_rest(
        provider_hostname, access_token, file_id, share_name
    )


@given(parsers.parse("using REST, user {user} creates following shares:\n{config}"))
def create_many_shares_using_rest(
    user: str, config: str, hosts: Hosts, users: Users, shares: dict[str, str]
) -> None:
    """Create shares described by a YAML list."""
    _create_many_shares_using_rest(user, config, hosts, users, shares)


def _create_many_shares_using_rest(
    user: str, config: str, hosts: Hosts, users: Users, shares: dict[str, str]
) -> None:
    data = yaml.load(config, yaml.Loader)
    for share in data:
        create_share_using_rest(
            share["path"],
            share["provider"],
            user,
            share["name"],
            hosts,
            users,
            shares,
        )


@given(parsers.parse("user {user} is added to mock handle service in {host}"))
def add_user_to_handle_service(
    user: str, users: Users, host: str, hosts: Hosts
) -> None:
    zone_hostname = hosts[transform(host)]["hostname"]
    access_token = users["admin"].token
    handle_service_id = get_first_handle_service_id(zone_hostname, access_token)
    add_user_to_handle_service_using_rest(
        zone_hostname, access_token, handle_service_id, users[user].user_id
    )


@wt(
    parsers.parse(
        'using REST, {user} creates {number} shares in space "{space_name}" in {host}'
    )
)
def create_n_shares_in_space(
    users: Users,
    user: str,
    hosts: Hosts,
    host: str,
    number: str,
    space_name: str,
    shares: dict[str, str],
) -> None:
    for i in range(int(number)):
        item_path = f"{space_name}/file{i}"
        create_empty_file(item_path, users, user, host, hosts)
        create_share_using_rest(
            item_path, host, user, f"share{i}", hosts, users, shares
        )
