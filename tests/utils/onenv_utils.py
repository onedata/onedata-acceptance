"""This file contains utility functions for operation using onenv tool."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import os
import re
import sys
import collections
import subprocess as sp

import yaml
import urllib3
from kubernetes import client, config


# TODO: After resolving VFS-4820 all this function can be imported from
# one-env submodule

def client_alias_to_pod_mapping():
    prov_clients_mapping = collections.defaultdict(list)
    client_alias_mapping = {}
    pods_list = list_pods()
    clients_pods = [pod for pod in pods_list
                    if get_service_type(pod) == 'oneclient']
    for client_pod in clients_pods:
        provider = get_client_provider_host(client_pod)
        provider_alias = service_name_to_alias_mapping(provider)
        prov_clients_mapping[provider_alias].append(client_pod)

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

    return output, proc.returncode


def get_kube_client():
    urllib3.disable_warnings()
    config.load_kube_config()
    kube = client.CoreV1Api()
    return kube


def list_pods_and_jobs():
    kube = get_kube_client()
    namespace = get_current_namespace()
    return kube.list_namespaced_pod(namespace).items


def cmd_exec(pod, command, interactive=False, tty=False, container=None):
    cmd = ['kubectl', '--namespace', get_current_namespace(), 'exec']

    if interactive:
        cmd.append('-i')
    if tty:
        cmd.append('-t')
    cmd.append(pod)

    if container:
        cmd.extend(['-c', container])

    if isinstance(command, list):
        cmd.append('--')
        cmd += command
    else:
        cmd.extend(['--', command])

    return cmd


def get_name(component):
    return component.metadata.name


def get_ip(pod):
    return pod.status.pod_ip


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


def deployments_directory():
    return os.path.join(one_env_directory(), 'deployments')


def current_deployment_dir():
    all_deployments = os.listdir(deployments_directory())
    all_deployments.sort()
    if len(all_deployments) == 0:
        print 'There are no deployments'
        sys.exit(1)
    else:
        return os.path.join(deployments_directory(), all_deployments[-1])


def deployment_data_path():
    return os.path.join(current_deployment_dir(), 'deployment_data.yml')
