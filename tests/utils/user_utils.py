"""Module implements utility functions for managing users in onedata via REST.
"""
__author__ = "Jakub Kudzia, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.utils.utils import repeat_failed
from tests.utils.net_utils import (http_post, get_zone_rest_path)

import json


class User:
    def __init__(self, username, password=None, token=None, id=None):
        self.username = username
        self.password = password
        self.id = id
        self.token = token

        self.last_operation_failed = False
        self.clients = {}

    def mark_last_operation_failed(self):
        self.last_operation_failed = True

    def mark_last_operation_succeeded(self):
        self.last_operation_failed = False

    @repeat_failed(attempts=5)
    def create_token(self, oz_ip):
        response = http_post(ip=oz_ip, port=OZ_REST_PORT,
                             path=get_zone_rest_path('user', 'client_tokens'),
                             auth=(self.username, self.password))
        return json.loads(response.content)['token']


class AdminUser(User):
    def __init__(self, username, password):
        User.__init__(self, username, password)
