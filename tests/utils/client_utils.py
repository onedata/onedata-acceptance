"""This module contains utility functions for using client instances under
tests. Client is started in docker during env_up, acceptance and performance
tests.
"""
__author__ = "Jakub Kudzia, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import os
import time
import errno
import stat as stat_lib
import hashlib
import subprocess
from collections import namedtuple

import rpyc
import pytest

from .docker_utils import run_cmd
from tests.utils.utils import (log_exception, assert_)
from tests.utils.path_utils import escape_path
from tests.utils.user_utils import User


BAD_TOKEN = 'bad token'
CORRECT_TOKEN = 'token'
RPYC_DEFAULT_PORT = 18812

CLIENT_CONF = namedtuple('ClientConf', ['user', 'mount_path', 'client_host',
                                        'client_instance', 'token'])


class Client:
    def __init__(self, mount_path, provider, docker_id, ip, timeout=40):
        self.mount_path = mount_path
        self.provider = provider
        self.rpyc_connection = None
        self.rpyc_server_pid = None
        self.docker_id = docker_id
        self.ip = ip
        self.timeout = timeout
        self.opened_files = {}
        self.file_stats = {}

    def mount(self, username, hosts, access_token, mode, gdb=False, retries=3,
              clean_mountpoint=True):
        if clean_mountpoint:
            clean_mount_path(username, self)
        if 'proxy' in mode:
            mode_flag = '--force-proxy-io'
        else:
            mode_flag = '--force-direct-io'

        print('Mounting client with {} flag'.format(mode_flag))

        mkdir(self, self.mount_path, recursive=True, exist_ok=True)
        mkdir(self, "/tmp/oc_logs", recursive=True, exist_ok=True)
        self.rpyc_connection.modules.os.environ['ONECLIENT_PROVIDER_HOST'] = \
            hosts[self.provider]['hostname']
        self.rpyc_connection.modules.os.environ['ONECLIENT_ACCESS_TOKEN'] = access_token

        if gdb:
            cmd = ('gdb oneclient -batch -return-child-result -ex'
                   ' \'run --log-dir /tmp/oc_logs {mode} --insecure {mount_path}'
                   ' \' -ex \'bt\'').format(
                mount_path=self.mount_path,
                mode=mode_flag)
        else:
            cmd = " ".join(['oneclient', '--log-dir', '/tmp/oc_logs', mode_flag,
                            '--insecure', self.mount_path])

        def retry_fun():
            if clean_mountpoint:
                clean_mount_path(username, self)

        returncode = client_run_cmd(self, cmd,
                                    on_retry=retry_fun,
                                    verbose=True, retries=retries)

        rm(self, path=os.path.join(os.path.dirname(self.mount_path), '.local'),
           recursive=True, force=True)

        return returncode

    def absolute_path(self, path):
        return os.path.join(self.mount_path, str(path))

    def start_rpyc(self, user, port):
        started = False
        timeout = 30
        while not started and timeout >= 0:
            try:
                self._start_rpyc_server(user, port)
                self.rpyc_connection = rpyc.classic.connect(self.ip, port)

                get_pid_cmd = ' | '.join(
                    ['ps aux', 'grep "rpyc_classic.py"',
                     'grep -v "grep"', 'awk \'{print $2}\'']
                )

                pid = client_run_cmd(self, get_pid_cmd, output=True, verbose=False)
                self.rpyc_server_pid = pid

                # change timeout for rpyc to avoid AsyncResultTimeout
                # in performance tests on bamboo
                self.rpyc_connection._config['sync_request_timeout'] = 300
                started = True
            except:
                time.sleep(1)
                timeout -= 1
        if not started:
            log_exception()
            pytest.skip('Environment error: rpc connection couldn\'t be established')

    def _start_rpyc_server(self, user_name, port):
        """start rpc server on client docker"""
        cmd = ('python3 `which rpyc_classic.py` --host 0.0.0.0 --port {}'
               .format(port))
        print("\n\nstarting rpyc server on client {}".format(self.ip))
        run_cmd(user_name, self.docker_id, cmd, detach=True)
        print("rpyc server on client {} successfully started".format(self.ip))

    def stop_rpyc_server(self):
        if self.rpyc_server_pid:
            for pid in self.rpyc_server_pid.split():
                kill(self, pid)
            self.rpyc_server_pid = None

    def perform(self, condition, timeout=None):
        if timeout is None:
            timeout = self.timeout
        return self._repeat_until(condition, timeout)

    def _repeat_until(self, condition, timeout):
        condition_satisfied = False
        while not condition_satisfied and timeout >= 0:
            try:
                condition_satisfied = condition()
                if condition_satisfied is None:
                    condition_satisfied = True
            except:
                condition_satisfied = False
                if timeout == 0:
                    log_exception()
            finally:
                if not condition_satisfied:
                    time.sleep(1)
                    timeout -= 1

        return condition_satisfied


