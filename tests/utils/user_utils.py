"""Module implements utility functions for managing users in onedata via REST.
"""
__author__ = "Jakub Kudzia, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import json

from tests import OZ_REST_PORT, HTTP_PORT
from tests.utils.utils import repeat_failed
from tests.utils.onenv_utils import match_pods, get_ip
from tests.utils.rest_utils import (http_post, get_zone_rest_path,
                                    get_token_dispenser_rest_path,
                                    http_get)


CORRECT_TOKEN = 'token'


class User:
    def __init__(self, username, password=None, token=None, id=None):
        self.username = username
        self.password = password
        self.id = id
        self.token = token
        self.idps = []
        self.keycloak_name = ''

        self.last_operation_failed = False
        self.clients = {}

    def mark_last_operation_failed(self):
        self.last_operation_failed = True

    def mark_last_operation_succeeded(self):
        self.last_operation_failed = False

    @repeat_failed(attempts=5)
    def create_token(self, oz_ip):
        if 'keycloak' in self.idps:
            token_dispenser_pod = match_pods('token-dispenser')[0]
            token_dispenser_ip = get_ip(token_dispenser_pod)
            response = http_get(ip=token_dispenser_ip, port=HTTP_PORT,
                                path=get_token_dispenser_rest_path('token',
                                                                   self.keycloak_name),
                                auth=(self.username, self.password),
                                default_headers=False, use_ssl=False)
            self.token = response.content
        else:
            response = http_post(ip=oz_ip, port=OZ_REST_PORT,
                                 path=get_zone_rest_path('user', 'client_tokens'),
                                 auth=(self.username, self.password))
            self.token = json.loads(response.content)['token']
        return self.token

    @repeat_failed(attempts=5)
    def retrieve_onedata_id(self, oz_ip):
        if not self.id:
            response = http_get(ip=oz_ip, port=OZ_REST_PORT,
                                path=get_zone_rest_path('user'),
                                auth=(self.username, self.password))
            self.id = json.loads(response.content)['userId']
        return self.id


class AdminUser(User):
    def __init__(self, username, password):
        User.__init__(self, username, password)
