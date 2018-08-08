"""This module contains gherkin for operations on oneclient.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml
import pytest
from pytest_bdd import given, parsers
from tests.gui.utils.generic import parse_seq
from tests.utils.acceptance_utils import get_pod_names_matching_regexp, wt
from tests.utils.oneclient_utils import (create_entities_in_oneclient_containers,
                                         do_touch, do_rm, do_cat,
                                         do_mkdir, mount_oneclient,
                                         do_ls, do_chown)


def full_space_path(mountpoint, user, space, path):
    return '{}/{}/{}/{}'.format(mountpoint, user, space, path)


@given(parsers.re('(?P<users_list>.*) mounted (?P<clients_list>.*) to '
                  '(?P<host>.*) on "(?P<client_pod>.*)"'))
def g_mount_oneclient(clients, clients_list, users_list, users, hosts,
                      host, client_pod):
    for user, client in zip(parse_seq(users_list), parse_seq(clients_list)):
        oneclient_pods = get_pod_names_matching_regexp(client_pod)
        mountpath = '/mnt/oneclient'
        mountpoint = '{}/{}'.format(mountpath, user)
        for pod_name in oneclient_pods:
            do_mkdir(mountpoint, pod_name)
            do_chown(mountpoint, user, pod_name)
            mount_oneclient(mountpoint, pod_name, users[user].token,
                            hosts[host]['ip'])
            clients[client] = {'mountpoint': mountpath,
                               'pod_name': pod_name}


@given(parsers.re('there are mounted clients:\n(?P<config>(.|\s)+)'))
def map_existing_clients(config, clients):
    config = yaml.load(config)
    for client, regexp in config.items():
        clients[client] = {'mountpoint': '/mnt/oneclient',
                           'pod_name': get_pod_names_matching_regexp(regexp)[0]}


@given(parsers.re('created in oneclient containers:\n(?P<config>(.|\s)+)'))
def create_groups_and_users(config):
    config = yaml.load(config)
    oneclient_pods = get_pod_names_matching_regexp('oneclient')
    for pod in oneclient_pods:
        create_entities_in_oneclient_containers(config['groups'], pod, 'group')
        create_entities_in_oneclient_containers(config['users'], pod, 'user')


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) creates file '
               '"(?P<path>.*)" in space "(?P<space>.*)"'))
def create_file(path, client, clients, user, space):
    pod_name = clients[client]['pod_name']
    parent_path = '/'.join(path.split('/')[:-1])
    if parent_path:
        parent_path = full_space_path(clients[client]['mountpoint'], user, space,
                                      parent_path)
        do_mkdir(parent_path, pod_name)
    file_path = full_space_path(clients[client]['mountpoint'], user, space, path)
    do_touch(file_path, pod_name)


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) fails to create file '
               '"(?P<path>.*)" in space "(?P<space>.*)"'))
def fail_to_create_file(path, client, clients, user, space):
    with pytest.raises(RuntimeError, message="File creation did not fail"):
        create_file(path, client, clients, user, space)


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) (?P<res>sees|does not see) '
               '(file )?"(?P<file_list>.*)" in space "(?P<space>[\w-]+)"'))
def assert_files_exist(file_list, client, clients, user, space, res):
    pod_name = clients[client]['pod_name']
    for path in parse_seq(file_list):
        full_path = full_space_path(clients[client]['mountpoint'], user, space, path)
        filename = path.split('/')[-1]
        if res == 'sees':
            error = 'File {} does not exist'.format(path)
            assert filename in do_ls(full_path, pod_name, error=error).keys(), \
                error
        else:
            do_ls(full_path, pod_name, should_fail=True,
                  error='File {} exists on client {} when it shouldn\'t'
                  .format(filename, client))


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) sees that '
               '"(?P<path>.*)" in space "(?P<space>[\w-]+)" (?P<res>has|has not):\n'
               '(?P<description>(.|\s)+)'))
def assert_file_stats(client, clients, user, path, description, space, res):
    filename = path.split('/')[-1]
    path = full_space_path(clients[client]['mountpoint'], user, space, path)
    pod_name = clients[client]['pod_name']
    file_stat = do_ls(path, pod_name)[filename]
    description = yaml.load(description)
    if 'not' in res:
        for key, value in description.items():
            assert file_stat[key] != str(value), 'File {} has {} {} when it shouldn\'t'.format(
                path, key, file_stat[key], value)
    else:
        for key, value in description.items():
            assert file_stat[key] == str(value), 'File {} has {} {} instead of {}'.format(
                path, key, file_stat[key], value)


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) (?P<res>tries|succeeds) to '
               '(?P<force>force )?remove (?P<rec>directory )?"(?P<filename>.*)" '
               'in space "(?P<space>.*)"'))
def remove_file_or_directory(filename, client, clients, user, space, res, force, rec):
    path = full_space_path(clients[client]['mountpoint'], user, space, filename)
    pod_name = clients[client]['pod_name']
    should_fail = (res == 'tries')
    do_rm(path, pod_name, force=force, recursive=rec, should_fail=should_fail)


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) opens "(?P<filename>.*)" '
               'in space "(?P<space>.*)"'))
def open_file(filename, client, clients, user, space):
    path = full_space_path(clients[client]['mountpoint'], user, space, filename)
    pod_name = clients[client]['pod_name']
    do_cat(path, pod_name)


@wt(parsers.re('there is file "(?P<path>.*)" in container "(?P<container>.*)" '
               'on provider "(?P<provider>.*)"'))
def assert_file_in_storage(path, container, provider, hosts):
    pod_name = get_pod_names_matching_regexp(hosts[provider]['name'])[0]
    filename = path.split('/')[-1]
    assert filename in do_ls(path, pod_name, container=container).keys(), \
        'File {} does not exists in storage {}'.format(filename, container)


@wt(parsers.re('file "(?P<path>.*)" in container "(?P<container>.*)" '
               'on provider "(?P<provider>.*)" has:\n(?P<description>(.|\s)+)'))
def assert_file_stats_in_storage(path, container, provider, hosts, description):
    pod_name = get_pod_names_matching_regexp(hosts[provider]['name'])[0]
    filename = path.split('/')[-1]
    file_stat = do_ls(path, pod_name, container=container)[filename]
    description = yaml.load(description)
    for key, value in description.items():
        assert file_stat[key] == str(value), 'File {} has {} {} instead of {}'.format(
            path, key, file_stat[key], value)
