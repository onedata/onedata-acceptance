"""Steps for storage creation using REST API.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json
import yaml

from tests import PANEL_REST_PORT
from tests.gui.meta_steps.onepanel.storages import (
    _remove_storage_in_op_panel_using_rest)
from tests.utils.bdd_utils import given, parsers
from tests.utils.rest_utils import http_post, get_panel_rest_path


@given(parsers.parse('initial "{name}" storage configuration in "{host}" '
                     'Onezone service:\n{config}'))
def create_storage(hosts, host, config, onepanel_credentials, name):
    options = yaml.load(config)

    _remove_storage_in_op_panel_using_rest(name, host, hosts,
                                           onepanel_credentials)
    storage_data = {name: options}
    http_post(ip=hosts[host]['hostname'], port=PANEL_REST_PORT,
              path=get_panel_rest_path('provider', 'storages'),
              auth=(onepanel_credentials.username,
                    onepanel_credentials.password),
              data=json.dumps(storage_data))
