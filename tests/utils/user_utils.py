"""Module implements utility functions for managing users in onedata via REST.
"""
__author__ = "Jakub Kudzia, Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2016-2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import os
import json
import hashlib

from tests import OZ_REST_PORT, HTTP_PORT
from tests.utils import RPYC_LOGS_DIR, ONECLIENT_LOGS_DIR, ONECLIENT_MOUNT_DIR
from tests.utils.utils import repeat_failed
from tests.utils.onenv_utils import match_pods, get_ip
from tests.utils.rest_utils import (http_post, get_zone_rest_path,
                                    get_token_dispenser_rest_path,
                                    http_get)
from tests.utils.onenv_utils import run_onenv_command
from tests.utils.docker_utils import run_cmd as docker_run_cmd
from tests.utils.client_utils import Client, get_client_conf

RPYC_DEFAULT_PORT = 18812
BAD_TOKEN = 'bad token'
CORRECT_TOKEN = 'token'


class User:
    def __init__(self, zone_hostname, username, password=None, user_id=None):
        self.username = username
        self.password = password
        self._user_id = user_id
        self._token = None
        self.idps = []
        self.keycloak_name = ''
        self.zone_hostname = zone_hostname

        self.last_operation_failed = False
        self.clients = {}
        self._rpyc_connections = {}

    @property
    def token(self):
        if self._token:
            return self._token
        self._token = self._create_token()
        return self._token

    @property
    def user_id(self):
        if self._user_id:
            return self._user_id
        self._user_id = self._retrieve_onedata_id()
        return self._user_id

    def get_rpyc_connection(self, client_host_dict):
        client_host = client_host_dict['pod-name']
        if self._rpyc_connections.get(client_host, None):
            return self._rpyc_connections[client_host]
        self._rpyc_connections[client_host] = self._create_rpyc_connection(client_host_dict)
        return self._rpyc_connections[client_host]

    def mark_last_operation_failed(self):
        self.last_operation_failed = True

    def mark_last_operation_succeeded(self):
        self.last_operation_failed = False

    def mount_client(self, client_host_alias, client_id, hosts, env_desc, token=CORRECT_TOKEN):
        rpyc_connection = self.get_rpyc_connection(hosts[client_host_alias])
        client_conf = get_client_conf(client_id, client_host_alias, env_desc)

        client = Client(rpyc_connection, timeout=client_conf.get('default timeout'))
        self.clients[client_conf.get('id')] = client

        token = self.token if token == CORRECT_TOKEN else token

        rpyc_connection.modules.os.environ['ONECLIENT_ACCESS_TOKEN'] = token
        rpyc_connection.modules.os.environ['ONECLIENT_PROVIDER_HOST'] = \
            hosts[client_conf.get('provider')]['hostname']

        ret = client.mount(client_conf.get('mode'))
        if ret == 0:
            self.mark_last_operation_succeeded()
            return client
        else:
            self.mark_last_operation_failed()
            del self.clients[client_conf.get('id')]
            return None

    @repeat_failed(attempts=5)
    def _create_token(self):
        if 'keycloak' in self.idps:
            token_dispenser_pod = match_pods('token-dispenser')[0]
            token_dispenser_ip = get_ip(token_dispenser_pod)
            response = http_get(ip=token_dispenser_ip, port=HTTP_PORT,
                                path=get_token_dispenser_rest_path('token',
                                                                   self.keycloak_name),
                                auth=(self.username, self.password),
                                default_headers=False, use_ssl=False)
            return response.content
        response = http_post(ip=self.zone_hostname, port=OZ_REST_PORT,
                             path=get_zone_rest_path('user', 'client_tokens'),
                             auth=(self.username, self.password))
        return json.loads(response.content)['token']

    @repeat_failed(attempts=5)
    def _retrieve_onedata_id(self):
        response = http_get(ip=self.zone_hostname, port=OZ_REST_PORT,
                            path=get_zone_rest_path('user'),
                            auth=(self.username, self.password))
        return json.loads(response.content)['userId']

    def _create_rpyc_connection(self, client_host_dict):
        client_host = client_host_dict['pod-name']
        client_host_ip = client_host_dict['ip']
        cointainer_id = client_host_dict['container-id']
        port = gen_port_number(self.username)
        create_required_dirs(client_host)
        cmd = 'python3 `which rpyc_classic.py` --host 0.0.0.0 --port {} --logfile {}'.format(
            port, os.path.join(RPYC_LOGS_DIR, self.username))

        print("\n\nstarting rpyc server for user '{}' on client host '{}'".format(
            self.username, client_host))

        docker_run_cmd(self.username, cointainer_id, cmd, detach=True)
        rpyc_connection = self._connect_to_rpyc(client_host_ip, port)

        # change timeout for rpyc to avoid AsyncResultTimeout in performance tests on bamboo
        rpyc_connection._config['sync_request_timeout'] = 300

        print("rpyc server for user '{}' on client host '{}' successfully started".format(
            self.username, client_host))

        return rpyc_connection

    @repeat_failed(attempts=10, interval=1, exceptions=ConnectionRefusedError)
    def _connect_to_rpyc(self, ip, port):
        import rpyc
        return rpyc.classic.connect(ip, port)


class AdminUser(User):
    def __init__(self, zone_hostname, username, password):
        User.__init__(self, zone_hostname=zone_hostname, username=username, password=password)


def create_required_dirs(pod):
    create_dir(pod, ONECLIENT_MOUNT_DIR)
    create_dir(pod, RPYC_LOGS_DIR)
    create_dir(pod, ONECLIENT_LOGS_DIR)


def create_dir(pod, log_dir_path):
    cmd = [pod, "--", "mkdir", "-p", "-m 777", log_dir_path]
    run_onenv_command("exec", cmd)


def gen_port_number(username):
    return int(hashlib.sha1(username.encode('utf-8')).hexdigest(), 16) % 10000 + RPYC_DEFAULT_PORT
