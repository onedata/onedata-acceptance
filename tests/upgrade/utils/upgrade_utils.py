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
from tests.utils.docker_utils import pull_docker_image_with_retries
from tests.utils.http_exceptions import HTTPError
from tests.utils.onenv_utils import run_onenv_command
from tests.utils.path_utils import get_default_image_for_service
from tests.utils.rest_utils import get_zone_rest_path, http_get
from requests.exceptions import ConnectTimeout
from tests.utils.environment_utils import (update_etc_hosts, setup_hosts_cfg, configure_os,
                                           get_deployment_status)
from tests.utils.client_utils import fusermount, mount_client

ENV_READY_TIMEOUT_SECONDS = 300


class UpgradeTest:
    def __init__(self, name, setup, verify):
        self.__name = name
        self.__setup = setup  # function executed before any upgrade is performed
        self.__verify = verify  # function executed after all upgrades are performed

    def run_setup(self, *args, **kwargs):
        print("\nRunning setup for test \"{}\"\n".format(self.__name))
        self.__setup(*args, **kwargs)
        print("\nSetup for test \"{}\" finished\n".format(self.__name))

    def run_verify(self, *args, **kwargs):
        print("\nRunning verify for test \"{}\"\n".format(self.__name))
        self.__verify(*args, **kwargs)
        print("\nVerify for test \"{}\" finished\n".format(self.__name))


class UpgradeTestsController:
    def __init__(self, **kwargs):
        self.__tests_list = []
        self.__dict__.update(kwargs)

    def add_test(self, name, setup, verify):
        self.__tests_list.append(UpgradeTest(name, setup, verify))

    def mount_client(self, client_conf):
        return mount_client(client_conf, self.clients, self.hosts,
                            self.request, self.users, self.env_desc, clean_mountpoint=False)

    def run_tests(self):
        admin_user = self.users['admin']
        [self.__run_setup(test) for test in self.__tests_list]
        for service_name in ['onezone', 'oneprovider', 'oneclient']:
            if service_name in self.test_config['targetVersions'].keys():
                upgrade_service(service_name, admin_user, self.hosts,
                                self.test_config['targetVersions'][service_name])

        setup_hosts_cfg(self.hosts, self.request)
        configure_os(self.scenario_abs_path, get_deployment_status())
        [self.__run_verify(test) for test in self.__tests_list]
        self.__unmount_clients()

    def __run_setup(self, test):
        test.run_setup(self)
        self.__unmount_clients()

    def __run_verify(self, test):
        test.run_verify(self)
        self.__unmount_clients()

    def __unmount_clients(self):
        for client in self.clients.keys():
            fusermount(self.clients[client], self.clients[client].mount_path,
                       unmount=True, lazy=True)
        self.clients.clear()


def upgrade_service(service_name, admin_user, hosts, version):
    for service in hosts.keys():
        if service.startswith(service_name):
            pod_name = hosts[service]['pod-name']
            run_upgrade_command(pod_name, service_name, version)

    if service_name == 'onezone':
        # etc hosts update needed so it is possible to connect
        # to Onezone during env ready verification
        update_etc_hosts()
    verify_env_ready(admin_user, hosts)


def run_upgrade_command(pod_name, service, version):
    cmd = [pod_name]
    if isinstance(version, str):
        cmd.extend(prepare_image_upgrade_command(service, version))
        run_onenv_command('upgrade', cmd)
    else:
        cmd.extend(prepare_sources_upgrade_command(service, version))
        run_onenv_command('upgrade', cmd)


def prepare_image_upgrade_command(service, version):
    if version == 'default':
        image = get_default_image_for_service(service)
    else:
        image = "docker.onedata.org/{}-dev:{}".format(service, version)
    pull_docker_image_with_retries(image)
    return ['-i', image]


def prepare_sources_upgrade_command(service, version):
    image = "docker.onedata.org/{}-dev:{}".format(service, version['sources']['baseImage'])
    pull_docker_image_with_retries(image)
    components = []
    for component in version['sources']['components']:
        components.append('--{}'.format(component))
    cmd = ['-i', image, '--sources-path', '.']
    cmd.extend(components)
    return cmd


def verify_env_ready(admin_user, hosts):
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