def create_client(clients, username, mount_path, client_instance,
                  client_host, hosts, users, timeout, provider):
    container_id = hosts[client_host]['container-id']
    client_ip = hosts[client_host]['ip']
    provider_host = ''

    for host, host_cfg in hosts.items():
        if (host_cfg.get('service-type') == 'oneprovider' and
                host == provider):
            provider_host = host

    client = Client(mount_path, provider_host, container_id, client_ip,
                    timeout)

    clients[client_instance] = client
    users[username].clients[client_instance] = client

    return client


def mount_users(clients, user_names, mount_paths, client_hosts,
                client_instances, tokens, hosts, request, users, env_desc,
                should_fail=False, clean_mountpoint=True):
    params = zip(user_names, mount_paths, client_instances, client_hosts,
                 tokens)

    for i, (username, mount_path, client_instance, client_host,
            token) in enumerate(params):
        user = users.get(username)
        if not user:
            user = users[username] = User(username)

        client_host_conf = env_desc.get('oneclient').get(client_host)
        client_conf = client_host_conf.get('clients').get(client_instance)
        client = create_client(clients, username, mount_path, client_instance,
                               client_host, hosts, users,
                               client_conf.get('default timeout'),
                               client_conf.get('provider'))

        client.start_rpyc(username, i + RPYC_DEFAULT_PORT)

        access_token = user.token if token == CORRECT_TOKEN else token

        client_mode = client_conf.get('mode')
        retries = 1 if should_fail else 3
        ret = client.mount(username, hosts, access_token, client_mode,
                           retries=retries, clean_mountpoint=clean_mountpoint)

        if ret != 0 and (access_token != BAD_TOKEN and not should_fail):
            clean_mount_path(username, client)
            pytest.skip('Environment error: error mounting client')

        if access_token != BAD_TOKEN and not should_fail and clean_mountpoint:
            try:
                clean_spaces(client)
            except AssertionError:
                pytest.skip('Environment error: failed to clean spaces')

        if ret == 0:
            user.mark_last_operation_succeeded()
        else:
            user.mark_last_operation_failed()

    def fin():
        if clean_mountpoint:
            clean_clients(user_names, users)

    request.addfinalizer(fin)


def clean_clients(user_names, users, lazy=False):
    for user in users.values():
        for client in user.clients.values():
            for opened_file in client.opened_files.keys():
                close_file(client, opened_file)
            client.opened_files.clear()
            clean_mount_path(user.username, client, lazy)
    for user_name in user_names:
        for client in users[user_name].clients.values():
            client.stop_rpyc_server()
        users[user_name].clients.clear()


def clean_mount_path(user, client, lazy=False):
    try:
        clean_spaces(client)
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Error during cleaning up spaces: {}".format(e))
    finally:
        # get pid of running oneclient node
        get_pid_cmd = ' | '.join(
            ['ps aux', 'grep "oneclient .* {}"'.format(client.mount_path),
             'grep -v "grep"', 'awk {\'print $2\'}']
        )
        pid = client_run_cmd(client, get_pid_cmd, output=True)

        if pid:
            # kill oneclient process
            kill(client, pid)

        # unmount oneclient
        fusermount(client, client.mount_path, unmount=True, lazy=lazy)
        rm(client, path=client.mount_path, recursive=True, force=True)


