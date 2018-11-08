"""This module contains gherkin for operations on oneclient.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import os

import yaml
from pytest_bdd import given, parsers

from tests import ONECLIENT_MOUNTPATH_PREFIX
from tests.gui.utils.generic import parse_seq
from tests.utils.acceptance_utils import wt
from tests.utils.onenv_utils import match_pods, get_name
from tests.utils.oneclient_utils import (do_touch, do_rm, do_cat,
                                         do_mkdir, mount_oneclient, do_ls)


def full_space_path(mountpoint, user, space, path):
    return '{}/{}/{}/{}'.format(mountpoint, user, space, path)


@given(parsers.re('(?P<users_list>.*) mounted clients to '
                  '(?P<host>.*) on (?P<client_host>.*)'))
def g_mount_oneclient(clients, users_list, users, hosts,
                      host, client_host):
    pod_name = clients[client_host]['pod_name']
    for user in parse_seq(users_list):
        mountpoint = '{}/{}'.format(ONECLIENT_MOUNTPATH_PREFIX, user)
        do_mkdir(mountpoint, pod_name)
        mount_oneclient(mountpoint, pod_name, users[user].token,
                        hosts[host]['ip'])


@given(parsers.re('there are client hosts:\n(?P<config>(.|\s)+)'))
def map_existing_clients(config, clients):
    config = yaml.load(config)
    for client, regexp in config.items():
        clients[client] = {'mountpoint': ONECLIENT_MOUNTPATH_PREFIX,
                           'pod_name': get_name(match_pods(regexp)[0])}


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) (?P<res>fails|succeeds) to '
               'create file "(?P<path>.*)" in space "(?P<space>.*)"'))
def create_file(path, client, clients, user, space, res):
    pod_name = clients[client]['pod_name']
    parent_path = os.path.dirname(path)
    if parent_path:
        parent_path = full_space_path(clients[client]['mountpoint'], user, space,
                                      parent_path)
        do_mkdir(parent_path, pod_name)
    file_path = full_space_path(clients[client]['mountpoint'], user, space, path)
    should_fail = (res == 'fails')
    do_touch(file_path, pod_name, should_fail=should_fail)


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) (?P<res>sees|does not see) '
               '(file )?"(?P<file_list>.*)" in space "(?P<space>[\w-]+)"'))
def assert_files_exist(file_list, client, clients, user, space, res):
    pod_name = clients[client]['pod_name']
    for path in parse_seq(file_list):
        full_path = full_space_path(clients[client]['mountpoint'], user, space, path)
        filename = os.path.basename(path)
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
    filename = os.path.basename(path)
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


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) (?P<res>fails|succeeds) to '
               '(?P<force>force )?remove (?P<rec>directory )?"(?P<filename>.*)" '
               'in space "(?P<space>.*)"'))
def remove_file_or_directory(filename, client, clients, user, space, res, force, rec):
    path = full_space_path(clients[client]['mountpoint'], user, space, filename)
    pod_name = clients[client]['pod_name']
    should_fail = (res == 'fails')
    do_rm(path, pod_name, force=force, recursive=rec, should_fail=should_fail)


@wt(parsers.re('using (?P<client>\w+) (?P<user>\w+) opens "(?P<filename>.*)" '
               'in space "(?P<space>.*)"'))
def open_file(filename, client, clients, user, space):
    path = full_space_path(clients[client]['mountpoint'], user, space, filename)
    pod_name = clients[client]['pod_name']
    do_cat(path, pod_name)


@wt(parsers.re('there is file "(?P<path>.*)" in container "(?P<container>.*)" '
               'on provider "(?P<provider>.*)"'))
def assert_file_exists_in_storage(path, container, provider, hosts):
    pod_name = get_name(match_pods(hosts[provider]['name'])[0])
    filename = os.path.basename(path)
    assert filename in do_ls(path, pod_name, container=container).keys(), \
        'File {} does not exists in storage {}'.format(filename, container)


@wt(parsers.re('file "(?P<path>.*)" in container "(?P<container>.*)" '
               'on provider "(?P<provider>.*)" has:\n(?P<description>(.|\s)+)'))
def assert_file_stats_in_storage(path, container, provider, hosts, description):
    pod_name = get_name(match_pods(hosts[provider]['name'])[0])
    filename = os.path.basename(path)
    file_stat = do_ls(path, pod_name, container=container)[filename]
    description = yaml.load(description)
    for key, value in description.items():
        assert file_stat[key] == str(value), 'File {} has {} {} instead of {}'.format(
            path, key, file_stat[key], value)
