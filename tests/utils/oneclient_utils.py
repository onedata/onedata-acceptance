"""This module implements some common basic oneclient functions
and functionality for acceptance tests of onedata.
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.utils.acceptance_utils import execute_command


def do_ls(path, pod_name, user):
    list_ = execute_command(['kubectl', 'exec', pod_name, '--', 'runuser', '-l',
                             user, '-c', 'ls -Ald {}'.format(path)]).split('\n')
    # remove empty strings
    list_ = [x for x in list_ if x]
    res = {}
    for file_ in list_:
        file_ = file_.split()
        filename = file_[-1].split('/')[-1]
        res[filename] = {'owner_name': file_[2],
                         'owner_group': file_[3],
                         'permissions': file_[0]}
    return res


def do_mkdir(path, pod_name):
    execute_command(['kubectl', 'exec', pod_name, '--', 'mkdir', '-p', path])


def do_chown(path, owner, pod_name):
    execute_command(['kubectl', 'exec', pod_name, '--', 'chown', owner, path])


def create_users_in_oneclient_pods(config, pod_name):
    for username, uid in config.items():
        execute_command(['kubectl', 'exec', pod_name, '--',
                         'useradd', '-u', str(uid), username],
                        error='Error adding user in oneclient pod')


def create_groups_in_oneclient_pods(config, pod_name):
    for groupname, gid in config.items():
        execute_command(['kubectl', 'exec', pod_name, '--',
                         'groupadd', '-g', str(gid), groupname],
                        error='Error adding group in oneclient pod')


def mount_oneclient(mountpoint, pod_name, user, token, provider_ip):
    execute_command(['kubectl', 'exec', pod_name, '--', 'runuser', '-l', user, '-c',
                     'oneclient -i -H {provider_ip} -t {token} {mountpoint}'.format(
                         provider_ip=provider_ip,
                         token=token,
                         mountpoint=mountpoint
                     )])


def create_file_as_user_using_oneclient(path, user, pod_name):
    execute_command(['kubectl', 'exec', pod_name, '--', 'runuser', '-l', user,
                     '-c', 'touch {}'.format(path)])
