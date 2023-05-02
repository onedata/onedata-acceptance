"""This module provides utility functions for test environment management"""

__author__ = "Jakub Kudzia, Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2016-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import re
import yaml
import json
import time
import urllib3
import requests
import subprocess as sp
from typing import Dict, List
from requests.exceptions import ConnectTimeout

from tests import PANEL_REST_PORT, OZ_REST_PORT
from tests.utils.http_exceptions import HTTPError
from tests.utils.onenv_utils import (init_helm, client_alias_to_pod_mapping,
                                     service_name_to_alias_mapping,
                                     OnenvError, run_onenv_command, run_command)
from tests.utils.luma_utils import (get_local_feed_luma_storages, get_all_spaces_details,
                                    add_user_luma_mapping, add_spaces_luma_mapping, gen_uid,
                                    gen_gid)
from tests.utils.user_utils import User, AdminUser
from tests.utils.rest_utils import get_zone_rest_path, http_get

START_ENV_MAX_RETRIES = 3
ONE_ENV_CONTAINER_NAME = 'one-env'
ENV_READY_TIMEOUT_SECONDS = 300


def start_environment(scenario_path, request, hosts, patch_path, users, test_config):
    attempts = 0
    local = request.config.getoption('--local')
    up_args = parse_up_args(request, test_config)
    up_args.extend(['{}'.format(scenario_path)])
    wait_args = parse_wait_args(request)
    patch_args = parse_patch_args(request, patch_path) if patch_path else []

    dep_status = {}
    started = False
    while not started and attempts < START_ENV_MAX_RETRIES:
        try:
            maybe_setup_helm()
            run_onenv_command('init', cwd=None, onenv_path='one_env/onenv')
            run_onenv_command('up', up_args)
            run_onenv_command('wait', wait_args)
            dep_status = get_deployment_status()
            check_deployment(dep_status)

            if not local:
                update_etc_hosts()
            setup_hosts_cfg(hosts, request)
            zone_hostname = hosts['onezone']['hostname']
            users['admin'] = AdminUser(zone_hostname, 'admin', 'password')

            if patch_path and not request.config.getoption('--no-clean'):
                run_onenv_command('patch', patch_args)
                wait_args = parse_wait_args(request)
                run_onenv_command('wait', wait_args)
                dep_status = get_deployment_status()
                check_deployment(dep_status)

            if patch_path:
                with open(patch_path, 'r') as patch_file:
                    patch_cfg = yaml.load(patch_file)
                setup_users(patch_cfg, users, zone_hostname)
                add_luma_mappings(patch_cfg, users, hosts)

            started = True

        except OnenvError as e:
            attempts += 1
            if attempts >= START_ENV_MAX_RETRIES:
                return e
            else:
                clean_env()

    configure_os(scenario_path, dep_status)
    return 'ok'


def maybe_setup_helm():
    is_helm_v2 = False
    try:
        helm_version_proc = sp.run(
            ['helm', 'version'],
            stdout=sp.PIPE
        )
        version_string = str(helm_version_proc.stdout)
        version2_match = re.search(
            r'Server:.*v2',
            version_string
        )
        if version2_match:
            is_helm_v2 = True
    except FileNotFoundError:
        is_helm_v2 = False

    if is_helm_v2:
        print('Helm version 2.x is used - invoking init helm...')
        init_helm()


def update_etc_hosts():
    """
    The 'onenv hosts' command updates entries in /etc/hosts file present in
    one-env container. This file is a docker volume mounted from host machine.
    As some tests modifies entries in /etc/hosts file, it is undesired to make
    this volume available also in test-runner container. Thus this function
    firstly updates /etc/hosts entries using the 'onenv hosts' command and then
    copies modified /etc/hosts from one-env container to test-runner container.
    """

    run_onenv_command('hosts')
    etc_hosts_path = '/etc/hosts'
    tmp_hosts_path = '/tmp/hosts'
    sp.call(['docker', 'cp', '{}:{}'.format(ONE_ENV_CONTAINER_NAME,
                                            etc_hosts_path),
             tmp_hosts_path])
    sp.call(['sudo', 'cp', tmp_hosts_path, etc_hosts_path])


def configure_os(scenario_path: str, dep_status) -> None:
    """
    Function responsible for creating system users and groups in containers for
    Onezone / Oneprovider / Oneclient.

    os_configs parameter corresponds to 'os-config' section in environment
    configuration file that was generated by merging command-line arguments
    and config file passed by user to onenv_up script.
    """
    check_deployment(dep_status)
    pods_cfg = dep_status.get('pods')

    with open(scenario_path, 'r') as env_file:
        env_cfg = yaml.load(env_file, yaml.Loader)
    os_configs = env_cfg.get('os-config')
    if not os_configs:
        return

    for pod_name, pod_cfg in pods_cfg.items():
        service_type = pod_cfg['service-type']
        if service_type in ['onezone', 'oneprovider']:
            alias = service_name_to_alias_mapping(pod_name)
            os_config = os_configs.get('services').get(alias)
            if os_config:
                create_users_in_pod(pod_name, os_config.get('users'))
                create_groups_in_pod(pod_name, os_config.get('groups'))
        if service_type == 'oneclient':
            os_config = os_configs.get('services').get("oneclient")
            if os_config:
                create_users_in_pod(pod_name, os_config.get('users'))
                create_groups_in_pod(pod_name, os_config.get('groups'))


