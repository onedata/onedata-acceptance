"""Steps for inventories creation using REST API.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json
import pdb

import yaml

from tests import OZ_REST_PORT, PANEL_REST_PORT, OP_REST_PORT
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.rest.shares import get_file_id_by_rest
from tests.utils.bdd_utils import given, parsers
from tests.utils.http_exceptions import (
    HTTPNotFound, HTTPError, HTTPBadRequest, HTTPForbidden)
from tests.utils.rest_utils import (
    http_get, http_post, http_put, get_panel_rest_path, get_zone_rest_path,
    get_provider_rest_path, http_delete)
from tests.utils.utils import repeat_failed


@given(parsers.parse('initial inventories configuartion in "{zone_name}" '
                     'Onezone service:'))
def create_inventory(hosts, users, zone_name):
    owner = users['space-owner-user']
    zone_hostname = hosts[zone_name]['hostname']
    inventory_properties = json.dumps({'name':'inventory1'})
    response = http_post(ip=zone_hostname, port=OZ_REST_PORT,
                         path=get_zone_rest_path('user', 'atm_inventories'),
                         auth=(owner.username, owner.password),
                         data=inventory_properties)