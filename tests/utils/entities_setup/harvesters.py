"""Steps for harvesters management using REST API."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from collections.abc import Mapping, MutableMapping
from typing import Optional

from tests import ELASTICSEARCH_PORT, OZ_REST_PORT
from tests.gui.utils.generic import ELEMENTS_SEQUENCE_PATTERN, parse_elements_sequence
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.rest_utils import (
    get_zone_rest_path,
    http_delete,
    http_get,
    http_post,
    http_put,
)
from tests.utils.user_utils import Users

HostsConfig = Mapping[str, Mapping[str, str]]
IdMap = Mapping[str, str]
MutableIdMap = MutableMapping[str, str]


@given(
    parsers.re(
        r"using REST, user (?P<user>.*) creates "
        rf"(?P<harvesters_list>{ELEMENTS_SEQUENCE_PATTERN}) harvesters? in"
        r' "(?P<service>.*)" '
        r"Onezone service"
    ),
    converters={
        "harvesters_list": parse_elements_sequence,
    },
)
@given(
    parsers.re(
        rf"user (?P<user>.*) has (?P<harvesters_list>{ELEMENTS_SEQUENCE_PATTERN})"
        r" harvesters? "
        r'in "(?P<service>.*)" Onezone service'
    ),
    converters={
        "harvesters_list": parse_elements_sequence,
    },
)
def create_harvesters_rest(
    user: str,
    harvesters_list: list[str],
    service: str,
    hosts: HostsConfig,
    users: Users,
    harvesters: MutableIdMap,
) -> None:
    zone_hostname = hosts[service]["hostname"]
    owner = users[user]
    plugin = "elasticsearch_harvesting_backend"
    endpoint = f'{hosts["elasticsearch"]["name"]}:{ELASTICSEARCH_PORT}'

    for harvester in harvesters_list:
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
    zone_hostname: str,
    owner_username: str,
    owner_password: Optional[str],
    harvester_name: str,
    endpoint: str,
    plugin: str,
    harvesters: MutableIdMap,
) -> None:
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
    zone_hostname: str,
    owner_username: str,
    owner_password: Optional[str],
    harvester_id: str,
) -> None:
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
def remove_all_harvesters_rest(user: str, hosts: HostsConfig, users: Users) -> None:
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
    harvester_id: str, zone_hostname: str, user: str, users: Users
) -> None:
    http_delete(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("harvesters", harvester_id),
        auth=(user, users[user].password),
    )


@given(
    parsers.re(
        rf"spaces? (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) belongs? to "
        r'"(?P<harvester_name>.*)" harvester of user '
        r"(?P<username>.*)"
    ),
    converters={"space_list": parse_elements_sequence},
)
def g_add_space_to_harvester(
    space_list: list[str],
    harvester_name: str,
    spaces: IdMap,
    harvesters: IdMap,
    hosts: HostsConfig,
    username: str,
    users: Users,
) -> None:
    add_space_to_harvester(
        space_list, harvester_name, spaces, harvesters, hosts, username, users
    )


@wt(
    parsers.re(
        r"using REST, user (?P<username>.*) adds spaces? "
        rf'(?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) to "(?P<harvester_name>.*)"'
        r" harvester"
    ),
    converters={"space_list": parse_elements_sequence},
)
def wt_add_space_to_harvester(
    space_list: list[str],
    harvester_name: str,
    spaces: IdMap,
    harvesters: IdMap,
    hosts: HostsConfig,
    username: str,
    users: Users,
) -> None:
    add_space_to_harvester(
        space_list, harvester_name, spaces, harvesters, hosts, username, users
    )


def add_space_to_harvester(
    space_list: list[str],
    harvester_name: str,
    spaces: IdMap,
    harvesters: IdMap,
    hosts: HostsConfig,
    username: str,
    users: Users,
) -> None:
    for space in space_list:
        _add_space_to_harvester(
            space, harvester_name, spaces, harvesters, hosts, username, users
        )


def _add_space_to_harvester(
    space_name: str,
    harvester_name: str,
    spaces: IdMap,
    harvesters: IdMap,
    hosts: HostsConfig,
    username: str,
    users: Users,
) -> None:
    space_id = spaces[space_name]
    harvester_id = harvesters[harvester_name]
    zone_hostname = hosts["onezone"]["hostname"]

    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("harvesters", harvester_id, "spaces", space_id),
        auth=(username, users[username].password),
    )
