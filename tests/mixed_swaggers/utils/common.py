"""Utils and fixtures to facilitate common operations using REST API.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests import (OZ_REST_PATH_PREFIX, OZ_REST_PORT, PANEL_REST_PORT,
                   PANEL_REST_PATH_PREFIX, PROVIDER_REST_PATH_PREFIX,
                   CDMI_REST_PATH_PREFIX)


class NoSuchClientException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def login_to_oz(username, password, host):
    from tests.mixed_swaggers.onezone_client.configuration import (Configuration
                                                                   as Conf_OZ)
    from tests.mixed_swaggers.onezone_client import (ApiClient as ApiClient_OZ)

    configuration = Conf_OZ()
    configuration.username = username
    configuration.password = password
    configuration.verify_ssl = False
    configuration.host = 'https://{}:{}{}'.format(host, OZ_REST_PORT,
                                                  OZ_REST_PATH_PREFIX)

    return ApiClient_OZ(configuration=configuration)


def login_to_panel(username, password, host):
    from tests.mixed_swaggers.onepanel_client.configuration import \
                                                (Configuration as Conf_panel)
    from tests.mixed_swaggers.onepanel_client import (ApiClient 
                                                      as ApiClient_panel)
    Conf_panel().verify_ssl = False
    Conf_panel().username = username
    Conf_panel().password = password

    client = ApiClient_panel(
        host='https://{}:{}{}'.format(host,
                                      PANEL_REST_PORT,
                                      PANEL_REST_PATH_PREFIX))
    return client


def login_to_cdmi(username, users, host):
    from tests.mixed_swaggers.cdmi_client.configuration import (Configuration
                                                                as Conf_CDMI)
    from tests.mixed_swaggers.cdmi_client import (ApiClient as ApiClient_CDMI)
    Conf_CDMI().verify_ssl = False

    client = ApiClient_CDMI(
        host='https://{}:{}{}'.format(host,
                                      OZ_REST_PORT,
                                      CDMI_REST_PATH_PREFIX),
        header_name = 'X-Auth-Token', header_value = users[username].token)
    return client


def login_to_provider(username, users, host):
    from tests.mixed_swaggers.onepprovider_client.configuration import \
                                                Configuration as Conf_provider
    from tests.mixed_swaggers.onepprovider_client import (ApiClient
                                                          as ApiClient_provider)
    Conf_provider().verify_ssl = False

    client = ApiClient_provider(
        host = 'https://{}:{}{}'.format(host,
                                      OZ_REST_PORT,
                                      PROVIDER_REST_PATH_PREFIX), 
        header_name = 'X-Auth-Token', header_value = users[username].token)
    return client


def send_copied_item_to_other_users_rest(sender, receiver, item_type,
                                         tmp_memory):
    tmp_memory[receiver]['mailbox'][item_type.lower()] = \
        tmp_memory[sender][item_type]
