"""This module implements some common basic oneclient functions
and functionality for acceptance tests of onedata.
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.utils.acceptance_utils import execute_command
from tests.gui.utils.generic import repeat_failed


EXEC_CMD = ['kubectl', 'exec']


@repeat_failed(timeout=60, interval=4)
def do_ls(path, pod_name, should_fail=False, error=None, container=''):
    cmd = ['ls', '-Ald', path]
    exec_cmd = EXEC_CMD + ['-c', container] if container else EXEC_CMD
    list_ = execute_command(exec_cmd + [pod_name, '--'] + cmd,
                            should_fail=should_fail, error=error).split('\n')
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
    cmd = ['--', 'mkdir', '-p', path]
    execute_command(EXEC_CMD + [pod_name] + cmd)


def do_rm(path, pod_name, should_fail=False, recursive=False, force=False):
    cmd = ['--', 'rm', ]
    if recursive:
        cmd += ['-r']
    if force:
        cmd += ['-f']
    cmd += [path]
    execute_command(EXEC_CMD + [pod_name] + cmd,
                    should_fail=should_fail)


def do_touch(path, pod_name):
    cmd = ['touch', path]
    execute_command(EXEC_CMD + [pod_name, '--'] + cmd)


def do_cat(path, pod_name):
    cmd = ['cat', path]
    return execute_command(EXEC_CMD + [pod_name, '--'] + cmd)


def do_chown(path, owner, pod_name):
    cmd = ['--', 'chown', owner, path]
    execute_command(EXEC_CMD + [pod_name] + cmd)


def create_entities_in_oneclient_containers(config, pod_name, entity_type):
    for name, _id in config.items():
        cmd = ['--', '{}add'.format(entity_type), '-{}'.format(entity_type[0]),
               str(_id), name]
        execute_command(EXEC_CMD + [pod_name] + cmd,
                        error='Error adding {} in oneclient pod {}'
                        .format(entity_type, pod_name))


def mount_oneclient(mountpoint, pod_name, token, provider_ip):
    cmd = ['oneclient', '-i', '-H', provider_ip, '-t', token, mountpoint]
    execute_command(EXEC_CMD + [pod_name, '--'] + cmd,
                    error='Error mounting oneclient in {}'.format(mountpoint))
