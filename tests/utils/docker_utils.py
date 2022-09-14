"""This module contains utility functions for running commands in docker
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import subprocess

from environment import docker


def run_cmd(username, client, cmd, detach=False, output=False, error=False):
    """Run command in docker
    :param username: command will be run as given user
    :param client: instance of utils.client_utils.Client class
    :param cmd: command to be run, can be string or list of strings
    :param detach: argument passed to docker.exec_, if true process started in
    docker will be in detached mode
    :param output: argument passed to docker.exec_, if false function will
    return exit code of run command, otherwise its output
    :param error: argument passed to docker.exec_, if true stderr will be
    redirected to stdout
    """
    # convert command into ascii string or list of ascii strings
    if isinstance(cmd, str):
        cmd = str(cmd)
    elif isinstance(cmd, list):
        cmd = [str(x) for x in cmd]

    if username != 'root' and isinstance(cmd, str):
        cmd = ['su', '-c', cmd, str(username)]
    elif username != 'root' and isinstance(cmd, list):
        cmd = ['su', '-c'] + cmd + [str(username)]

    return docker.exec_(container=client, command=cmd, output=output,
                        tty=True, stderr=subprocess.STDOUT if error else None,
                        detach=detach)


def docker_ip(container):
    return docker.inspect(container)['NetworkSettings']['IPAddress']
