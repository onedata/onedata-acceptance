"""Steps for harvesters management using REST API."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from collections.abc import Mapping, MutableMapping

from pytest import FixtureRequest

from tests import ELASTICSEARCH_PORT, OZ_REST_PORT
from tests.gui.utils.generic import ELEMENTS_SEQUENCE_PATTERN, parse_elements_sequence
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.http_exceptions import HTTPNotFound
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
        r' "(?P<service>.*)" Onezone service'
    ),
    converters={
        "harvesters_list": parse_elements_sequence,
    },
)
@given(
    parsers.re(
        rf"user (?P<user>.*) has (?P<harvesters_list>{ELEMENTS_SEQUENCE_PATTERN})"
        r' harvesters? in "(?P<service>.*)" Onezone service'
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
    request: FixtureRequest,
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
            request,
        )


def _create_harvester(
    zone_hostname: str,
    owner_username: str,
    owner_password: str | None,
    harvester_name: str,
    endpoint: str,
    plugin: str,
    harvesters: MutableIdMap,
    request: FixtureRequest,
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
    harvester_id = response.headers["Location"].split("/")[-1]
    harvesters[harvester_name] = harvester_id

    request.addfinalizer(
        lambda: _remove_harvester(
            harvester_id, zone_hostname, owner_username, owner_password
        )
    )

    _create_harvester_gui_index(
        zone_hostname, owner_username, owner_password, harvester_id
    )


def _create_harvester_gui_index(
    zone_hostname: str,
    owner_username: str,
    owner_password: str | None,
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
    password = users[user].password

    for harvester_id in get_user_harvester_ids(zone_hostname, user, password):
        _remove_harvester(harvester_id, zone_hostname, user, password)


def get_user_harvester_ids(
    zone_hostname: str,
    username: str,
    password: str | None,
) -> set[str]:
    response = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "harvesters"),
        auth=(username, password),
    )

    return set(response.json()["harvesters"])


def _remove_harvester(
    harvester_id: str,
    zone_hostname: str,
    owner_username: str,
    owner_password: str | None,
) -> None:
    try:
        http_delete(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("harvesters", harvester_id),
            auth=(owner_username, owner_password),
        )
    except HTTPNotFound:
        # A scenario may explicitly remove the harvester before its finalizer runs.
        pass


@given(
    parsers.re(
        rf"spaces? (?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) belongs? to "
        r'"(?P<harvester_name>.*)" harvester of user (?P<username>.*)'
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
        rf"(?P<space_list>{ELEMENTS_SEQUENCE_PATTERN}) to "
        r'"(?P<harvester_name>.*)" harvester'
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
