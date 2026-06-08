"""Steps for users creation using REST API."""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
from typing import Any

import yaml
from pytest import skip
from pytest_bdd import given

from tests import OZ_REST_PORT, PANEL_REST_PORT
from tests.utils.bdd_utils import parsers
from tests.utils.entities_setup.spaces import _rm_all_spaces_for_users_list
from tests.utils.http_exceptions import HTTPBadRequest, HTTPError, HTTPNotFound
from tests.utils.rest_utils import (
    get_panel_rest_path,
    get_zone_rest_path,
    http_delete,
    http_get,
    http_patch,
    http_post,
    http_put,
)
from tests.utils.user_utils import User
from tests.utils.utils import repeat_failed


@given(
    parsers.parse('initial users configuration in "{host}" Onezone service:\n{config}')
)
def users_creation_with_cleanup_step(
    host: Any,
    config: Any,
    admin_credentials: Any,
    onepanel_credentials: Any,
    hosts: Any,
    users: Any,
    rm_users: Any,
) -> Any:
    users_db, zone_hostname = users_creation_with_cleanup(
        host,
        yaml.load(config, yaml.Loader),
        admin_credentials,
        onepanel_credentials,
        hosts,
        users,
        rm_users,
    )

    yield

    _rm_all_spaces_for_users_list(zone_hostname, users_db)
    _cleanup_users(zone_hostname, admin_credentials, users_db)


@given(
    parsers.parse(
        'initial user for future delete configuration in "{host}" '
        "Onezone service:\n{config}"
    )
)
def users_creation_step(
    host: Any,
    config: Any,
    admin_credentials: Any,
    onepanel_credentials: Any,
    hosts: Any,
    users: Any,
    rm_users: Any,
) -> Any:
    return users_creation(
        host,
        yaml.load(config, yaml.Loader),
        admin_credentials,
        onepanel_credentials,
        hosts,
        users,
        rm_users,
    )


def users_creation_with_cleanup(
    host: Any,
    config: Any,
    admin_credentials: Any,
    onepanel_credentials: Any,
    hosts: Any,
    users: Any,
    rm_users: Any,
) -> Any:
    return users_creation(
        host, config, admin_credentials, onepanel_credentials, hosts, users, rm_users
    )


def users_creation(
    host: Any,
    config: Any,
    admin_credentials: Any,
    onepanel_credentials: Any,
    hosts: Any,
    users: Any,
    rm_users: Any,
) -> Any:
    zone_hostname = hosts[host]["hostname"]
    users_db: dict[str, Any] = {}
    for user_config in config:
        username, options = _parse_user_info(user_config)
        try:
            user_cred = _create_user(
                zone_hostname,
                onepanel_credentials,
                admin_credentials,
                username,
                options,
                rm_users,
            )
            _configure_user(zone_hostname, admin_credentials, user_cred, options)
        except Exception as ex:
            _cleanup_users(zone_hostname, admin_credentials, users_db)
            raise ex
        users[username] = users_db[username] = user_cred

    return users_db, zone_hostname


def _parse_user_info(user_config: Any) -> Any:
    try:
        [(username, options)] = user_config.items()
    except AttributeError:
        return user_config, {}
    return username, options


def _create_new_user(
    zone_hostname: Any,
    onepanel_credentials: Any,
    username: Any,
    password: Any,
    user_conf_details: Any,
) -> Any:
    http_post(
        ip=zone_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("zone", "users"),
        auth=(onepanel_credentials.username, onepanel_credentials.password),
        data=json.dumps(user_conf_details),
    )

    # user is created in zone panel and not zone itself
    # so for them to be created also in zone
    # login/rest call to zone using his credentials must be made
    response = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user"),
        auth=(username, password),
    ).json()
    user_id = response["userId"]
    return User(
        username=username,
        zone_hostname=zone_hostname,
        password=password,
        user_id=user_id,
    )


def _create_user(
    zone_hostname: Any,
    onepanel_credentials: Any,
    admin_credentials: Any,
    username: Any,
    options: Any,
    rm_users: Any,
) -> Any:
    password = options.get("password", "password")
    user_conf_details = {"username": username, "password": password, "groups": []}

    try:
        return _create_new_user(
            zone_hostname, onepanel_credentials, username, password, user_conf_details
        )
    except HTTPBadRequest:
        # this error appear when trying to create user with name that already exist
        # (possible remnants from previous tests)
        if rm_users:
            _remove_remnant_user(
                username, zone_hostname, onepanel_credentials, admin_credentials
            )
            return _create_new_user(
                zone_hostname,
                onepanel_credentials,
                username,
                password,
                user_conf_details,
            )
        skip(f'"{username}" user already exist')
    return None