def clean_spaces(client):
    spaces = ls(client, path=client.mount_path)
    for space in spaces:
        space_path = client.absolute_path(space)

        def condition():
            try:
                rm(client, path=space_path, recursive=True)
            except FileNotFoundError:
                return
            except OSError as e:
                # ignore EACCES errors during cleaning
                if e.errno == errno.EACCES:
                    return
        assert_(client.perform, condition)


def ls(client, path='.'):
    return client.rpyc_connection.modules.os.listdir(path)


def osrename(client, src, dest):
    client.rpyc_connection.modules.os.rename(src, dest)


def mv(client, src, dest):
    client.rpyc_connection.modules.shutil.move(src, dest)


def chmod(client, mode, file_path):
    client.rpyc_connection.modules.os.chmod(file_path, mode)


def stat(client, path):
    return client.rpyc_connection.modules.os.stat(path)


def rm(client, path, recursive=False, force=False, onerror=None):
    if recursive and force:
        client.rpyc_connection.modules.shutil.rmtree(path, ignore_errors=True,
                                                     onerror=onerror)
    elif recursive:
        client.rpyc_connection.modules.shutil.rmtree(path, onerror=onerror)
    else:
        client.rpyc_connection.modules.os.remove(path)


def rmdir(client, dir_path, recursive=False):

    if recursive:
        client.rpyc_connection.modules.os.removedirs(dir_path)
    else:
        client.rpyc_connection.modules.os.rmdir(dir_path)


def mkdir(client, dir_path, recursive=False, exist_ok=False):
    if recursive:
        client.rpyc_connection.modules.os.makedirs(dir_path, exist_ok=exist_ok)
    else:
        client.rpyc_connection.modules.os.mkdir(dir_path)


def create_file(client, file_path, mode=0o664):
    client.rpyc_connection.modules.os.mknod(file_path, mode | stat_lib.S_IFREG)


def touch(client, file_path):
    client.rpyc_connection.modules.os.utime(file_path, None)


def cp(client, src, dest, recursive=False):
    if recursive:
        if client.rpyc_connection.modules.os.path.isdir(dest):
            # shutil.copytree fails if dest is an existing directory
            dest = os.path.join(dest, os.path.basename(os.path.normpath(src)))
            client.rpyc_connection.modules.shutil.copytree(src, dest)
        else:
            client.rpyc_connection.modules.shutil.copytree(src, dest)
    else:
        client.rpyc_connection.modules.shutil.copy(src, dest)


def truncate(client, file_path, size):
    with client.rpyc_connection.builtins.open(file_path, 'w') as f:
        f.truncate(size)


def write(client, text, file_path, mode='w'):
    with client.rpyc_connection.builtins.open(file_path, mode) as f:
        f.write(text)


def read(client, file_path, mode='r'):
    with client.rpyc_connection.builtins.open(file_path, mode) as f:
        read_text = f.read()
    return read_text


def open_file(client, file, mode='w+'):
    return client.rpyc_connection.builtins.open(file, mode)


def close_file(client, file):
    client.opened_files[file].close()


def write_to_opened_file(client, file, text):
    client.opened_files[file].write(text)
    client.opened_files[file].flush()


def read_from_opened_file(client, file):
    return client.opened_files[file].read()


def seek(client, file, offset):
    client.opened_files[file].seek(offset)


def kill(client, pid, signal='KILL', user='root'):
    cmd = 'kill -{signal} {pid}'.format(signal=signal, pid=pid)
    return run_cmd(user, client.docker_id, cmd, detach=True)


def setxattr(client, file, name, value):
    xattrs = client.rpyc_connection.modules.xattr.xattr(file)
    xattrs[name] = value


def getxattr(client, file, name):
    xattrs = client.rpyc_connection.modules.xattr.xattr(file)
    return xattrs[name]


def get_all_xattr(client, file):
    return client.rpyc_connection.modules.xattr.xattr(file)


def listxattr(client, file):
    xattrs = client.rpyc_connection.modules.xattr.xattr(file)
    return xattrs.list()


def removexattr(client, file, name):
    xattrs = client.rpyc_connection.modules.xattr.xattr(file)
    del xattrs[name]


