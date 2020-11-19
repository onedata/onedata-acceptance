""" This module contains utility functions used in tests of upgrade procedure.
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json
import time
import urllib3
import requests

from tests import OZ_REST_PORT
from tests.utils.onenv_utils import run_onenv_command
from tests.utils.user_utils import AdminUser
from tests.utils.rest_utils import get_zone_rest_path, http_get
from tests.utils.http_exceptions import HTTPError
from requests.exceptions import ConnectTimeout
from tests.utils.environment_utils import update_etc_hosts, setup_hosts_cfg, configure_os


from tests.utils.performance_utils import mount_client

ENV_READY_TIMEOUT_SECONDS = 300


class UpgradeTest:
    def __init__(self, setup, check):
        self.setup = setup
        self.check = check


class UpgradeTestsController:
    tests_list = []

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def add_test(self, setup, check):
        self.tests_list.append(UpgradeTest(setup, check))

    def mount_client(self, client_conf):
        return mount_client(client_conf, self.clients, self.hosts,
                            self.request, self.users, self.env_desc, clean_mountpoint=False)

    def run_tests(self):
        admin_user = AdminUser('admin', 'password')
        admin_user.create_token(self.hosts['onezone']['ip'])
        [test.setup(self) for test in self.tests_list]
        for service_name in ['onezone', 'oneprovider', 'oneclient']:
            if service_name in self.test_config['targetVersions'].keys():
                upgrade_service(service_name, admin_user, self.hosts,
                                self.test_config['targetVersions'][service_name])

        setup_hosts_cfg(self.hosts, self.request)
        configure_os(self.scenario_abs_path)
        [test.check(self) for test in self.tests_list]


def upgrade_service(service_name, admin_user, hosts, version):
    for service in hosts.keys():
        if service.startswith(service_name):
            pod_name = hosts[service]['pod-name']
            run_upgrade_command(pod_name, service_name, version)

    if service_name == 'onezone':
        update_etc_hosts()
    check_env_ready(admin_user, hosts)


def run_upgrade_command(pod_name, service, version):
    if version == 'sources':
        image = "docker.onedata.org/{}-dev:{}".format(service, 'develop')
        run_onenv_command('upgrade', [pod_name, '-i', image, '-wp', '--sources-path', '.'])
    else:
        image = "docker.onedata.org/{}-dev:{}".format(service, version)
        run_onenv_command('upgrade', [pod_name, '-i', image])


def check_env_ready(admin_user, hosts):
    zone_hostname = hosts['onezone']['hostname']
    ready = False
    start = time.time()
    while not ready:
        if time.time() - start > ENV_READY_TIMEOUT_SECONDS:
            raise RuntimeError("Environment not ready after upgrade")
        time.sleep(1)
        try:
            providers = get_providers_list(admin_user, zone_hostname)
            ready = all([is_provider_online(admin_user, zone_hostname, p) for p in providers])
        except (HTTPError, ConnectTimeout, ConnectionRefusedError,
                urllib3.exceptions.NewConnectionError, requests.exceptions.ConnectionError):
            # ignore those errors as they are normal when Onezone is starting
            pass


def get_providers_list(admin_user, zone_hostname):
    response = http_get(ip=zone_hostname, port=OZ_REST_PORT,
                        path=get_zone_rest_path('providers'),
                        headers={
                            'X-Auth-Token': admin_user.token,
                            'Content-Type': 'application/json'
                        })
    return json.loads(response.content)['providers']


def is_provider_online(admin_user, zone_hostname, provider):
    response = http_get(ip=zone_hostname, port=OZ_REST_PORT,
                        path=get_zone_rest_path('providers', provider),
                        headers={
                            'X-Auth-Token': admin_user.token,
                            'Content-Type': 'application/json'
                        })
    return json.loads(response.content)['online']
