"""This module contains steps for operations on tokens in Onezone
using REST.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import base64
import time
from collections.abc import Mapping
from typing import Optional, Protocol, cast

import yaml
from onezone_client import TokenApi

from tests.conftest import Hosts, Tokens
from tests.gui.types import TmpMemory
from tests.mixed.steps.rest.onezone.members import (
    translate_privileges,
)
from tests.mixed.types import (
    ConfigMap,
    GroupMap,
    PrivilegeGroupConfig,
    SpaceMap,
    TokenCaveat,
    TokenConfig,
    TokenValue,
)
from tests.mixed.utils.common import login_to_oz


class UserLike(Protocol):
    password: str
    user_id: str


class InviteTokenLike(Protocol):
    invite_type: str


class TokenTypeLike(Protocol):
    invite_token: InviteTokenLike


class TokenMetadataLike(Protocol):
    privileges: list[str]


class NamedTokenLike(Protocol):
    type: TokenTypeLike
    caveats: list[TokenCaveat]
    metadata: TokenMetadataLike


def _token_caveats(token_config: TokenConfig) -> list[TokenCaveat]:
    return cast(list[TokenCaveat], token_config["caveats"])


def create_token_with_config_rest(
    user: str,
    config: str,
    users: Mapping[str, UserLike],
    tokens: Tokens,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    groups: GroupMap,
    spaces: SpaceMap,
) -> None:
    """Create token according to given config.

    Config format given in yaml is as follows:

            name: token_name
            type: access/identity/invite
            invite type: type_of_invite
            invite target: target of invite        ---> optional
            usage limit: number > 0 or infinity    ---> optional, default:
                                                                  infinity
            caveats:                               ---> optional
                caveat_type_1:
                    caveat config:
            ...

    Example configuration:

          type: invite
          invite type: Invite harvester to space
          invite target: space1
          usage limit: infinity
          caveats:
            expiration:
                after: count (in minutes)
            region:
                allow: True/False, default True
                region codes:
                    - Europe
                    - Asia
            IP:
              - 127.0.0.1
            consumer:
              - type: group
                by: id
                consumer name: group2
              - type: user
                by: name
                consumer name: user1

    """
    _create_token_with_config(
        user,
        config,
        users,
        hosts,
        tmp_memory,
        tokens,
        groups,
        spaces,
        zone_name="onezone",
    )


translation_dict = {
    "Invite user to space": {"type": "userJoinSpace", "target": "spaceId"}
}


def _create_token_with_config(
    user: str,
    config: str,
    users: Mapping[str, UserLike],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    tokens: Tokens,
    groups: GroupMap,
    spaces: SpaceMap,
    zone_name: str,
) -> None:
    data = cast(ConfigMap, yaml.load(config, yaml.Loader))
    name = cast(str, data["name"])
    token_type = cast(str, data["type"])
    usage_limit = data.get("usage limit", False)
    caveats = data.get("caveats", False)
    privileges = data.get("privileges", False)

    token_variant: dict[str, TokenValue] = {}
    token_type_config: dict[str, TokenValue] = {f"{token_type}Token": token_variant}
    token_config: TokenConfig = {
        "name": name,
        "type": token_type_config,
    }
    if token_type == "invite":
        invite_type = cast(str, data["invite type"])
        invite_target = cast(Optional[str], data.get("invite target"))

        invite_type_rest = translation_dict[invite_type]["type"]

        token_variant["inviteType"] = invite_type_rest
        if invite_target:
            target = translation_dict[invite_type]["target"]
            if "space" in invite_target:
                invite_target = spaces[invite_target]
            token_variant[target] = invite_target

    if usage_limit:
        token_config["usageLimit"] = usage_limit
    if caveats:
        parse_token_caveats(
            cast(ConfigMap, caveats), token_config, groups, users, spaces, tmp_memory
        )
    if privileges:
        grant: list[str] = []
        revoke: list[str] = []
        translate_privileges(
            cast(Mapping[str, PrivilegeGroupConfig], privileges), grant, revoke
        )
        grant.sort()
        token_config["privileges"] = grant

    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])
    token_api = TokenApi(user_client)
    response = token_api.create_named_token_for_current_user(data=token_config)
    token = response.token
    token_id = response.token_id
    tmp_memory[user]["token"] = token
    tokens[name] = {"token_id": token_id, "token": token}


def parse_token_caveats(
    caveats: ConfigMap,
    token_config: TokenConfig,
    groups: GroupMap,
    users: Mapping[str, UserLike],
    spaces: SpaceMap,
    tmp_memory: TmpMemory,
) -> None:
    token_config["caveats"] = []
    expiration = caveats.get("expiration", False)
    region = caveats.get("region", False)
    country = caveats.get("country", False)
    asn = caveats.get("ASN", False)
    ip = caveats.get("IP", False)
    consumer = caveats.get("consumer", False)
    service = caveats.get("service", False)
    interface = caveats.get("interface", False)
    readonly = caveats.get("read only", False)
    path = caveats.get("path", False)
    object_id = caveats.get("object ID", False)

    if expiration:
        set_expiration_caveat(token_config, cast(ConfigMap, expiration), tmp_memory)
    if region:
        set_geo_caveat(token_config, cast(ConfigMap, region), "region")
    if country:
        set_geo_caveat(token_config, cast(ConfigMap, country), "country")
    if asn:
        set_address_caveat(token_config, cast(list[str], asn), "ASN")
    if ip:
        set_address_caveat(token_config, cast(list[str], ip), "IP")
    if consumer:
        set_consumer_caveat(
            token_config, cast(list[Mapping[str, str]], consumer), groups, users
        )
    if service:
        set_service_caveat(token_config, cast(Mapping[str, list[str]], service))
    if interface:
        set_interface_caveat(token_config, cast(str, interface))
    if readonly:
        set_readonly_caveat(token_config)
    if path:
        set_path_caveat(token_config, cast(list[Mapping[str, str]], path), spaces)
    if object_id:
        set_object_id_caveat(token_config, cast(list[str], object_id))


def set_expiration_caveat(
    token_config: TokenConfig, expiration: ConfigMap, tmp_memory: TmpMemory
) -> None:
    time_to = int(time.time()) + cast(int, expiration["after"]) * 60
    _token_caveats(token_config).append({"type": "time", "validUntil": time_to})
    tmp_memory["expire_time"] = time.strftime(
        "%Y/%m/%d %-H:%M", time.localtime(time_to)
    )


def set_geo_caveat(token_config: TokenConfig, caveat: ConfigMap, geo_type: str) -> None:
    regions = caveat.get(f"{geo_type} codes", [])
    if caveat.get("allow", False):
        _token_caveats(token_config).append(
            {"type": f"geo.{geo_type}", "filter": "whitelist", "list": regions}
        )
    else:
        _token_caveats(token_config).append(
            {"type": f"geo.{geo_type}", "filter": "blacklist", "list": regions}
        )


def set_address_caveat(
    token_config: TokenConfig, caveat: list[str], address_type: str
) -> None:
    _token_caveats(token_config).append(
        {"type": address_type.lower(), "whitelist": caveat}
    )


def set_consumer_caveat(
    token_config: TokenConfig,
    caveat: list[Mapping[str, str]],
    groups: GroupMap,
    users: Mapping[str, UserLike],
) -> None:
    consumer_list = []
    for consumer in caveat:
        consumer_list.append(set_consumer_in_consumer_caveat(consumer, groups, users))
    _token_caveats(token_config).append(
        {"type": "consumer", "whitelist": consumer_list}
    )


def set_consumer_in_consumer_caveat(
    consumer: Mapping[str, str], groups: GroupMap, users: Mapping[str, UserLike]
) -> str:
    cons_type = consumer.get("type", "user")
    cons_name = consumer.get("consumer name", "")
    if cons_type == "user":
        value = "usr-*" if "any" in cons_name else f"usr-{users[cons_name].user_id}"
    elif cons_type == "group":
        value = "grp-*" if "any" in cons_name else f"grp-{groups[cons_name]}"
    else:
        value = "prv-*"
    return value


def set_service_caveat(
    token_config: TokenConfig, given_service: Mapping[str, list[str]]
) -> None:
    services_list = []
    service = given_service.get("Service", [])
    op_service = given_service.get("Service Onepanel", [])
    if service:
        for curr_service in service:
            if curr_service == "Any Oneprovider":
                services_list.append("opw-*")
            else:
                if curr_service == "dev-onezone":
                    curr_service = "onezone"
                services_list.append(f"ozw-{curr_service}")
    if op_service:
        for curr_service in op_service:
            if "onezone" in curr_service.lower():
                services_list.append("ozp-onezone")
            if "oneprovider onepanel" in curr_service.lower():
                services_list.append("opp-*")
            elif "oneprovider" in curr_service.lower():
                services_list.append(f"opw-{curr_service}")

    _token_caveats(token_config).append({"type": "service", "whitelist": services_list})


def set_interface_caveat(token_config: TokenConfig, service: str) -> None:
    _token_caveats(token_config).append(
        {"type": "interface", "interface": service.lower()}
    )


def set_readonly_caveat(token_config: TokenConfig) -> None:
    _token_caveats(token_config).append({"type": "data.readonly"})


def set_path_caveat(
    token_config: TokenConfig, paths: list[Mapping[str, str]], spaces: SpaceMap
) -> None:
    whitelist = []
    for path in paths:
        whitelist.append(decode_path(path, spaces))
    _token_caveats(token_config).append({"type": "data.path", "whitelist": whitelist})


def decode_path(path: Mapping[str, str], spaces: SpaceMap) -> str:
    space = spaces[path["space"]]
    file_path = path["path"]
    file_path = "" if file_path == "/" else file_path
    can_path = f"/{space}{file_path}"
    encoded = base64.b64encode(can_path.encode("ascii"))
    return encoded.decode("ascii")


def set_object_id_caveat(token_config: TokenConfig, object_ids: list[str]) -> None:
    whitelist = list(object_ids)
    _token_caveats(token_config).append(
        {"type": "data.objectid", "whitelist": whitelist}
    )


def revoke_token_rest(
    user: str,
    users: Mapping[str, UserLike],
    hosts: Hosts,
    zone_name: str,
    tokens: Tokens,
    token_name: str,
) -> None:
    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])
    token_api = TokenApi(user_client)

    token = tokens.get(token_name, None)
    if token:
        token_id = token["token_id"]
    else:
        token_id = token_api.get_named_token_of_current_user_by_name(token_name).id
    token_config = {"revoked": True}
    token_api.modify_named_token(id=token_id, data=token_config)


def assert_token_with_config_rest(
    user: str,
    config: str,
    users: Mapping[str, UserLike],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    groups: GroupMap,
    spaces: SpaceMap,
    zone_name: str = "onezone",
) -> None:
    data = cast(ConfigMap, yaml.load(config, yaml.Loader))

    name = cast(str, data["name"])
    token_type = cast(str, data["type"])
    invite_type = data.get("invite type", False)
    privileges = data.get("privileges", False)
    caveats = data.get("caveats", False)

    user_client = login_to_oz(user, users[user].password, hosts[zone_name]["hostname"])
    token_api = TokenApi(user_client)
    response = token_api.get_named_token_of_current_user_by_name(name)

    assert_token_type(token_type.lower(), response)
    if invite_type:
        assert_invite_type(cast(str, invite_type), response)
    if caveats:
        assert_token_caveats(
            cast(ConfigMap, caveats), response, groups, users, spaces, tmp_memory
        )
    if privileges:
        assert_token_privileges(cast(ConfigMap, privileges), response)


def assert_token_type(token_type: str, token: NamedTokenLike) -> None:
    assert (
        getattr(token.type, f"{token_type}_token") is not None
    ), f"token is not {token_type}"


def assert_invite_type(invite_type: str, token: NamedTokenLike) -> None:
    actual = token.type.invite_token.invite_type
    expected = translation_dict[invite_type]["type"]
    assert (
        actual == expected
    ), f"Invite token invite type {actual} is not as expected {expected}"


def get_caveat(caveat_name: str, caveats: list[TokenCaveat]) -> TokenCaveat:
    caveat = [cav for cav in caveats if cav["type"] == caveat_name][0]
    assert len(caveat), f"Caveat {caveat_name} not in token configuration"
    return caveat


def assert_token_caveats(
    caveats: ConfigMap,
    token: NamedTokenLike,
    groups: GroupMap,
    users: Mapping[str, UserLike],
    spaces: SpaceMap,
    tmp_memory: TmpMemory,
) -> None:
    expiration = caveats.get("expiration", False)
    region = caveats.get("region", False)
    country = caveats.get("country", False)
    asn = caveats.get("ASN", False)
    ip = caveats.get("IP", False)
    consumer = caveats.get("consumer", False)
    service = caveats.get("service", False)
    interface = caveats.get("interface", False)
    readonly = caveats.get("read only", False)
    path = caveats.get("path", False)
    object_id = caveats.get("object ID", False)

    if expiration:
        assert_expiration_caveat(
            get_caveat("time", token.caveats), cast(ConfigMap, expiration), tmp_memory
        )
    if region:
        assert_geo_caveat(
            get_caveat("geo.region", token.caveats),
            cast(ConfigMap, region),
            "region",
        )
    if country:
        assert_geo_caveat(
            get_caveat("geo.country", token.caveats),
            cast(ConfigMap, country),
            "country",
        )
    if asn:
        assert_address_caveat(
            get_caveat("asn", token.caveats), cast(list[str], asn), "ASN"
        )
    if ip:
        assert_address_caveat(
            get_caveat("ip", token.caveats), cast(list[str], ip), "IP"
        )
    if consumer:
        assert_consumer_caveat(
            get_caveat("consumer", token.caveats),
            cast(list[Mapping[str, str]], consumer),
            groups,
            users,
        )
    if service:
        assert_service_caveat(
            get_caveat("service", token.caveats), cast(list[str], service)
        )
    if interface:
        assert_interface_caveat(
            get_caveat("interface", token.caveats), cast(str, interface)
        )
    if readonly:
        get_caveat("data.readonly", token.caveats)
    if path:
        assert_path_caveat(
            get_caveat("data.path", token.caveats),
            cast(list[Mapping[str, str]], path),
            spaces,
        )
    if object_id:
        assert_object_id_caveat(
            get_caveat("data.objectid", token.caveats), cast(list[str], object_id)
        )


def assert_expiration_caveat(
    token_caveat: ConfigMap,
    expiration: ConfigMap,
    tmp_memory: TmpMemory,
) -> None:
    if expiration["set"]:
        exp_time = cast(str | float, tmp_memory["expire_time"])
        if isinstance(exp_time, str) and "/" in exp_time:
            str_time = time.strptime(exp_time, "%Y/%m/%d %H:%M")
            exp_time = time.mktime(str_time)
        assert (
            token_caveat["validUntil"] == exp_time
        ), f"Wrong expiration time caveat: exp: {exp_time}, given: {token_caveat}"


def assert_geo_caveat(
    token_caveat: ConfigMap,
    expected_caveat: ConfigMap,
    geo_type: str,
) -> None:
    regions = cast(list[str], expected_caveat.get(f"{geo_type} codes", []))
    if expected_caveat.get("allow", False):
        assert (
            token_caveat["filter"] == "whitelist"
        ), f"{geo_type} caveat is blacklisted while should be whitelisted"
    else:
        assert (
            token_caveat["filter"] == "blacklist"
        ), f"{geo_type} caveat is whitelisted while should be blacklisted"
    token_list = cast(list[str], token_caveat["list"])
    assert len(token_list) == len(
        regions
    ), f"Token {geo_type} list {token_list} is not as long as expected {regions}"
    for region in regions:
        assert region in token_list, f"{geo_type} {region} not in token caveat"


def assert_address_caveat(
    token_caveat: ConfigMap, expected_caveat: list[str], address_type: str
) -> None:
    token_list = cast(list[str], token_caveat["whitelist"])
    assert len(token_list) == len(expected_caveat), (
        f"Expected {address_type} caveat list {expected_caveat} is "
        "not as long as actual token_caveat whitelist "
        f"{token_caveat['whitelist']}"
    )
    for address in expected_caveat:
        assert (
            address in token_list
        ), f"{address}  {address_type} address not in token caveat"


def assert_consumer_caveat(
    token_caveat: ConfigMap,
    expected_caveat: list[Mapping[str, str]],
    groups: GroupMap,
    users: Mapping[str, UserLike],
) -> None:
    token_list = cast(list[str], token_caveat["whitelist"])
    assert len(token_list) == len(expected_caveat), (
        f"Expected consumer caveat list {expected_caveat} is "
        f"not as long as actual token caveat whitelist {token_list}"
    )

    for consumer in expected_caveat:
        assert_consumer_in_consumer_caveat(consumer, token_list, groups, users)


def assert_consumer_in_consumer_caveat(
    consumer: Mapping[str, str],
    token_list: list[str],
    groups: GroupMap,
    users: Mapping[str, UserLike],
) -> None:
    value = set_consumer_in_consumer_caveat(consumer, groups, users)
    assert value in token_list, f"{consumer} not in consumer token caveat"


def assert_service_caveat(token_caveat: ConfigMap, expected_caveat: list[str]) -> None:
    services_list = []
    token_list = cast(list[str], token_caveat["whitelist"])
    services = [service for service in expected_caveat if "Onepanel" not in service]
    op_service = [service for service in expected_caveat if "Onepanel" in service]

    for curr_service in services:
        if curr_service == "Any Oneprovider":
            services_list.append("opw-*")
        else:
            services_list.append(f"ozw-{curr_service}")
    for curr_service in op_service:
        if "onezone" in curr_service.lower():
            services_list.append("ozp-onezone")
        if "oneprovider onepanel" in curr_service.lower():
            services_list.append("opp-*")
        elif "oneprovider" in curr_service.lower():
            services_list.append(f"opw-{curr_service}")

    assert len(token_list) == len(services_list), (
        f"Expected {services_list} and actual {token_list} "
        "services lists have different length"
    )

    for service in services_list:
        assert service in token_list, f"Expected service {service} not in {token_list}"


def assert_interface_caveat(token_caveat: ConfigMap, expected_caveat: str) -> None:
    assert (
        token_caveat["interface"] == expected_caveat.lower()
    ), f"Interface {expected_caveat} not set in token caveat"


def assert_path_caveat(
    token_caveat: ConfigMap,
    expected_caveat: list[Mapping[str, str]],
    spaces: SpaceMap,
) -> None:
    token_list = cast(list[str], token_caveat["whitelist"])
    whitelist = []
    for path in expected_caveat:
        decoded_path = decode_path(path, spaces)
        whitelist.append(decoded_path)

        assert decoded_path in token_list, f"Path {path} not in {token_list}"

    assert len(token_list) == len(
        whitelist
    ), f"Expected {whitelist} and actual {token_list} paths lists have different length"


def assert_object_id_caveat(
    token_caveat: ConfigMap, expected_caveat: list[str]
) -> None:
    token_list = cast(list[str], token_caveat["whitelist"])
    assert len(token_list) == len(expected_caveat), (
        f"Expected objectID caveat list {expected_caveat} is "
        f"not as long as actual token caveat whitelist {token_list}"
    )

    for object_id in expected_caveat:
        assert object_id in token_list, f"Object id {object_id} not in token"


privileges_translation = {
    "Space management": {
        "View space": "space_view",
    },
    "Data management": {
        "Read files": "space_read_data",
        "Write files": "space_write_data",
    },
    "Transfer management": {"View transfers": "space_view_transfers"},
}


def assert_token_privileges(privileges: ConfigMap, response: NamedTokenLike) -> None:
    actual_privs = response.metadata.privileges
    expected_privs = []
    for priv_group, priv_group_items in privileges.items():
        sub_privs = cast(
            Mapping[str, bool], cast(ConfigMap, priv_group_items)["privilege subtypes"]
        )
        for priv in sub_privs:
            if sub_privs[priv]:
                expected_privs.append(privileges_translation[priv_group][priv])

    for priv in expected_privs:
        assert priv in actual_privs, f"{priv} not in {actual_privs}"
    assert len(expected_privs) == len(
        actual_privs
    ), "Expected and actual privileges lists are not equal"