def _configure_user(
    zone_hostname: Any, admin_credentials: Any, user_cred: Any, options: Any
) -> Any:
    full_name = options.get("fullName", user_cred.username.replace("_", " "))
    http_patch(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user"),
        auth=(user_cred.username, user_cred.password),
        data=json.dumps({"fullName": full_name}),
    )
    if options.get("user role") == "onezone admin":
        _add_user_to_zone_cluster(
            zone_hostname,
            admin_credentials,
            user_cred,
            options.get("cluster privileges"),
        )


def _add_user_to_zone_cluster(
    zone_hostname: Any,
    admin_credentials: Any,
    user_credentials: Any,
    cluster_privileges: Any,
) -> Any:
    username, password = user_credentials.username, user_credentials.password
    admin_username = admin_credentials.username
    admin_password = admin_credentials.password

    # get user ID
    response = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user"),
        auth=(username, password),
    ).json()
    user_id = response["userId"]

    # add user to cluster
    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path(f"clusters/onezone/users/{user_id}"),
        auth=(admin_username, admin_password),
    )

    # add privileges
    if cluster_privileges is not None:
        http_patch(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path(f"users/{user_id}/privileges"),
            auth=(admin_username, admin_password),
            data=json.dumps({"grant": cluster_privileges}),
        )
    return User(
        username=username,
        zone_hostname=zone_hostname,
        password=password,
        user_id=user_id,
    )


def _cleanup_users(
    zone_hostname: Any,
    admin_credentials: Any,
    users_db: Any,
    ignore_http_exceptions: Any = False,
) -> Any:
    for user_credentials in users_db.values():
        _rm_user(
            zone_hostname, admin_credentials, user_credentials, ignore_http_exceptions
        )


def _rm_user(
    zone_hostname: Any,
    admin_credentials: Any,
    user_credentials: Any,
    ignore_http_exceptions: Any = False,
) -> Any:
    try:
        _rm_zone_user(zone_hostname, admin_credentials, user_credentials.user_id)
    except HTTPNotFound:
        pass
    except HTTPError as ex:
        if not ignore_http_exceptions:
            raise ex


@repeat_failed(attempts=5)
def _rm_zone_user(zone_hostname: Any, admin_credentials: Any, user_id: Any) -> Any:
    admin_username = admin_credentials.username
    admin_password = admin_credentials.password

    path = get_zone_rest_path("users", user_id)
    http_delete(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=path,
        auth=(admin_username, admin_password),
    )


def _remove_remnant_user(
    username: Any, zone_hostname: Any, onepanel_credentials: Any, admin_credentials: Any
) -> Any:
    users_list = http_get(
        ip=zone_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("zone", "users"),
        auth=(onepanel_credentials.username, onepanel_credentials.password),
    ).json()["ids"]
    for user_id in users_list:
        user_details = http_get(
            ip=zone_hostname,
            port=PANEL_REST_PORT,
            path=get_panel_rest_path("zone", "users", user_id),
            auth=(onepanel_credentials.username, onepanel_credentials.password),
        ).json()
        if user_details["username"] == username:
            _remove_user_spaces(zone_hostname, admin_credentials, user_id)
            _rm_zone_user(zone_hostname, admin_credentials, user_id)


def _remove_user_spaces(
    zone_hostname: Any, admin_credentials: Any, owner_id: Any
) -> Any:
    spaces_list = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("spaces"),
        auth=(admin_credentials.username, admin_credentials.password),
    ).json()["spaces"]
    for space_id in spaces_list:
        owner_list = http_get(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("spaces", space_id, "owners"),
            auth=(admin_credentials.username, admin_credentials.password),
        ).json()["users"]
        if owner_id in owner_list and len(owner_list) == 1:
            http_delete(
                ip=zone_hostname,
                port=OZ_REST_PORT,
                path=get_zone_rest_path("spaces", space_id),
                auth=(admin_credentials.username, admin_credentials.password),
            )
