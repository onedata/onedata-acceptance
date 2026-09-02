"""Steps for inventories creation using REST API."""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from collections.abc import Mapping, MutableMapping
from typing import NotRequired, Optional, Protocol, TypedDict, cast

import yaml

from tests import OZ_REST_PORT
from tests.utils.bdd_utils import given, parsers
from tests.utils.rest_utils import get_zone_rest_path, http_post, http_put
from tests.utils.user_utils import Users

HostsConfig = Mapping[str, Mapping[str, str]]


class MemberOptions(TypedDict):
    privileges: list[str]


MemberEntry = str | dict[str, MemberOptions]


class InventoryDescription(TypedDict):
    owner: str
    users: NotRequired[list[MemberEntry]]
    groups: NotRequired[list[MemberEntry]]


InventoriesConfig = Mapping[str, InventoryDescription]


class CredentialsLike(Protocol):
    username: str
    password: str


@given(
    parsers.parse(
        'initial inventories configuration in "{zone_name}" Onezone service:\n{config}'
    )
)
def inventories_creation(
    config: str,
    admin_credentials: CredentialsLike,
    hosts: HostsConfig,
    users: Users,
    groups: Mapping[str, str],
    zone_name: str,
    inventories: MutableMapping[str, str],
) -> None:
    """Create and configure inventories according to given config.

    Config format given in yaml is as follows:

        inventory_name_1:
            owner: user_name

            [users]:                        ---> optional
                - user_name_2
                - user_name_3:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
            [groups]:                       ---> optional
                - group_name_1:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
                - group_name_2
        inventory_name_2:
            ...

    Example configuration:

        inventory1:
            owner: user1
            users:
                - user2
                - user3
            groups:
                - group1
        inventory2:
            owner: user2
    """
    _inventories_creation(
        config, hosts, users, zone_name, admin_credentials, groups, inventories
    )


def _inventories_creation(
    config: str,
    hosts: HostsConfig,
    users: Users,
    zone_name: str,
    admin_credentials: CredentialsLike,
    groups: Mapping[str, str],
    inventories: MutableMapping[str, str],
) -> None:
    zone_hostname = hosts[zone_name]["hostname"]
    inventories_config = cast(InventoriesConfig, yaml.load(config, yaml.Loader))

    for inventory_name, description in inventories_config.items():
        owner = users[description["owner"]]

        inventory_id = _create_inventory(zone_hostname, owner, inventory_name)
        inventories[inventory_name] = inventory_id
        for user_entry in description.get("users", []):
            user, privileges = _unpack_member_entry(user_entry)

            _add_user_to_inventory(
                zone_hostname,
                admin_credentials,
                inventory_id,
                users[user].user_id,
                privileges,
            )

        for group_entry in description.get("groups", []):
            group, privileges = _unpack_member_entry(group_entry)

            group_id = groups[group]

            _add_group_to_inventory(
                zone_hostname, admin_credentials, inventory_id, group_id, privileges
            )


def _unpack_member_entry(entry: MemberEntry) -> tuple[str, Optional[list[str]]]:
    if isinstance(entry, str):
        return entry, None
    [(name, options)] = entry.items()
    return name, options["privileges"]


def _create_inventory(
    zone_hostname: str, owner: CredentialsLike, inventory_name: str
) -> str:
    inventory_properties = json.dumps({"name": inventory_name})

    response = http_post(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "atm_inventories"),
        auth=(owner.username, owner.password),
        data=inventory_properties,
    )

    return response.headers["location"].split("/")[-1]


def _add_user_to_inventory(
    zone_hostname: str,
    admin_credentials: CredentialsLike,
    inventory_id: str,
    user_id: str,
    privileges: Optional[list[str]],
) -> None:
    if privileges:
        data = json.dumps({"privileges": privileges})
    else:
        data = None

    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("atm_inventories", inventory_id, "users", user_id),
        auth=(
            admin_credentials.username,
            admin_credentials.password,
        ),
        data=data,
    )


def _add_group_to_inventory(
    zone_hostname: str,
    admin_credentials: CredentialsLike,
    inventory_id: str,
    group_id: str,
    privileges: Optional[list[str]],
) -> None:
    if privileges:
        data = json.dumps({"privileges": privileges})
    else:
        data = None

    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("atm_inventories", inventory_id, "groups", group_id),
        auth=(
            admin_credentials.username,
            admin_credentials.password,
        ),
        data=data,
    )
