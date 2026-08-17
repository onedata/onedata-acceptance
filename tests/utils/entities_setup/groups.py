"""Steps for groups creation using REST API."""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from collections.abc import Mapping, MutableMapping
from typing import Callable, NotRequired, Protocol, TypedDict, cast

import pytest
import yaml

from tests import OZ_REST_PORT
from tests.gui.meta_steps.rest.groups import delete_group_if_present_using_rest
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.http_exceptions import HTTPForbidden
from tests.utils.rest_utils import (
    get_zone_rest_path,
    http_delete,
    http_get,
    http_post,
    http_put,
)
from tests.utils.user_utils import Users

HostsConfig = Mapping[str, Mapping[str, str]]


class CredentialsLike(Protocol):
    username: str
    password: str


class MemberOptions(TypedDict):
    privileges: list[str]


MemberEntry = str | dict[str, MemberOptions]


class GroupDescription(TypedDict):
    owner: str
    users: NotRequired[list[MemberEntry]]
    groups: NotRequired[list[MemberEntry]]


GroupsConfig = Mapping[str, GroupDescription]
GroupFinalizerRegistrar = Callable[[str], None]


def _register_group_finalizer(
    request: pytest.FixtureRequest,
    zone_hostname: str,
    admin_credentials: CredentialsLike,
    group_id: str,
) -> None:
    request.addfinalizer(
        lambda: delete_group_if_present_using_rest(
            zone_hostname,
            admin_credentials.username,
            admin_credentials.password,
            group_id,
        )
    )


@given(
    parsers.parse(
        'initial groups configuration in "{service}" Onezone service:\n{config}'
    )
)
def groups_creation_step(
    config: str,
    service: str,
    admin_credentials: CredentialsLike,
    users: Users,
    hosts: HostsConfig,
    groups: MutableMapping[str, str],
    request: pytest.FixtureRequest,
) -> None:
    groups_config = cast(GroupsConfig, yaml.load(config, yaml.Loader))
    zone_hostname = hosts[service]["hostname"]
    groups_creation(
        groups_config,
        service,
        admin_credentials,
        users,
        hosts,
        groups,
        lambda group_id: _register_group_finalizer(
            request, zone_hostname, admin_credentials, group_id
        ),
    )


def groups_creation(
    config: GroupsConfig,
    service: str,
    admin_credentials: CredentialsLike,
    users: Users,
    hosts: HostsConfig,
    groups: MutableMapping[str, str],
    register_finalizer: GroupFinalizerRegistrar | None = None,
) -> None:
    """Create and configure groups according to given config.

    Config format given in yaml is as follows:

        group_name_1:
            owner: user_name
            [users]:                        ---> optional
                - user_name_2
                - user_name_3:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
            [groups]:                       ---> optional
                - child_group_1
                - child_group_2:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
        group_name_2:
            ...

    Example configuration:

        group1:
            owner: user3
        group2:
            owner: user1
            users:
                - user2:
                    privileges:
                        - group_invite_user
                        - group_remove_user
                - user3
            groups:
                - group1:
                    privileges:
                        - group_view
                        - group_invite_user
                - group3
        group3:
            owner: user2
    """
    _groups_creation(
        config,
        service,
        admin_credentials,
        users,
        hosts,
        groups,
        register_finalizer,
    )


def _groups_creation(
    config: GroupsConfig,
    service: str,
    admin_credentials: CredentialsLike,
    users: Users,
    hosts: HostsConfig,
    groups: MutableMapping[str, str],
    register_finalizer: GroupFinalizerRegistrar | None,
) -> None:
    zone_hostname = hosts[service]["hostname"]

    for group_name, description in config.items():
        owner = users[description["owner"]]

        group_id = _create_group(
            zone_hostname,
            owner.username,
            owner.password,
            group_name,
        )
        if register_finalizer:
            register_finalizer(group_id)
        groups[group_name] = group_id

        for user_entry in description.get("users", []):
            user, privileges = _unpack_member_entry(user_entry)

            _add_user_to_group(
                zone_hostname,
                admin_credentials,
                group_id,
                users[user].user_id,
                privileges,
            )

    for group_name, description in config.items():
        group_id = groups[group_name]
        for child_group_entry in description.get("groups", []):
            child_group, privileges = _unpack_member_entry(child_group_entry)

            child_id = groups[child_group]

            _add_child_group(
                zone_hostname, admin_credentials, group_id, child_id, privileges
            )


