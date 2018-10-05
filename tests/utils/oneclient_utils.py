"""This module implements some common basic oneclient functions
and functionality for acceptance tests of onedata.
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os
from tests.utils.acceptance_utils import execute_command
from tests.utils.utils import repeat_failed


EXEC_CMD = ['kubectl', 'exec']


@repeat_failed(timeout=60, interval=4)
def do_ls(path, pod_name, should_fail=False, error=None, container=''):
    cmd = ['ls', '-Ald', path]
    exec_cmd = EXEC_CMD + ['-c', container] if container else EXEC_CMD
    files_list = execute_command(exec_cmd + [pod_name, '--'] + cmd,
                                 should_fail=should_fail, error=error).split('\n')
    files_list = [x for x in files_list if x]  # remove empty strings
    res = {}
    for f in files_list:
        f = f.split()
        filename = os.path.basename(f[-1])
        res[filename] = {'owner_name': f[2],
                         'owner_group': f[3],
                         'permissions': f[0]}
    return res


def do_mkdir(path, pod_name):
    cmd = ['mkdir', '-p', path]
    execute_command(EXEC_CMD + [pod_name, '--'] + cmd)


def do_rm(path, pod_name, should_fail=False, recursive=False, force=False):
    cmd = ['rm']
    if recursive:
        cmd += ['--recursive']
    if force:
        cmd += ['--force']
    cmd += [path]
    execute_command(EXEC_CMD + [pod_name, '--'] + cmd,
                    should_fail=should_fail)


def do_touch(path, pod_name, should_fail=False):
    cmd = ['touch', path]
    execute_command(EXEC_CMD + [pod_name, '--'] + cmd,
                    should_fail=should_fail)


def do_cat(path, pod_name):
    cmd = ['cat', path]
    return execute_command(EXEC_CMD + [pod_name, '--'] + cmd)


def mount_oneclient(mountpoint, pod_name, token, provider_ip):
    cmd = ['oneclient', '-i', '-H', provider_ip, '-t', token, mountpoint]
    execute_command(EXEC_CMD + [pod_name, '--'] + cmd,
                    error='Error mounting oneclient in {}'.format(mountpoint))
