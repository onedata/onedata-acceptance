"""Utils and fixtures to facilitate common operations using REST API."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
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
from tests.mixed.utils.privileges import (
    space_manager_privileges,
    space_member_privileges,
    space_owner_privileges,
)
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


def construct_curl_get_cmd(link: str):
    return f"curl -X GET {link}"


@wt(parsers.parse("{sender} sends token to {receiver}"))
def send_copied_token_to_other_user(sender, receiver, tmp_memory):
    tmp_memory[receiver]["mailbox"]["token"] = tmp_memory[sender]["token"]


@wt(parsers.parse("user of {browser_id} executes copied command"))
def execute_copied_curl_command(
    browser_id,
    displays,
    clipboard,
    tmp_memory,
    config=None,  # config will always be None there
):
    _execute_curl_command(
        clipboard.paste(display=displays[browser_id]),
        tmp_memory,
        config,
    )


def _execute_curl_command(
    command: str,
    tmp_memory,
    config,
    flags: list[str] | None = None,
    file_out: str | None = None,
):
    cmd = (
        replace_vars_in_cmd_if_exist(command, config=config)
        + " -k"  # ignore ssl certs and get http status code
        + ' -w "http status code:%{http_code}"'
        + (f" -{' -'.join(flags)}" if flags else "")
        + (f" -o {file_out}" if file_out else "")
    )

    output = sp.run(
        cmd, capture_output=True, text=True, shell=True, check=True, timeout=60
    )

    output_message, http_status_code = output.stdout.split("http status code:")
    tmp_memory["http status code"] = http_status_code
    tmp_memory["output"] = output_message
    tmp_memory["stderr"] = output.stderr


@wt(
    parsers.parse(
        "user of {browser_id} executes copied command with environment"
        " variables:\n{config}"
    )
)
def execute_copied_curl_command_with_env_vars(
    browser_id, displays, clipboard, tmp_memory, selenium, config
):
    """
    config is in following format:
    ENV_VAR1: VAL1 or $(resolve_... VAL1)
    ...
    """
    config = yaml.load(config, yaml.Loader)
    config = {
        k: try_to_resolve_items(v, selenium["request"]) for k, v in config.items()
    }
    execute_copied_curl_command(
        browser_id, displays, clipboard, tmp_memory, config=config
    )


def replace_vars_in_cmd_if_exist(cmd, config=None):
    if config is None:
        return cmd
    new_cmd = cmd
    for k, v in config.items():
        new_cmd = new_cmd.replace(f"${k}", v)
    return new_cmd


def try_to_resolve_items(val: str, request):
    if not isinstance(val, str):
        val = str(val)
    users = request.getfixturevalue("users")
    groups = request.getfixturevalue("groups")
    shares = request.getfixturevalue("shares")
    tmp_memory = request.getfixturevalue("tmp_memory")

    # dict to store mapping resolve type into resolve function
    s = {
        "resolve_user_id": lambda x: users[x].user_id,
        "resolve_group_id": lambda x: groups[x],
        "resolve_share_id": lambda x: shares[x],
        "resolve_token": lambda _: tmp_memory["copied_token"],
        "space_owner_privileges": lambda _: space_owner_privileges,
        "space_manager_privileges": lambda _: space_manager_privileges,
        "space_member_privileges": lambda _: space_member_privileges,
        "resolve_compose_json": lambda x: json.dumps(
            {x.split(",")[0]: x.split(",")[1]}
        ),
        "resolve_compose_list": lambda x: json.dumps([x]),
    }

    def _resolve(text):
        new_text = text
        for k, v in s.items():
            if k in text:
                if "resolve" not in k:
                    new_text = new_text.replace(f"<{k}>", str(v(k)))
                else:
                    item = new_text.split(f"$({k} ")[1].split(")")[0]
                    new_text = new_text.replace(f"$({k} {item})", v(item))
        return new_text

    prev_val = None
    while prev_val != val:
        prev_val = val
        val = _resolve(val)
    return val


@wt(
    parsers.parse(
        "user of {browser_id} sees that output of executed command contains:\n{config}"
    )
)
def assert_command_output_contains(request, tmp_memory, config):
    output = tmp_memory["output"]
    output = yaml.load(output, yaml.Loader)
    expected = yaml.load(config, yaml.Loader)
    for k, v in expected.items():
        if isinstance(v, list):
            assert len(v) == len(output[k]), (
                f"expected {len(v)} elements from REST command in output,"
                f" but got {len(output[k])}."
            )
            for el in v:
                el = try_to_resolve_items(str(el), request)
                assert el in output[k], f"item {el} not in output command {output[k]}"
        else:
            val = try_to_resolve_items(str(v), request)
            err_msg = (
                f"expected {k}: {val} from REST command in output, but got {output[k]}"
            )
            assert str(output[k]) == str(val), err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees that output of executed command is equal to:"
        ' "{expected_output}"'
    )
)
def assert_command_output_equals(tmp_memory, expected_output):
    output = tmp_memory["output"]
    err_msg = f"expected command output to be {expected_output}, but got {output}"
    assert expected_output == output, err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees that executed curl command returned successful HTTP"
        " code"
    )
)
def assert_curl_command_successful_http_code(tmp_memory):
    http_status_code = tmp_memory["http status code"]
    command_output = tmp_memory["output"]
    command_stderr = tmp_memory["stderr"]
    err_msg = (
        f"Expected 2xx http status code but got: {http_status_code}\n"
        "--- Captured curl stdout ---\n"
        f"{command_output}\n"
        "--- Captured curl stderr ---\n"
        f"{command_stderr}"
    )
    assert http_status_code.startswith("2"), err_msg


@wt(
    parsers.parse(
        "user of {browser_id} uses curl to get content from copied link and"
        ' forwards output to "{file_out}"'
    )
)
def download_using_curl_with_forward(
    browser_id,
    tmp_memory,
    clipboard,
    displays,
    tmpdir,
    browsers_to_users,
    file_out,
):
    download_link = clipboard.paste(display=displays[browser_id])
    file_out = (
        tmpdir.join(browsers_to_users[browser_id], "download", file_out)
        if file_out
        else None
    )

    _execute_curl_command(
        construct_curl_get_cmd(download_link),
        tmp_memory,
        None,
        flags=["L"],
        file_out=file_out,
    )


@wt(parsers.parse("user of {browser_id} uses curl to get content from copied link"))
def download_using_curl(
    browser_id, tmp_memory, clipboard, displays, tmpdir, browsers_to_users
):
    download_using_curl_with_forward(
        browser_id,
        tmp_memory,
        clipboard,
        displays,
        tmpdir,
        browsers_to_users,
        file_out=None,
    )
