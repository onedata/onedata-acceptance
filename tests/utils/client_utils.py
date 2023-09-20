"""This module contains utility functions for using client instances under tests.
"""
__author__ = "Jakub Kudzia, Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2016-2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import os
import time
import stat as stat_lib
import hashlib
import subprocess

import random
import string

from tests.utils import ONECLIENT_LOGS_DIR, ONECLIENT_MOUNT_DIR
from tests.utils.utils import log_exception
from tests.utils.path_utils import escape_path


class Client:
    def __init__(self, rpyc_connection, timeout=40):
        self._id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
        self._mount_path = os.path.join(ONECLIENT_MOUNT_DIR, self._id)
        self.rpyc_connection = rpyc_connection
        self.timeout = timeout
        self.opened_files = {}
        self.file_stats = {}

    def mount(self, mode, gdb=False, additional_opts=None):
        if 'proxy' in mode:
            mode_flag = '--force-proxy-io'
        else:
            mode_flag = '--force-direct-io'
        if additional_opts is None:
            additional_opts = ['--message-trace-log']

        print(f'\nMounting client with {mode_flag} flag in {self._mount_path}\n')

        logdir = os.path.join(ONECLIENT_LOGS_DIR, self._id)
        self.mkdir(self._mount_path, recursive=True, exist_ok=True)
        self.mkdir(logdir, recursive=True, exist_ok=True)

        if gdb:
            cmd = ('gdb oneclient -batch -return-child-result -ex'
                   ' \'run --log-dir /tmp/oc_logs {mode} --insecure {mount_path}'
                   ' \' -ex \'bt\'').format(mount_path=self._mount_path, mode=mode_flag)
        else:
            cmd = " ".join(['oneclient', '--log-dir', logdir, mode_flag, '-v2', '--insecure']
                           + additional_opts + [self._mount_path])

        ret = self.run_cmd(cmd, verbose=True)

        return ret

    def unmount(self):
        print(f"\nUnmounting client from {self._mount_path}\n")
        for opened_file in self.opened_files.keys():
            self.close_file(opened_file)
        self.opened_files.clear()
        self.fusermount(self._mount_path, unmount=True, lazy=True)
        self.rm(path=self._mount_path, recursive=True, force=True)

    def absolute_path(self, path):
        return os.path.join(self._mount_path, str(path))

    def perform(self, condition, timeout=None):
        if timeout is None:
            timeout = self.timeout
        return self._repeat_until(condition, timeout)

    @staticmethod
    def _repeat_until(condition, timeout):
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

    def list_spaces(self):
        return self.ls(path=self._mount_path)

    def ls(self, path='.'):
        return self.rpyc_connection.modules.os.listdir(path)

    def osrename(self, src, dest):
        self.rpyc_connection.modules.os.rename(src, dest)

    def mv(self, src, dest):
        self.rpyc_connection.modules.shutil.move(src, dest)

    def chmod(self, mode, file_path):
        self.rpyc_connection.modules.os.chmod(file_path, mode)

    def stat(self, path):
        return self.rpyc_connection.modules.os.stat(path)

    def rm(self, path, recursive=False, force=False, onerror=None):
        if recursive and force:
            self.rpyc_connection.modules.shutil.rmtree(path, ignore_errors=True,
                                                       onerror=onerror)
        elif recursive:
            self.rpyc_connection.modules.shutil.rmtree(path, onerror=onerror)
        else:
            self.rpyc_connection.modules.os.remove(path)

    def rmdir(self, dir_path, recursive=False):

        if recursive:
            self.rpyc_connection.modules.os.removedirs(dir_path)
        else:
            self.rpyc_connection.modules.os.rmdir(dir_path)

    def mkdir(self, dir_path, recursive=False, exist_ok=False):
        if recursive:
            self.rpyc_connection.modules.os.makedirs(dir_path, exist_ok=exist_ok)
        else:
            self.rpyc_connection.modules.os.mkdir(dir_path)

    def create_file(self, file_path, mode=0o664):
        self.rpyc_connection.modules.os.mknod(file_path, mode | stat_lib.S_IFREG)

    def touch(self, file_path):
        self.rpyc_connection.modules.os.utime(file_path, None)

    def cp(self, src, dest, recursive=False):
        if recursive:
            if self.rpyc_connection.modules.os.path.isdir(dest):
                # shutil.copytree fails if dest is an existing directory
                dest = os.path.join(dest, os.path.basename(os.path.normpath(src)))
                self.rpyc_connection.modules.shutil.copytree(src, dest)
            else:
                self.rpyc_connection.modules.shutil.copytree(src, dest)
        else:
            self.rpyc_connection.modules.shutil.copy(src, dest)

    def truncate(self, file_path, size):
        with self.rpyc_connection.builtins.open(file_path, 'w') as f:
            f.truncate(size)

    def write(self, text, file_path, mode='w'):
        with self.rpyc_connection.builtins.open(file_path, mode) as f:
            f.write(text)

    def read(self, file_path, mode='r'):
        with self.rpyc_connection.builtins.open(file_path, mode) as f:
            read_text = f.read()
        return read_text

    def open_file(self, file, mode='w+'):
        return self.rpyc_connection.builtins.open(file, mode)

    def close_file(self, file):
        self.opened_files[file].close()

    def write_to_opened_file(self, file, text):
        self.opened_files[file].write(text)
        self.opened_files[file].flush()

    def read_from_opened_file(self, file):
        return self.opened_files[file].read()

    def seek(self, file, offset):
        self.opened_files[file].seek(offset)

    def setxattr(self, file, name, value):
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        xattrs[name] = value

    def getxattr(self, file, name):
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        return xattrs[name]

    def get_all_xattr(self, file):
        return self.rpyc_connection.modules.xattr.xattr(file)

    def listxattr(self, file):
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        return xattrs.list()

    def removexattr(self, file, name):
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        del xattrs[name]

    def clear_xattr(self, file):
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        try:
            xattrs.clear()
        except KeyError:
            pass

    def execute(self, command, output=False):
        if output:
            return self.rpyc_connection.modules.subprocess.check_output(command)
        else:
            return self.rpyc_connection.modules.subprocess.call(command)

    def md5sum(self, file_path):
        m = hashlib.md5()
        with self.rpyc_connection.builtins.open(file_path, 'r') as f:
            m.update(f.read().encode('utf-8'))
        return m.hexdigest()

    def mkstemp(self, dir=None):
        _handle, abs_path = self.rpyc_connection.modules.tempfile.mkstemp(dir=dir)
        return abs_path

    def mkdtemp(self, dir=None):
        return self.rpyc_connection.modules.tempfile.mkdtemp(dir=dir)

    def replace_pattern(self, file_path, pattern, new_text, output=False):
        cmd = 'sed -i \'s/{pattern}/{new_text}/g\' {file_path}'\
            .format(pattern=pattern,
                    new_text=new_text,
                    file_path=escape_path(file_path))
        return self.run_cmd(cmd, output=output)

    def dd(self, block_size, count, output_file, unit='M',
           input_file='/dev/zero', output=False, error=False):
        cmd = 'dd {input} {output} {bs} {count}'\
            .format(input='if={}'.format(escape_path(input_file)),
                    output='of={}'.format(escape_path(output_file)),
                    bs='bs={0}{1}'.format(block_size, unit),
                    count='count={}'.format(count))
        return self.run_cmd(cmd, output=output, error=error)

    def fusermount(self, path, unmount=False, lazy=False, quiet=False):
        unmount = '-u' if unmount else ''
        lazy = '-z' if lazy else ''
        quiet = '-q' if quiet else ''
        path = escape_path(path)
        cmd = ['fusermount', unmount, lazy, quiet, path]
        self.run_cmd(cmd)

    def run_cmd(self, cmd, output=False, error=False,
                retries=0, retry_sleep=8, on_retry=None, verbose=False):
        """Run command on oneself docker using rpyc
        :param self: instance of utils.client_utils.Client class
        :param cmd: command to be run, can be string or list of strings
        :param output: if false function will return exit code of run command, otherwise its output
        :param error: if true stderr will be redirected to stdout
        :param retries: maximum number of retries if command failed
        :param retry_sleep: only applicable if retries>0; time of idleness between retries
        :param on_retry: only applicable if retries>0; function to be executed
        after command failed, before next retry
        :param verbose: if True additional info will be printed to stdout
        """
        rpyc_connection = self.rpyc_connection

        if isinstance(cmd, list):
            cmd = [x for x in cmd if x]  # remove empty command tokens
            shell = False
        else:
            shell = True
        if verbose:
            print("rpyc running command: {}".format(cmd))
        proc = rpyc_connection.modules.subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT if error else subprocess.PIPE,
            shell=shell
        )

        if proc.wait() == 0:
            stdout = proc.stdout.read().decode()
            if verbose:
                print(stdout)
            return stdout if output else 0
        else:
            if verbose:
                print(proc.stdout.read().decode())
                if not error:
                    print(proc.stderr.read().decode())
            if retries > 0:
                if verbose:
                    print("Command {} failed. Retries left: {}".format(" ".join(cmd), retries))
                if on_retry:
                    on_retry()
                time.sleep(retry_sleep)
                return self.run_cmd(cmd, output=output, error=error, retries=retries-1,
                                    retry_sleep=retry_sleep, on_retry=on_retry, verbose=verbose)

        return None if output else proc.returncode


def user_home_dir(user='root'):
    return os.path.join('/home', user)


def get_client_conf(client_id, client_host_alias, env_desc):
    client_host_conf = env_desc.get('oneclient').get(client_host_alias)
    client_conf = client_host_conf.get('clients').get(client_id)
    client_conf["id"] = client_id
    return client_conf