def setup_hosts_cfg(hosts, request):
    pods_cfg = get_pods_config()
    for pod_name, pod_cfg in pods_cfg.items():
        service_type = pod_cfg['service-type']
        if service_type in ['onezone', 'oneprovider']:
            parse_oz_op_cfg(pod_name, pod_cfg, service_type,
                            request.config.getoption('--add-test-domain'),
                            hosts)

        elif service_type == 'oneclient':
            parse_client_cfg(pod_name, pod_cfg, hosts)
        elif service_type == 'elasticsearch':
            parse_elasticsearch_cfg(pod_cfg, hosts)


def setup_users(patch_cfg, users, zone_hostname):
    for user_cfg in patch_cfg.get('users'):
        user_name = user_cfg.get('name')
        password = user_cfg.get('password')
        new_user = users[user_name] = User(
            username=user_name, zone_hostname=zone_hostname, password=password)
        idps = user_cfg.get('idps', {})
        for idp_type in idps:
            new_user.idps.append(idp_type)
            if idp_type == 'keycloak':
                global_cfg = patch_cfg.get('global')
                keycloak_suffix = (global_cfg
                                   .get('keycloakInstance', {})
                                   .get('idpName'))
                new_user.keycloak_name = ('keycloak-{}'.format(keycloak_suffix))


def add_luma_mappings(patch_cfg, users, hosts):
    admin_user = users['admin']

    spaces = get_all_spaces_details(admin_user, hosts)
    local_feed_luma_storages = get_local_feed_luma_storages(admin_user, hosts)

    for user_cfg in patch_cfg.get('users'):
        user_name = user_cfg.get('name')
        new_user = users[user_name]
        add_user_luma_mapping(admin_user, new_user, local_feed_luma_storages)

    add_spaces_luma_mapping(admin_user, local_feed_luma_storages, spaces)


def get_deployment_status():
    return yaml.load(run_onenv_command('status'), yaml.Loader)


def check_deployment(deployment_status):
    env_ready = deployment_status.get('ready')

    if not env_ready:
        raise OnenvError('Environment error: timeout while waiting for '
                         'deployment to be ready.')


def parse_patch_args(request, patch_path):
    patch_args = []
    local_charts_path = request.config.getoption('--local-charts-path')

    if local_charts_path:
        patch_args.extend(['-lcp', local_charts_path])

    patch_args.extend(['--patch', patch_path])
    return patch_args


def parse_wait_args(request):
    wait_args = []

    timeout = request.config.getoption('--timeout')
    if timeout:
        wait_args.extend(['--timeout', timeout])
    return wait_args


def parse_up_args(request, test_config):
    up_args = []

    oz_image = request.config.getoption('--oz-image')
    op_image = request.config.getoption('--op-image')
    oc_image = request.config.getoption('--oc-image')
    rest_cli_image = request.config.getoption('--rest-cli-image')
    openfaas_pod_status_monitor_image = request.config.getoption('--openfaas-pod-status-monitor-image')
    sources = request.config.getoption('--sources')
    timeout = request.config.getoption('--timeout')
    local_charts_path = request.config.getoption('--local-charts-path')

    gui_pkg_verification = request.config.getoption('--gui-pkg-verification')

    if oz_image:
        up_args.extend(['-zi', oz_image])
    if op_image:
        up_args.extend(['-pi', op_image])
    if oc_image:
        up_args.extend(['-ci', oc_image])
    if rest_cli_image:
        up_args.extend(['-ri', rest_cli_image])
    if openfaas_pod_status_monitor_image:
        up_args.extend(['-mi', openfaas_pod_status_monitor_image])
    if sources:
        up_args.append('-s')
    if local_charts_path:
        up_args.extend(['-lcp', local_charts_path])
    if timeout:
        up_args.extend(['--timeout', timeout])
    if gui_pkg_verification:
        up_args.append('--gui-pkg-verification')

    if test_config:
        if not oz_image:
            oz_version = test_config['initialVersions']['onezone']
            up_args.extend(['-zi', 'docker.onedata.org/onezone-dev:{}'.format(oz_version)])
        if not op_image:
            op_version = test_config['initialVersions']['oneprovider']
            up_args.extend(['-pi', 'docker.onedata.org/oneprovider-dev:{}'.format(op_version)])
        if not oc_image:
            oc_version = test_config['initialVersions']['oneclient']
            up_args.extend(['-ci', 'docker.onedata.org/oneclient-dev:{}'.format(oc_version)])

    return up_args


