"""This file contains utility functions for operation using onenv tool."""


__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import os
import yaml
import re
import sys
import subprocess as sp
import urllib3
from kubernetes import client, config


# TODO: After resolving VFS-4820 all this function can be imported from
# one-env submodule

def client_alias_to_pod_mapping():
    prov_clients_mapping = {}
    client_alias_mapping = {}
    pods_list = list_pods()
    clients_pods = [pod for pod in pods_list
                    if get_service_type(pod) == 'oneclient']
    for client_pod in clients_pods:
        provider = get_client_provider_host(client_pod)
        provider_alias = service_name_to_alias_mapping(provider)
        if provider_alias in prov_clients_mapping:
            prov_clients_mapping[provider_alias].append(client_pod)
        else:
            prov_clients_mapping[provider_alias] = [client_pod]

    i = 1
    for prov_alias in sorted(list(prov_clients_mapping.keys())):
        client_pods = sorted(prov_clients_mapping.get(prov_alias),
                             key=get_name)
        for pod in client_pods:
            key = 'oneclient-{}'.format(i)
            client_alias_mapping[key] = get_name(pod)
            client_alias_mapping[get_name(pod)] = key
            i += 1
    return client_alias_mapping


def service_name_to_alias_mapping(name):
    return [val for key, val in
            {'oneprovider-krakow': 'oneprovider-1',
             'oneprovider-paris': 'oneprovider-2',
             'oneprovider-lisbon': 'oneprovider-3',
             'onezone': 'onezone'}.items() if key.lower() in name][0]


def get_service_type(pod):
    # returns SERVICE_ONEZONE | SERVICE_ONEPROVIDER
    return pod.metadata.labels.get('component')


def get_client_provider_host(pod):
    return get_env_variable(pod, 'ONECLIENT_PROVIDER_HOST')


def get_env_variable(pod, env_name):
    envs = get_env_variables(pod)
    for env in envs:
        if env.name == env_name:
            return env.value
    return None


def get_env_variables(pod):
    return pod.spec.containers[0].env


def init_helm():
    sp.call(helm_init_cmd(client_only=True))


def helm_init_cmd(client_only=None):
    cmd = ['helm', 'init']

    if client_only:
        cmd.append('--client-only')

    return cmd


def run_onenv_command(command, args=None):
    cmd = ['./onenv', command]

    if args:
        cmd.extend(args)

    print('Running command: {}'.format(cmd))
    proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, cwd='one_env')
    output, err = proc.communicate()

    sys.stdout.write(output.decode('utf-8'))
    sys.stderr.write(err.decode('utf-8'))

    return output


def create_users(pod_name, users):
    """Creates system users on pod specified by 'pod'."""

    def _user_exists(user, pod_name):
        command = ['id', '-u', user]
        ret = sp.call(cmd_exec(pod_name, command))

        if ret == 1:
            return False
        elif ret == 0:
            return True

    for user in users:
        user_exists = _user_exists(user, pod_name)

        if user_exists:
            print('Skipping creation of user {} - user already exists in {}.'
                  .format(user, pod_name))
        else:
            uid = str(hash(user) % 50000 + 10000)
            command = ['adduser', '--disabled-password', '--gecos', '""',
                       '--uid', uid, user]
            assert 0 is sp.call(cmd_exec(pod_name, command))


def create_groups(pod_name, groups):
    """Creates system groups on docker specified by 'container'."""

    def _group_exists(group, pod_name):
        command = ['grep', '-q', group, '/etc/group']
        ret = sp.call(cmd_exec(pod_name, command))

        if ret == 1:
            return False
        elif ret == 0:
            return True

    for group in groups:
        group_exists = _group_exists(group, pod_name)
        if group_exists:
            print('Skipping creation of group {} - group already exists in {}.'
                  .format(group, pod_name))
        else:
            gid = str(hash(group) % 50000 + 10000)
            command = ['groupadd', '-g', gid, group]
            assert 0 is sp.call(cmd_exec(pod_name, command))
        for user in groups[group]:
            command = ['usermod', '-a', '-G', group, user]
            assert 0 is sp.call(cmd_exec(pod_name, command))


def get_kube_client():
    urllib3.disable_warnings()
    config.load_kube_config()
    kube = client.CoreV1Api()
    return kube


def list_pods_and_jobs():
    kube = get_kube_client()
    namespace = get_current_namespace()
    return kube.list_namespaced_pod(namespace).items


def cmd_exec(pod, command):
    if isinstance(command, list):
        return ['kubectl', '--namespace', get_current_namespace(),
                'exec', '-it', pod, '--'] + command
    else:
        return ['kubectl', '--namespace', get_current_namespace(),
                'exec', '-it', pod, '--', command]


def get_name(component):
    return component.metadata.name


def is_pod(pod):
    if pod.metadata.owner_references:
        return pod.metadata.owner_references[0].kind != 'Job'


def list_pods():
    return list(filter(lambda pod: is_pod(pod), list_pods_and_jobs()))


def match_pods(substring):
    pods_list = list_pods()
    # Accept dashes as wildcard characters
    pattern = '.*{}.*'.format(substring.replace('-', '.*'))
    return list(filter(lambda pod: re.match(pattern, get_name(pod)), pods_list))


def get_current_namespace():
    return get('currentNamespace')


def get(key):
    config = load_yaml(user_config_path())
    return config[key]


# FIXME use config reader from reauserders
def load_yaml(path):
    with open(path) as f:
        return yaml.load(f)


def user_config_path():
    return os.path.join(one_env_directory(), 'config.yaml')


def one_env_directory():
    return os.path.join(host_home(), '.one-env')


def host_home():
    return os.path.expanduser('~')
