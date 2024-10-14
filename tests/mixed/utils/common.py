"""Utils and fixtures to facilitate common operations using REST API."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


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
from tests.mixed.onepanel_client.configuration import (
    Configuration as Conf_panel,
)
from tests.mixed.oneprovider_client import ApiClient as ApiClient_provider
from tests.mixed.oneprovider_client.configuration import (
    Configuration as Conf_provider,
)
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


def login_to_cdmi(
    username, users, host, access_token=None, identity_token=None
):

    configuration = Conf_CDMI()
    setup_basic_configuration(
        configuration, host, OZ_REST_PORT, CDMI_REST_PATH_PREFIX
    )

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