def create_users_in_pod(pod_name: str, users: List[str]) -> None:
    """Creates system users on pod specified by 'pod_name'."""

    def _user_exists(user: str, pod_name: str) -> bool:
        cmd = [pod_name, '--', 'id', '-u', user]
        ret = run_kubectl_command('exec', cmd, fail_with_error=False, return_output=False)
        return ret == 0

    for username in users:
        if _user_exists(username, pod_name):
            print('Skipping creation of user {} - user already exists in {}.'
                  .format(username, pod_name))
        else:
            uid = str(gen_uid(username))
            command = [pod_name, '--', 'adduser', '--disabled-password', '--gecos', '""',
                       '--uid', uid, username]
            run_kubectl_command('exec', command)


def create_groups_in_pod(pod_name: str, groups: Dict[str, List[str]]) -> None:
    """Creates system groups on pod specified by 'pod_name'."""

    def _group_exists(group: str, pod_name: str) -> bool:
        cmd = [pod_name, '--', 'grep', '-q', group, '/etc/group']
        ret = run_kubectl_command('exec', cmd, fail_with_error=False, return_output=False)
        return ret == 0

    for group, users in groups.items():
        if _group_exists(group, pod_name):
            print('Skipping creation of group {} - group already exists in {}.'
                  .format(group, pod_name))
        else:
            gid = str(gen_gid(group))
            command = [pod_name, '--', 'groupadd', '-g', gid, group]
            run_kubectl_command('exec', command)
            for user in users:
                command = [pod_name, '--', 'usermod', '-a', '-G', group, user]
                run_kubectl_command('exec', command)


def get_pods_config():
    pods_json = get_pods_with_kubectl()['items']
    pods = {}
    for pod in pods_json:
        pod_data = pod['metadata']
        pod_title = pod_data['name']
        pod_name = pod_data['labels'].get('app', None)
        pod_service_type = pod_data['labels'].get('component', None)
        pod_service_name = pod_data['labels'].get('chart', None)
        pod_namespace = pod_data['namespace']
        pod_ip = pod['status'].get('podIP', None)
        pod_container_id = pod['status']['containerStatuses'][0].get('containerID', None)
        if pod_container_id:
            pod_container_id = pod_container_id.replace('docker://', '')

        pods[pod_title] = {'name': pod_name, 'ip': pod_ip,
                           'container-id': pod_container_id}

        pod_domain = f'{pod_name}.{pod_namespace}.svc.cluster.local'
        pod_hostname = f'{pod_title}.{pod_domain}'

        pods[pod_title]['domain'] = pod_domain
        pods[pod_title]['hostname'] = pod_hostname

        pods[pod_title]['service-type'] = (
            pod_service_type if pod_service_type else pod_service_name)

    return pods


def get_pods_with_kubectl():
    cmd = ['pods', '-o', 'json']
    output = run_kubectl_command('get', cmd, verbose=False)
    return json.loads(output)


def parse_oz_op_cfg(pod_name, pod_cfg, service_type, add_test_domain, hosts):
    alias = service_name_to_alias_mapping(pod_name)
    name, hostname, ip, container_id = (pod_cfg.get('name'),
                                        pod_cfg.get('domain'),
                                        pod_cfg.get('ip'),
                                        pod_cfg.get('container-id'))

    hosts[alias] = {'pod-name': pod_name,
                    'service-type': service_type,
                    'name': name,
                    'hostname': hostname,
                    'ip': ip,
                    'container-id': container_id,
                    'panel':
                        {'hostname': '{}:{}'.format(hostname,
                                                    PANEL_REST_PORT)}
                    }
    if add_test_domain and service_type == 'oneprovider':
        add_etc_hosts_entries(ip, '{}.test'.format(hostname))


def parse_client_cfg(pod_name, pod_cfg, hosts):
    ip, container_id, provider_host = (pod_cfg.get('ip'),
                                       pod_cfg.get('container-id'),
                                       pod_cfg.get('provider-host'))

    client_alias = client_alias_to_pod_mapping().get(pod_name)
    hosts[client_alias] = {'ip': ip,
                           'container-id': container_id,
                           'pod-name': pod_name,
                           'provider-host': provider_host}


def parse_elasticsearch_cfg(pod_cfg, hosts):
    ip, container_id = (pod_cfg.get('ip'),
                        pod_cfg.get('container-id'))
    hosts['elasticsearch'] = {'ip': ip,
                              'container-id': container_id}


def add_etc_hosts_entries(service_ip, service_host):
    sp.call('sudo bash -c "echo {} {} >> /etc/hosts"'.format(
        service_ip, service_host), shell=True)


def run_kubectl_command(command, args=None, fail_with_error=True, return_output=True, verbose=True):
    cmd = ['kubectl', command]
    if args:
        cmd.extend(args)
    return run_command(cmd, fail_with_error=fail_with_error, return_output=return_output, 
                       verbose=verbose)


def clean_env():
    run_onenv_command('clean', ['-a', '-s', '-d', '-v'])


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