def clear_xattr(client, file):
    xattrs = client.rpyc_connection.modules.xattr.xattr(file)
    try:
        xattrs.clear()
    except KeyError:
        pass


def execute(client, command, output=False):
    if output:
        return client.rpyc_connection.modules.subprocess.check_output(command)
    else:
        return client.rpyc_connection.modules.subprocess.call(command)


def md5sum(client, file_path):
    m = hashlib.md5()
    with client.rpyc_connection.builtins.open(file_path, 'r') as f:
        m.update(f.read().encode('utf-8'))
    return m.hexdigest()


def mkstemp(client, dir=None):
    _handle, abs_path = client.rpyc_connection.modules.tempfile.mkstemp(dir=dir)
    return abs_path


def mkdtemp(client, dir=None):
    return client.rpyc_connection.modules.tempfile.mkdtemp(dir=dir)


def replace_pattern(client, file_path, pattern, new_text, user='root',
                    output=False):
    cmd = 'sed -i \'s/{pattern}/{new_text}/g\' {file_path}'\
        .format(pattern=pattern,
                new_text=new_text,
                file_path=escape_path(file_path))
    return client_run_cmd(client, cmd, output=output)


def dd(client, block_size, count, output_file, unit='M',
       input_file='/dev/zero', user='root', output=False, error=False):
    cmd = 'dd {input} {output} {bs} {count}'\
        .format(input='if={}'.format(escape_path(input_file)),
                output='of={}'.format(escape_path(output_file)),
                bs='bs={0}{1}'.format(block_size, unit),
                count='count={}'.format(count))
    return client_run_cmd(client, cmd, output=output, error=error)


def fusermount(client, path, unmount=False, lazy=False, quiet=False):
    unmount = '-u' if unmount else ''
    lazy = '-z' if lazy else ''
    quiet = '-q' if quiet else ''
    path = escape_path(path)
    cmd = ['fusermount', unmount, lazy, quiet, path]
    client_run_cmd(client, cmd)


def user_home_dir(user='root'):
    return os.path.join('/home', user)


def client_run_cmd(client, cmd, output=False, error=False,
                   retries=0, retry_sleep=8, on_retry=None, verbose=False):
    """Run command on oneclient docker using rpyc
    :param client: instance of utils.client_utils.Client class
    :param cmd: command to be run, can be string or list of strings
    :param output: if false function will return exit code of run command, otherwise its output
    :param error: if true stderr will be redirected to stdout
    :param retries: maximum number of retries if command failed
    :param retry_sleep: only applicable if retries>0; time of idleness between retries
    :param on_retry: only applicable if retries>0; function to be executed
    after command failed, before next retry
    :param verbose: if True additional info will be printed to stdout
    """
    rpyc_connection = client.rpyc_connection

    if isinstance(cmd, list):
        cmd = [x for x in cmd if x]  # remove empty command tokens
        shell = False
    else:
        shell = True
    if verbose: print("rpyc running command: {}".format(cmd))
    proc = rpyc_connection.modules.subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT if error else subprocess.PIPE,
        shell=shell
    )

    if proc.wait() == 0:
        stdout = proc.stdout.read().decode()
        if verbose: print(stdout)
        return stdout if output else 0
    else:
        if verbose: print(proc.stdout.read().decode())
        if verbose and not error: print(proc.stderr.read().decode())
        if retries > 0:
            if verbose: print("Command {} failed. Retries left: {}".format(" ".join(cmd), retries))
            if on_retry: on_retry()
            time.sleep(retry_sleep)
            return client_run_cmd(client, cmd, output=output, error=error,
                                  retries=retries - 1, retry_sleep=retry_sleep, on_retry=on_retry,
                                  verbose=verbose)

    return None if output else proc.returncode


def mount_client(client_conf, clients, hosts, request, users, env_desc, clean_mountpoint=True):
    mount_users(clients, [client_conf.user], [client_conf.mount_path],
                [client_conf.client_host], [client_conf.client_instance],
                [client_conf.token], hosts, request, users, env_desc,
                clean_mountpoint=clean_mountpoint)

    return users[client_conf.user].clients[client_conf.client_instance]
