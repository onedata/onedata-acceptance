"""Steps for shares management using REST API."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json

import yaml

from tests import OP_REST_PORT, OZ_REST_PORT
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.entities_setup.spaces import create_empty_file, get_file_id_by_rest
from tests.utils.rest_utils import (
    get_provider_rest_path,
    get_zone_rest_path,
    http_get,
    http_post,
    http_put,
)


@given(
    parsers.parse(
        'using REST, user {user} creates "{share_name}" share of '
        '"{item_path}" supported by "{provider}" provider'
    )
)
def create_share_using_rest(
    item_path, provider, user, share_name, hosts, users, shares
):
    provider_hostname = hosts[provider]["hostname"]
    file_id = get_file_id_by_rest(item_path, provider_hostname, user, users)

    share_details = {"name": share_name, "fileId": file_id}

    res = http_post(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("shares"),
        headers={"X-Auth-Token": users[user].token},
        data=json.dumps(share_details),
    )
    shares[share_name] = res.json()["shareId"]


@wt(
    parsers.parse(
        'using REST, user {user} creates "{share_name}" share of '
        '"{item_path}" supported by "{provider}" provider'
    )
)
def wt_create_share_using_rest(
    item_path, provider, user, share_name, hosts, users, shares
):
    create_share_using_rest(item_path, provider, user, share_name, hosts, users, shares)


@given(parsers.parse("using REST, user {user} creates following shares:\n{config}"))
def create_many_shares_using_rest(user, config, hosts, users, shares):
    """Config:

    - name: share name
      path: path of file to make share for
      provider: provider that supports space

    """
    _create_many_shares_using_rest(user, config, hosts, users, shares)


def _create_many_shares_using_rest(user, config, hosts, users, shares):
    data = yaml.load(config, yaml.Loader)
    for share in data:
        name = share["name"]
        path = share["path"]
        provider = share["provider"]

        create_share_using_rest(path, provider, user, name, hosts, users, shares)


@given(parsers.parse("user {user} is added to mock handle service in {host}"))
def add_user_to_handle_service(user, users, host, hosts):
    zone_hostname = hosts[transform(host)]["hostname"]
    handle_service_id = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handle_services"),
        headers={"X-Auth-Token": users["admin"].token},
    ).json()["handle_services"][0]
    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path(
            "handle_services", handle_service_id, "users", users[user].user_id
        ),
        headers={"X-Auth-Token": users["admin"].token},
    )


@wt(
    parsers.parse(
        'using REST, {user} creates {number} shares in space "{space_name}" in {host}'
    )
)
def create_n_shares_in_space(users, user, hosts, host, number: int, space_name, shares):
    for i in range(number):
        create_empty_file(f"{space_name}/file{i}", users, user, host, hosts)
        create_share_using_rest(
            f"{space_name}/file{i}", host, user, f"share{i}", hosts, users, shares
        )
