"""Steps for storage creation using REST API.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.meta_steps.onepanel.storages import (
    _remove_storage_in_op_panel_using_rest)
from tests.mixed.onepanel_client.api.storages_api import StoragesApi
from tests.mixed.utils.common import login_to_panel
from tests.utils.bdd_utils import given, parsers
import yaml


@given(parsers.parse('initial "{name}" storage configuration in "{host}" '
                     'Onezone service:\n{config}'))
def create_storage(hosts, host, config, onepanel_credentials, name):
    options = yaml.load(config)

    _remove_storage_in_op_panel_using_rest(name, host, hosts,
                                           onepanel_credentials)
    storage_data = {name: options}
    client = login_to_panel(onepanel_credentials.username,
                            onepanel_credentials.password,
                            hosts[host]['hostname'])

    storages_api = StoragesApi(client)
    storages_api.add_storage(storage_data)
