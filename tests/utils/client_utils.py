"""This module contains utility functions for using client instances under tests."""

__author__ = "Jakub Kudzia, Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2016-2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import hashlib
import os
import random
import stat as stat_lib
import string
import subprocess
import time
from typing import Any

from tests.utils import ONECLIENT_LOGS_DIR, ONECLIENT_MOUNT_DIR
from tests.utils.path_utils import escape_path
from tests.utils.utils import log_exception


class Client:
    def __init__(self, rpyc_connection: Any, timeout: Any = 40) -> None:
        self._id = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(16)
        )
        self._mount_path = os.path.join(ONECLIENT_MOUNT_DIR, self._id)
        self.rpyc_connection = rpyc_connection
        self.timeout = timeout
        self.opened_files: dict[Any, Any] = {}
        self.file_stats: dict[Any, Any] = {}

    def mount(self, mode: Any, gdb: Any = False, additional_opts: Any = None) -> Any:
        if "proxy" in mode:
            mode_flag = "--force-proxy-io"
        else:
            mode_flag = "--force-direct-io"
        if additional_opts is None:
            additional_opts = ["--message-trace-log"]

        print(f"\nMounting client with {mode_flag} flag in {self._mount_path}\n")

        logdir = os.path.join(ONECLIENT_LOGS_DIR, self._id)
        self.mkdir(self._mount_path, recursive=True, exist_ok=True)
        self.mkdir(logdir, recursive=True, exist_ok=True)

        if gdb:
            cmd = (
                "gdb oneclient -batch -return-child-result -ex 'run --log-dir"
                f" /tmp/oc_logs {mode_flag} --insecure {self._mount_path} ' -ex 'bt'"
            )
        else:
            cmd = " ".join(
                ["oneclient", "--log-dir", logdir, mode_flag, "-v2", "--insecure"]
                + additional_opts
                + [self._mount_path]
            )

        ret = self.run_cmd(cmd, verbose=True)

        return ret

    def unmount(self) -> Any:
        print(f"\nUnmounting client from {self._mount_path}\n")
        for opened_file in self.opened_files:
            self.close_file(opened_file)
        self.opened_files.clear()
        self.fusermount(self._mount_path, unmount=True, lazy=True)
        self.rm(path=self._mount_path, recursive=True, force=True)

    def absolute_path(self, path: Any) -> Any:
        return os.path.join(self._mount_path, str(path))

    def perform(self, condition: Any, timeout: Any = None) -> Any:
        if timeout is None:
            timeout = self.timeout
        return self._repeat_until(condition, timeout)

    @staticmethod
    def _repeat_until(condition: Any, timeout: Any) -> Any:
        condition_satisfied = False
        while not condition_satisfied and timeout >= 0:
            try:
                condition_satisfied = condition()
                if condition_satisfied is None:
                    condition_satisfied = True
            except:  # pylint: disable=bare-except
                condition_satisfied = False
                if timeout == 0:
                    log_exception()
            finally:
                if not condition_satisfied:
                    time.sleep(1)
                    timeout -= 1

        return condition_satisfied

    def list_spaces(self) -> Any:
        return self.ls(path=self._mount_path)

    def ls(self, path: Any = ".") -> Any:
        res = self.rpyc_connection.modules.os.listdir(path)
        _ = res.remove(".hardlinks") if ".hardlinks" in res else None
        _ = res.remove(".symlinks") if ".symlinks" in res else None
        return res

    def osrename(self, src: Any, dest: Any) -> Any:
        self.rpyc_connection.modules.os.rename(src, dest)

    def mv(self, src: Any, dest: Any) -> Any:
        self.rpyc_connection.modules.shutil.move(src, dest)

    def chmod(self, mode: Any, file_path: Any) -> Any:
        self.rpyc_connection.modules.os.chmod(file_path, mode)

    def samefile(self, file_path1: Any, file_path2: Any) -> Any:
        return self.rpyc_connection.modules.os.path.samefile(file_path1, file_path2)

    def realpath(self, path: Any) -> Any:
        return self.rpyc_connection.modules.os.path.realpath(path)

    def stat(self, path: Any) -> Any:
        return self.rpyc_connection.modules.os.stat(path)

    def lstat(self, path: Any) -> Any:
        return self.rpyc_connection.modules.os.lstat(path)

    def rm(
        self, path: Any, recursive: Any = False, force: Any = False, onerror: Any = None
    ) -> Any:
        if recursive and force:
            self.rpyc_connection.modules.shutil.rmtree(
                path, ignore_errors=True, onerror=onerror
            )
        elif recursive:
            self.rpyc_connection.modules.shutil.rmtree(path, onerror=onerror)
        else:
            self.rpyc_connection.modules.os.remove(path)

    def rmdir(self, dir_path: Any, recursive: Any = False) -> Any:

        if recursive:
            self.rpyc_connection.modules.os.removedirs(dir_path)
        else:
            self.rpyc_connection.modules.os.rmdir(dir_path)

    def mkdir(
        self, dir_path: Any, recursive: Any = False, exist_ok: Any = False
    ) -> Any:
        if recursive or exist_ok:
            self.rpyc_connection.modules.os.makedirs(dir_path, exist_ok=exist_ok)
        else:
            self.rpyc_connection.modules.os.mkdir(dir_path)

    def create_file(self, file_path: Any, mode: Any = 0o664) -> Any:
        self.rpyc_connection.modules.os.mknod(file_path, mode | stat_lib.S_IFREG)

    def create_hardlink(self, file_path: Any, link_path: Any) -> Any:
        self.rpyc_connection.modules.os.link(file_path, link_path)

    def create_symlink(self, file_path: Any, link_path: Any) -> Any:
        self.rpyc_connection.modules.os.symlink(file_path, link_path)

    def touch(self, file_path: Any) -> Any:
        self.rpyc_connection.modules.os.utime(file_path, None)

    def cp(self, src: Any, dest: Any, recursive: Any = False) -> Any:
        if recursive:
            if self.rpyc_connection.modules.os.path.isdir(dest):
                # shutil.copytree fails if dest is an existing directory
                dest = os.path.join(dest, os.path.basename(os.path.normpath(src)))
                self.rpyc_connection.modules.shutil.copytree(src, dest)
            else:
                self.rpyc_connection.modules.shutil.copytree(src, dest)
        else:
            self.rpyc_connection.modules.shutil.copy(src, dest)

    def truncate(self, file_path: Any, size: Any) -> Any:
        with self.rpyc_connection.builtins.open(file_path, "w") as f:
            f.truncate(size)

    def write(self, text: Any, file_path: Any, mode: Any = "w") -> Any:
        with self.rpyc_connection.builtins.open(file_path, mode) as f:
            f.write(text)

    def read(self, file_path: Any, mode: Any = "r") -> Any:
        with self.rpyc_connection.builtins.open(file_path, mode) as f:
            read_text = f.read()
        return read_text

    def open_file(self, file: Any, mode: Any = "w+") -> Any:
        return self.rpyc_connection.builtins.open(file, mode)

    def close_file(self, file: Any) -> Any:
        self.opened_files[file].close()

    def write_to_opened_file(self, file: Any, text: Any) -> Any:
        self.opened_files[file].write(text)
        self.opened_files[file].flush()

    def read_from_opened_file(self, file: Any) -> Any:
        return self.opened_files[file].read()

    def seek(self, file: Any, offset: Any) -> Any:
        self.opened_files[file].seek(offset)

    def setxattr(self, file: Any, name: Any, value: Any) -> Any:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        xattrs[name] = value

    def getxattr(self, file: Any, name: Any) -> Any:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        return xattrs[name]

    def get_all_xattr(self, file: Any) -> Any:
        return self.rpyc_connection.modules.xattr.xattr(file)

    def listxattr(self, file: Any) -> Any:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        return xattrs.list()

    def removexattr(self, file: Any, name: Any) -> Any:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        del xattrs[name]

    def clear_xattr(self, file: Any) -> Any:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        try:
            xattrs.clear()
        except KeyError:
            pass

    def execute(self, command: Any, output: Any = False) -> Any:
        if output:
            return self.rpyc_connection.modules.subprocess.check_output(command)
        return self.rpyc_connection.modules.subprocess.call(command)

    def md5sum(self, file_path: Any) -> Any:
        m = hashlib.md5()
        with self.rpyc_connection.builtins.open(file_path, "r") as f:
            m.update(f.read().encode("utf-8"))
        return m.hexdigest()

    def mkstemp(self, directory: Any = None) -> Any:
        _handle, abs_path = self.rpyc_connection.modules.tempfile.mkstemp(dir=directory)
        return abs_path

    def mkdtemp(self, directory: Any = None) -> Any:
        return self.rpyc_connection.modules.tempfile.mkdtemp(dir=directory)

    def replace_pattern(
        self, file_path: Any, pattern: Any, new_text: Any, output: Any = False
    ) -> Any:
        cmd = f"sed -i 's/{pattern}/{new_text}/g' {escape_path(file_path)}"
        return self.run_cmd(cmd, output=output)

    def dd(
        self,
        block_size: Any,
        count: Any,
        output_file: Any,
        unit: Any = "M",
        input_file: Any = "/dev/zero",
        output: Any = False,
        error: Any = False,
    ) -> Any:
        cmd = "dd {input} {output} {bs} {count}"
        cmd = cmd.format(
            input=f"if={escape_path(input_file)}",
            output=f"of={escape_path(output_file)}",
            bs=f"bs={block_size}{unit}",
            count=f"count={count}",
        )
        return self.run_cmd(cmd, output=output, error=error)

    def fusermount(
        self, path: Any, unmount: Any = False, lazy: Any = False, quiet: Any = False
    ) -> Any:
        unmount = "-u" if unmount else ""
        lazy = "-z" if lazy else ""
        quiet = "-q" if quiet else ""
        path = escape_path(path)
        cmd = ["fusermount", unmount, lazy, quiet, path]
        self.run_cmd(cmd)

    def run_cmd(
        self,
        cmd: Any,
        output: Any = False,
        error: Any = False,
        retries: Any = 0,
        retry_sleep: Any = 8,
        on_retry: Any = None,
        verbose: Any = False,
    ) -> Any:
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
            print(f"rpyc running command: {cmd}")
        proc = rpyc_connection.modules.subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if error else subprocess.PIPE,
            shell=shell,
        )

        if proc.wait() == 0:
            stdout = proc.stdout.read().decode()
            if verbose:
                print(stdout)
            return stdout if output else 0

        if verbose:
            print(proc.stdout.read().decode())
            if not error:
                print(proc.stderr.read().decode())
        if retries > 0:
            if verbose:
                print(f"Command {" ".join(cmd)} failed. Retries left: {retries}")
            if on_retry:
                on_retry()
            time.sleep(retry_sleep)
            return self.run_cmd(
                cmd,
                output=output,
                error=error,
                retries=retries - 1,
                retry_sleep=retry_sleep,
                on_retry=on_retry,
                verbose=verbose,
            )

        return None if output else proc.returncode

    def get_mount_path(self) -> Any:
        return self._mount_path


def user_home_dir(user: Any = "root") -> Any:
    return os.path.join("/home", user)


def get_client_conf(client_id: Any, client_host_alias: Any, env_desc: Any) -> Any:
    client_host_conf = env_desc.get("oneclient").get(client_host_alias)
    client_conf = client_host_conf.get("clients").get(client_id)
    client_conf["id"] = client_id
    return client_conf
