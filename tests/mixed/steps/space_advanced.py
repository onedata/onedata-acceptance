"""This module contains gherkin steps to run acceptance tests featuring
advanced operations on spaces in Onezone using REST API mixed with web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.mixed.steps.rest.oneprovider.data import (
    _lookup_file_id,
    create_empty_file_in_dir_rest,
    create_share_rest,
)
from tests.mixed.utils.common import login_to_provider
from tests.utils.bdd_utils import parsers, wt
from tests.utils.entities_setup.spaces import _create_space, _get_support


@wt(
    parsers.parse(
        'using REST, {user} creates {number} spaces in "{zone_host}" Onezone service'
    )
)
def create_n_spaces_without_support(zone_host, users, user, hosts, number: int):
    name_prefix = "space"
    zone_hostname = hosts[zone_host]["hostname"]
    # let spaces names be space0, space1, ... space(n-1)
    owner = users[user]
    for i in range(number):
        space_name = f"{name_prefix}{i}"
        _create_space(zone_hostname, owner.username, owner.password, space_name)


@wt(
    parsers.parse(
        'using REST, {user} creates {number} spaces each with share in "{zone_host}"'
        " Onezone service"
    )
)
def create_n_spaces_with_shares(
    zone_host, users, user, hosts, number: int, onepanel_credentials, storages
):
    name_prefix = "space"
    host = "oneprovider-1"
    zone_hostname = hosts[zone_host]["hostname"]
    users_to_add = []
    providers = [{"oneprovider-1": {"storage": "posix", "size": 1000000}}]
    # let spaces names be space0, space1, ... space(n-1)
    owner = users[user]
    for i in range(number):
        space_name = f"{name_prefix}{i}"
        space_id = _create_space(
            zone_hostname, owner.username, owner.password, space_name
        )
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
        create_empty_file_in_dir_rest(users, user, hosts, host, space_id, f"file{i}")
        client = login_to_provider(user, users, hosts[host]["hostname"])
        file_id = _lookup_file_id(f"{space_name}/file{i}", client)
        create_share_rest(users, user, hosts, host, file_id, f"share{i}")
