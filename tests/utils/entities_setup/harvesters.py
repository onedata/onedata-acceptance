"""Steps for harvesters management using REST API."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from typing import Any

from tests import ELASTICSEARCH_PORT, OZ_REST_PORT
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.rest_utils import (
    get_zone_rest_path,
    http_delete,
    http_get,
    http_post,
    http_put,
)


@given(
    parsers.re(
        "using REST, user (?P<user>.*) creates "
        '(?P<harvesters_list>.*) harvesters? in "(?P<service>.*)" '
        "Onezone service"
    )
)
@given(
    parsers.re(
        "user (?P<user>.*) has (?P<harvesters_list>.*) harvesters? "
        'in "(?P<service>.*)" Onezone service'
    )
)
def create_harvesters_rest(
    user: Any,
    harvesters_list: Any,
    service: Any,
    hosts: Any,
    users: Any,
    harvesters: Any,
) -> Any:
    zone_hostname = hosts[service]["hostname"]
    owner = users[user]
    plugin = "elasticsearch_harvesting_backend"
    endpoint = f'{hosts["elasticsearch"]["name"]}:{ELASTICSEARCH_PORT}'

    for harvester in parse_seq(harvesters_list):
        _create_harvester(
            zone_hostname,
            owner.username,
            owner.password,
            harvester,
            endpoint,
            plugin,
            harvesters,
        )


def _create_harvester(
    zone_hostname: Any,
    owner_username: Any,
    owner_password: Any,
    harvester_name: Any,
    endpoint: Any,
    plugin: Any,
    harvesters: Any,
) -> Any:
    harvester_details = {
        "name": harvester_name,
        "harvestingBackendEndpoint": endpoint,
        "harvestingBackendType": plugin,
    }

    response = http_post(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "harvesters"),
        auth=(owner_username, owner_password),
        data=json.dumps(harvester_details),
    )

    # set harvester id
    harvesters[harvester_name] = response.headers["Location"].split("/")[-1]

    _create_harvester_gui_index(
        zone_hostname, owner_username, owner_password, harvesters[harvester_name]
    )


def _create_harvester_gui_index(
    zone_hostname: Any, owner_username: Any, owner_password: Any, harvester_id: Any
) -> Any:
    index_details = {
        "name": "generic-index",
        "guiPluginName": "generic-index",
        "includeMetadata": ["json", "xattrs", "rdf"],
        "includeFileDetails": ["fileName", "spaceId", "metadataExistenceFlags"],
        "includeRejectionReason": False,
        "retryOnRejection": True,
    }
    http_post(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("harvesters", harvester_id, "indices"),
        auth=(owner_username, owner_password),
        data=json.dumps(index_details),
    )


@given(parsers.parse("user {user} has no harvesters"))
@given(parsers.parse("user {user} has no harvesters other than defined in next steps"))
def remove_all_harvesters_rest(user: Any, hosts: Any, users: Any) -> Any:
    zone_hostname = hosts["onezone"]["hostname"]

    dict_harvesters = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "harvesters"),
        auth=(user, users[user].password),
    ).json()
    list_harvesters = dict_harvesters["harvesters"]

    for harvester in list_harvesters:
        _remove_harvester(harvester, zone_hostname, user, users)


def _remove_harvester(
    harvester_id: Any, zone_hostname: Any, user: Any, users: Any
) -> Any:
    http_delete(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("harvesters", harvester_id),
        auth=(user, users[user].password),
    )


@given(
    parsers.re(
        "spaces? (?P<space_list>.*) belongs? to "
        '"(?P<harvester_name>.*)" harvester of user '
        "(?P<username>.*)"
    )
)
def g_add_space_to_harvester(
    space_list: Any,
    harvester_name: Any,
    spaces: Any,
    harvesters: Any,
    hosts: Any,
    username: Any,
    users: Any,
) -> Any:
    add_space_to_harvester(
        space_list, harvester_name, spaces, harvesters, hosts, username, users
    )


@wt(
    parsers.re(
        "using REST, user (?P<username>.*) adds spaces? "
        '(?P<space_list>.*) to "(?P<harvester_name>.*)" harvester'
    )
)
def wt_add_space_to_harvester(
    space_list: Any,
    harvester_name: Any,
    spaces: Any,
    harvesters: Any,
    hosts: Any,
    username: Any,
    users: Any,
) -> Any:
    add_space_to_harvester(
        space_list, harvester_name, spaces, harvesters, hosts, username, users
    )


def add_space_to_harvester(
    space_list: Any,
    harvester_name: Any,
    spaces: Any,
    harvesters: Any,
    hosts: Any,
    username: Any,
    users: Any,
) -> Any:
    for space in parse_seq(space_list):
        _add_space_to_harvester(
            space, harvester_name, spaces, harvesters, hosts, username, users
        )


def _add_space_to_harvester(
    space_name: Any,
    harvester_name: Any,
    spaces: Any,
    harvesters: Any,
    hosts: Any,
    username: Any,
    users: Any,
) -> Any:
    space_id = spaces[space_name]
    harvester_id = harvesters[harvester_name]
    zone_hostname = hosts["onezone"]["hostname"]

    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("harvesters", harvester_id, "spaces", space_id),
        auth=(username, users[username].password),
    )
