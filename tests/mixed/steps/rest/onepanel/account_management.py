"""Utils and fixtures to facilitate account management operations in Onepanel
using REST API.
"""

from collections.abc import Mapping
from typing import NoReturn, Protocol

from tests.conftest import Hosts

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


class UserLike(Protocol):
    password: str


def change_user_password_in_oz_panel_using_rest(
    user: str,
    new_password: str,
    zone_host: str,
    users: Mapping[str, UserLike],
    hosts: Hosts,
) -> NoReturn:
    raise NotImplementedError
    # TODO VFS-12393 uncomment after resolving issues with import OnepanelApi
    # user_client = login_to_panel(
    #     user, users[user].password, hosts[zone_host]["hostname"]
    # )
    # onepanel_api = OnepanelApi(user_client)
    # user_mod_rq = UserModifyRequest(users[user].password, new_password)
    # onepanel_api.modify_user(user, user_mod_rq)


def login_to_oz_panel_using_new_password_rest(
    user: str, password: str, hosts: Hosts, zone_host: str
) -> NoReturn:
    # client = login_to_panel(user, password, hosts[zone_host]["hostname"])

    raise NotImplementedError
    # TODO VFS-12393 uncomment after resolving issues with import OnepanelApi
    # to confirm that new credentials are correct we have to perform some
    # operation
    # onepanel_api = OnepanelApi(client)
    # onepanel_api.get_user(user)
