"""Steps for inventories creation using REST API.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json

import yaml

from tests import OZ_REST_PORT
from tests.utils.bdd_utils import given, parsers
from tests.utils.rest_utils import (http_post, get_zone_rest_path)


@given(parsers.parse('initial inventories configuration in "{zone_name}" '
                     'Onezone service:'))
def create_inventory(hosts, users, zone_name):
    owner = users['space-owner-user']
    zone_hostname = hosts[zone_name]['hostname']
    inventory_properties = json.dumps({'name': 'inventory1'})
    http_post(ip=zone_hostname, port=OZ_REST_PORT,
              path=get_zone_rest_path('user', 'atm_inventories'),
              auth=(owner.username, owner.password),
              data=inventory_properties)
