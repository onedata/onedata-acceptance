"""This module contains gherkin for operations on oneclient.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml
from pytest_bdd import given, parsers
from tests.gui.utils.generic import parse_seq
from tests.utils.acceptance_utils import get_pod_names_matching_regexp, wt
from tests.utils.oneclient_utils import (create_groups_in_oneclient_pods,
                                         create_users_in_oneclient_pods,
                                         create_file_as_user_using_oneclient,
                                         do_mkdir, mount_oneclient, 
                                         do_ls, do_chown)


@given(parsers.re('(?P<users_list>.*) mounted (?P<clients_list>.*) to (?P<host>.*)'))
def g_mount_oneclient(clients, clients_list, users_list, users, hosts, host):
    for user, client in zip(parse_seq(users_list), parse_seq(clients_list)):
        oneclient_pods = get_pod_names_matching_regexp('oneclient')
        mountpoint = '/mnt/{}'.format(user)
        for pod_name in oneclient_pods:
            do_mkdir(mountpoint, pod_name)
            do_chown(mountpoint, user, pod_name)
            mount_oneclient(mountpoint, pod_name, user, users[user].token,
                            hosts[host]['ip'])
            clients[client] = {'mountpoint': mountpoint,
                               'pod_name': pod_name}


@given(parsers.re('created in oneclient containers:\n(?P<config>(.|\s)+)'))
def create_groups_and_users(config):
    config = yaml.load(config)
    oneclient_pods = get_pod_names_matching_regexp('oneclient')
    for pod in oneclient_pods:
        create_groups_in_oneclient_pods(config['groups'], pod)
        create_users_in_oneclient_pods(config['users'], pod)


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) creates file '
               '"(?P<filename>.*)" in space "(?P<space>.*)"'))
def create_file(filename, client, clients, user, space):
    path = '{}/{}/{}'.format(clients[client]['mountpoint'], space, filename)
    pod_name = clients[client]['pod_name']
    create_file_as_user_using_oneclient(path, user, pod_name)


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) sees '
               '"(?P<file_list>.*)" in space "(?P<space>\w+)"'))
def assert_files_exist(file_list, client, clients, user, space):
    pod_name = clients[client]['pod_name']
    for filename in parse_seq(file_list):
        path = '{}/{}/{}'.format(clients[client]['mountpoint'], space, filename)
        assert filename in do_ls(path, pod_name, user).keys(), \
            'File {} does not exist'.format(filename)


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) sees that '
               '"(?P<filename>.*)" in space "(?P<space>\w+)" has:\n'
               '(?P<description>(.|\s)+)'))
def assert_file_stats(client, clients, user, filename, description, space):
    path = '{}/{}/{}'.format(clients[client]['mountpoint'], space, filename)
    pod_name = clients[client]['pod_name']
    file_stat = do_ls(path, pod_name, user)[filename]
    description = yaml.load(description)
    for key, value in description.items():
        assert file_stat[key] == value, 'File {} has {} {} instead of {}'.format(
            filename, key, file_stat[key], value)