def _unpack_member_entry(entry: MemberEntry) -> tuple[str, list[str] | None]:
    if isinstance(entry, str):
        return entry, None
    [(name, options)] = entry.items()
    return name, options["privileges"]


def _create_group(
    zone_hostname: str,
    owner_username: str,
    owner_password: str,
    group_name: str,
    group_type: str = "team",
) -> str:
    group_properties = {"name": group_name, "type": group_type}
    response = http_post(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "groups"),
        auth=(owner_username, owner_password),
        data=json.dumps(group_properties),
    )
    return response.headers["location"].split("/")[-1]


def _add_user_to_group(
    zone_hostname: str,
    admin_credentials: CredentialsLike,
    group_id: str,
    user_id: str,
    privileges: list[str] | None,
) -> None:
    if privileges:
        data = json.dumps({"privileges": privileges})
    else:
        data = None

    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("groups", group_id, "users", user_id),
        auth=(
            admin_credentials.username,
            admin_credentials.password,
        ),
        data=data,
    )


def _add_child_group(
    zone_hostname: str,
    admin_credentials: CredentialsLike,
    parent_id: str,
    child_id: str,
    privileges: list[str] | None,
) -> None:
    if privileges:
        data = json.dumps({"privileges": privileges})
    else:
        data = None

    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("groups", parent_id, "children", child_id),
        auth=(
            admin_credentials.username,
            admin_credentials.password,
        ),
        data=data,
    )


def _get_group_id(
    hosts: HostsConfig, users: Users, user: str, group_name: str
) -> str | None:
    service = "onezone"
    zone_hostname = hosts[service]["hostname"]
    groups_id_list = get_group_id_list(user, users, zone_hostname)
    for group_id in groups_id_list:
        group_details = http_get(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("groups", group_id),
            auth=(user, users[user].password),
        )
        if group_details.json()["name"] == group_name:
            return group_id
    return None


@given(
    parsers.parse(
        "there is no {group_name} group in Onezone page used by "
        "{user} before definition in next steps"
    )
)
def remove_group_in_onezone(
    hosts: HostsConfig, users: Users, user: str, group_name: str
) -> None:
    service = "onezone"
    zone_hostname = hosts[service]["hostname"]
    group_id = _get_group_id(hosts, users, user, group_name)
    if group_id:
        http_delete(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("groups", group_id),
            auth=(user, users[user].password),
        )


@given(
    parsers.parse(
        "there is no groups in Onezone page used by {user} before "
        "definition in next steps"
    )
)
def remove_all_groups_rest(user: str, hosts: HostsConfig, users: Users) -> None:
    zone_hostname = hosts["onezone"]["hostname"]

    groups_id_list = get_group_id_list(user, users, zone_hostname)

    for group in groups_id_list:
        _try_to_remove_group(group, zone_hostname, user, users)


def _try_to_remove_group(
    group_id: str, zone_hostname: str, user: str, users: Users
) -> None:
    try:
        http_delete(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("groups", group_id),
            auth=(user, users[user].password),
        )
    except HTTPForbidden:
        pass


def get_group_id_list(user: str, users: Users, zone_hostname: str) -> list[str]:
    groups_list = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("groups"),
        auth=(user, users[user].password),
    )
    return groups_list.json()["groups"]


@wt(parsers.parse(r"using REST, user {user} creates {number} groups"))
def create_n_groups_using_rest(
    user: str,
    users: Users,
    hosts: HostsConfig,
    number: str,
    request: pytest.FixtureRequest,
    admin_credentials: CredentialsLike,
    host: str = "onezone",
) -> None:
    zone_hostname = hosts[host]["hostname"]
    for i in range(int(number)):
        group_name = f"group{i}"
        group_id = _create_group(
            zone_hostname,
            users[user].username,
            users[user].password,
            group_name,
        )
        _register_group_finalizer(request, zone_hostname, admin_credentials, group_id)
