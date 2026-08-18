"""This module contains gherkin steps to run acceptance tests featuring
advanced operations on spaces in Onezone using REST API mixed with web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from pytest import FixtureRequest

from tests.gui.meta_steps.rest.shares import create_share_using_rest
from tests.type_definitions import Hosts
from tests.utils.bdd_utils import parsers, wt
from tests.utils.entities_setup.spaces import (
    CredentialsLike,
    ProviderEntry,
    _create_space,
    _get_support,
    _register_space_finalizer,
    create_empty_file,
)
from tests.utils.user_utils import User, Users


@wt(
    parsers.parse(
        'using REST, {user} creates {number} spaces in "{zone_host}" Onezone service'
    )
)
def create_n_spaces_without_support(
    zone_host: str,
    users: Users,
    user: str,
    hosts: Hosts,
    number: str,
    request: FixtureRequest,
    admin_credentials: CredentialsLike,
) -> None:
    name_prefix = "space"
    zone_hostname = hosts[zone_host]["hostname"]
    # let spaces names be space0, space1, ... space(n-1)
    owner = users[user]
    for i in range(int(number)):
        space_name = f"{name_prefix}{i}"
        space_id = _create_space(
            zone_hostname,
            owner.username,
            owner.password,
            space_name,
        )
        _register_space_finalizer(request, zone_hostname, admin_credentials, space_id)


@wt(
    parsers.parse(
        "using REST, {user} creates {number} spaces with one share for each, in"
        ' "{zone_host}" Onezone service'
    )
)
def create_n_spaces_with_shares(
    zone_host: str,
    users: Users,
    user: str,
    hosts: Hosts,
    number: str,
    onepanel_credentials: User,
    storages: dict,
    shares: dict[str, str],
    request: FixtureRequest,
    admin_credentials: CredentialsLike,
) -> None:
    name_prefix = "space"
    host = "oneprovider-1"
    zone_hostname = hosts[zone_host]["hostname"]
    users_to_add: list[str] = []
    providers: list[ProviderEntry] = [
        {"oneprovider-1": {"storage": "posix", "size": 1000000}}
    ]
    # let spaces names be space0, space1, ... space(n-1)
    owner = users[user]
    for i in range(int(number)):
        space_name = f"{name_prefix}{i}"
        space_id = _create_space(
            zone_hostname,
            owner.username,
            owner.password,
            space_name,
        )
        _register_space_finalizer(request, zone_hostname, admin_credentials, space_id)
        _get_support(
            zone_hostname,
            onepanel_credentials,
            owner,
            space_id,
            storages,
            hosts,
            providers,
            users_to_add,
            users,
        )
        file_path = f"{space_name}/file{i}"
        create_empty_file(file_path, users, user, host, hosts)
        create_share_using_rest(
            file_path, host, user, f"share{i}", hosts, users, shares
        )
