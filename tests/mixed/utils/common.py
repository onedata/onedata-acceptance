"""Utils and fixtures to facilitate common operations using REST API."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import subprocess as sp

import yaml
from tests import (
    CDMI_REST_PATH_PREFIX,
    OZ_REST_PATH_PREFIX,
    OZ_REST_PORT,
    PANEL_REST_PATH_PREFIX,
    PANEL_REST_PORT,
    PROVIDER_REST_PATH_PREFIX,
)
from tests.mixed.cdmi_client import ApiClient as ApiClient_CDMI
from tests.mixed.cdmi_client.configuration import Configuration as Conf_CDMI
from tests.mixed.onepanel_client import ApiClient as ApiClient_panel
from tests.mixed.onepanel_client.configuration import Configuration as Conf_panel
from tests.mixed.oneprovider_client import ApiClient as ApiClient_provider
from tests.mixed.oneprovider_client.configuration import Configuration as Conf_provider
from tests.mixed.onezone_client import ApiClient as ApiClient_OZ
from tests.mixed.onezone_client.configuration import Configuration as Conf_OZ
from tests.utils.bdd_utils import parsers, wt


class NoSuchClientException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def setup_basic_configuration(
    configuration, host, port, path_prefix, username="", password=""
):
    configuration.username = username
    configuration.password = password
    configuration.verify_ssl = False
    configuration.safe_chars_for_path_param = "/"
    configuration.host = f"https://{host}:{port}{path_prefix}"


def login_to_oz(username, password, host):

    configuration = Conf_OZ()
    setup_basic_configuration(
        configuration,
        host,
        OZ_REST_PORT,
        OZ_REST_PATH_PREFIX,
        username,
        password,
    )

    return ApiClient_OZ(configuration=configuration)


def login_to_panel(username, password, host):

    configuration = Conf_panel()
    setup_basic_configuration(
        configuration,
        host,
        PANEL_REST_PORT,
        PANEL_REST_PATH_PREFIX,
        username,
        password,
    )

    return ApiClient_panel(configuration=configuration)


def login_to_cdmi(username, users, host, access_token=None, identity_token=None):

    configuration = Conf_CDMI()
    setup_basic_configuration(configuration, host, OZ_REST_PORT, CDMI_REST_PATH_PREFIX)

    header_value = access_token if access_token else users[username].token

    client = ApiClient_CDMI(
        configuration=configuration,
        header_name="X-Auth-Token",
        header_value=header_value,
    )

    if identity_token:
        client.set_default_header("x-onedata-consumer-token", identity_token)
    return client


def login_to_provider(username, users, host, access_token=None):

    header_value = access_token if access_token else users[username].token

    configuration = Conf_provider()
    setup_basic_configuration(
        configuration, host, OZ_REST_PORT, PROVIDER_REST_PATH_PREFIX
    )

    return ApiClient_provider(
        configuration=configuration,
        header_name="X-Auth-Token",
        header_value=header_value,
    )


@wt(parsers.parse("{sender} sends token to {receiver}"))
def send_copied_token_to_other_user(sender, receiver, tmp_memory):
    tmp_memory[receiver]["mailbox"]["token"] = tmp_memory[sender]["token"]


@wt(parsers.parse("user of {browser_id} executes copied command"))
def execute_copied_command_rest(
    browser_id, displays, clipboard, tmp_memory, selenium, config=None
):
    cmd = clipboard.paste(display=displays[browser_id])
    cmd = replace_vars_in_cmd_if_exists(cmd, tmp_memory, selenium, config=config)
    cmd += " -k"  # ignore ssl certs
    output = sp.run(
        cmd, capture_output=True, text=True, shell=True, check=True, timeout=60
    )
    tmp_memory["output"] = output.stdout


@wt(
    parsers.parse(
        'user of {browser_id} executes copied command with env variable "{var}" with'
        ' value of "{val}"'
    )
)
def execute_copied_command_rest_with_env_vars(
    browser_id, displays, clipboard, tmp_memory, selenium, var, val
):
    execute_copied_command_rest(
        browser_id, displays, clipboard, tmp_memory, selenium, {var: val}
    )


def replace_vars_in_cmd_if_exists(cmd, tmp_memory, selenium, config=None):
    if config is None:  # if config is None set default values
        config = {"USER_ID": "user1", "GROUP_ID": "group1"}
    request = selenium["request"]
    users = request.getfixturevalue("users")
    groups = request.getfixturevalue("groups")
    new_cmd = cmd
    if "$TOKEN" in cmd:
        new_cmd = new_cmd.replace("$TOKEN", tmp_memory["copied_token"])
    if "$USER_ID" in cmd:
        new_cmd = new_cmd.replace("$USER_ID", users[config["USER_ID"]].user_id)
    if "$GROUP_ID" in cmd:
        new_cmd = new_cmd.replace("$GROUP_ID", groups[config["GROUP_ID"]])
    return new_cmd


def try_to_resolve_items(val: str, request):
    users = request.getfixturevalue("users")
    groups = request.getfixturevalue("groups")
    shares = request.getfixturevalue("shares")
    for _ in range(5):  # max 5 resolve_id per string, can be increased if needed
        if "$(resolve_user_id" in val:
            user = val.split("$(resolve_user_id ")[1]
            user = user.split(")")[0]
            val = val.replace(f"$(resolve_user_id {user})", users[user].user_id)
        if "$(resolve_group_id" in val:
            group = val.split("$(resolve_group_id ")[1]
            group = group.split(")")[0]
            val = val.replace(f"$(resolve_group_id {group})", groups[group])
        if "$(resolve_share_id" in val:
            share = val.split("$(resolve_share_id ")[1]
            share = share.split(")")[0]
            val = val.replace(f"$(resolve_share_id {share})", shares[share])
    return val


@wt(parsers.parse("{user} sees that output of executed command contains:\n{config}"))
def assert_command_output_contains(request, tmp_memory, config):
    output = tmp_memory["output"]
    output = yaml.load(output, yaml.Loader)
    expected = yaml.load(config, yaml.Loader)
    for k, v in expected.items():
        if isinstance(v, list):
            assert len(v) == len(output[k]), (
                "expected output command to have "
                f"{len(v)} elems but got {len(output[k])}"
            )
            for el in v:
                el = try_to_resolve_items(str(el), request)
                assert el in output[k], f"item {el} not in output command {output[k]}"
        else:
            val = try_to_resolve_items(str(v), request)
            err_msg = (
                f"expected command output to contain {k}: {val}, but got {output[k]}"
            )
            assert str(output[k]) == str(val), err_msg


@wt(
    parsers.parse(
        '{user} sees that output of executed command is equal to: "{expected_output}"'
    )
)
def assert_command_output_equals(tmp_memory, expected_output):
    output = tmp_memory["output"]
    err_msg = f"expected command output to be {expected_output}, but got {output}"
    assert expected_output == output, err_msg
