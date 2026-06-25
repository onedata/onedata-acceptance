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
from collections.abc import Callable
from typing import IO, Mapping, Optional, Protocol, TypedDict, cast

from tests.utils import ONECLIENT_LOGS_DIR, ONECLIENT_MOUNT_DIR
from tests.utils.path_utils import escape_path
from tests.utils.utils import log_exception

type Command = str | list[str]
type Condition = Callable[[], Optional[bool]]
type XattrValue = str | bytes


class PathProxy(Protocol):
    def samefile(self, path1: str, path2: str) -> bool: ...
    def realpath(self, path: str) -> str: ...
    def isdir(self, path: str) -> bool: ...


class OsProxy(Protocol):
    path: PathProxy
    environ: dict[str, str]

    def listdir(self, path: str) -> list[str]: ...
    def rename(self, src: str, dest: str) -> None: ...
    def chmod(self, path: str, mode: int) -> None: ...
    def stat(self, path: str) -> os.stat_result: ...
    def lstat(self, path: str) -> os.stat_result: ...
    def remove(self, path: str) -> None: ...
    def removedirs(self, path: str) -> None: ...
    def rmdir(self, path: str) -> None: ...
    def makedirs(self, path: str, exist_ok: bool = ...) -> None: ...
    def mkdir(self, path: str) -> None: ...
    def mknod(self, path: str, mode: int) -> None: ...
    def link(self, src: str, dest: str) -> None: ...
    def symlink(self, src: str, dest: str) -> None: ...
    def utime(self, path: str, times: Optional[tuple[float, float]]) -> None: ...


class ShutilProxy(Protocol):
    def move(self, src: str, dest: str) -> str: ...
    def rmtree(
        self,
        path: str,
        ignore_errors: bool = ...,
        onerror: Optional[Callable[..., object]] = ...,
    ) -> None: ...
    def copytree(self, src: str, dest: str) -> str: ...
    def copy(self, src: str, dest: str) -> str: ...


class ProcessProxy(Protocol):
    stdout: IO[bytes]
    stderr: IO[bytes]
    returncode: int

    def wait(self) -> int: ...


class SubprocessProxy(Protocol):
    def check_output(self, command: Command) -> bytes: ...
    def call(self, command: Command) -> int: ...
    def Popen(  # pylint: disable=invalid-name
        self,
        command: Command,
        stdout: int,
        stderr: int,
        shell: bool,
    ) -> ProcessProxy: ...


class TempfileProxy(Protocol):
    def mkstemp(self, **kwargs: Optional[str]) -> tuple[int, str]: ...
    def mkdtemp(self, **kwargs: Optional[str]) -> str: ...


class XattrsProxy(Protocol):
    def __getitem__(self, name: str) -> bytes: ...
    def __setitem__(self, name: str, value: XattrValue) -> None: ...
    def __delitem__(self, name: str) -> None: ...
    def list(self) -> list[str]: ...
    def clear(self) -> None: ...


class XattrProxy(Protocol):
    def xattr(self, file: str) -> XattrsProxy: ...


class ModulesProxy(Protocol):
    os: OsProxy
    shutil: ShutilProxy
    subprocess: SubprocessProxy
    tempfile: TempfileProxy
    xattr: XattrProxy


class BuiltinsProxy(Protocol):
    def open(self, file: str, mode: str = ...) -> IO: ...


class RpycConnectionLike(Protocol):
    modules: ModulesProxy
    builtins: BuiltinsProxy
    _config: dict[str, object]


type CommandResult = Optional[int | str]

ClientConfig = TypedDict(
    "ClientConfig",
    {"id": str, "provider": str, "mode": str, "default timeout": int},
    total=False,
)


class Client:
    def __init__(
        self, rpyc_connection: RpycConnectionLike, timeout: Optional[int] = 40
    ) -> None:
        self._id = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(16)
        )
        self._mount_path = os.path.join(ONECLIENT_MOUNT_DIR, self._id)
        self.rpyc_connection = rpyc_connection
        self.timeout = timeout if timeout is not None else 40
        self.opened_files: dict[str, IO] = {}
        self.file_stats: dict[str, os.stat_result] = {}

    def mount(
        self,
        mode: Optional[str],
        gdb: bool = False,
        additional_opts: Optional[list[str]] = None,
    ) -> CommandResult:
        if mode and "proxy" in mode:
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

    def unmount(self) -> None:
        print(f"\nUnmounting client from {self._mount_path}\n")
        for opened_file in self.opened_files:
            self.close_file(opened_file)
        self.opened_files.clear()
        self.fusermount(self._mount_path, unmount=True, lazy=True)
        self.rm(path=self._mount_path, recursive=True, force=True)

    def absolute_path(self, path: str) -> str:
        return os.path.join(self._mount_path, path)

    def perform(self, condition: Condition, timeout: Optional[int] = None) -> bool:
        if timeout is None:
            timeout = self.timeout
        return self._repeat_until(condition, timeout)

    @staticmethod
    def _repeat_until(condition: Condition, timeout: int) -> bool:
        condition_satisfied = False
        while not condition_satisfied and timeout >= 0:
            try:
                result = condition()
                if result is None:
                    condition_satisfied = True
                else:
                    condition_satisfied = bool(result)
            except:  # pylint: disable=bare-except
                condition_satisfied = False
                if timeout == 0:
                    log_exception()
            finally:
                if not condition_satisfied:
                    time.sleep(1)
                    timeout -= 1

        return condition_satisfied

    def list_spaces(self) -> list[str]:
        return self.ls(path=self._mount_path)

    def ls(self, path: str = ".") -> list[str]:
        res = self.rpyc_connection.modules.os.listdir(path)
        if ".hardlinks" in res:
            res.remove(".hardlinks")
        if ".symlinks" in res:
            res.remove(".symlinks")
        return res

    def osrename(self, src: str, dest: str) -> None:
        self.rpyc_connection.modules.os.rename(src, dest)

    def mv(self, src: str, dest: str) -> None:
        self.rpyc_connection.modules.shutil.move(src, dest)

    def chmod(self, mode: int, file_path: str) -> None:
        self.rpyc_connection.modules.os.chmod(file_path, mode)

    def samefile(self, file_path1: str, file_path2: str) -> bool:
        return self.rpyc_connection.modules.os.path.samefile(file_path1, file_path2)

    def realpath(self, path: str) -> str:
        return self.rpyc_connection.modules.os.path.realpath(path)

    def stat(self, path: str) -> os.stat_result:
        return self.rpyc_connection.modules.os.stat(path)

    def lstat(self, path: str) -> os.stat_result:
        return self.rpyc_connection.modules.os.lstat(path)

    def rm(
        self,
        path: str,
        recursive: bool = False,
        force: bool = False,
        onerror: Optional[Callable[..., object]] = None,
    ) -> None:
        if recursive and force:
            self.rpyc_connection.modules.shutil.rmtree(
                path, ignore_errors=True, onerror=onerror
            )
        elif recursive:
            self.rpyc_connection.modules.shutil.rmtree(path, onerror=onerror)
        else:
            self.rpyc_connection.modules.os.remove(path)

    def rmdir(self, dir_path: str, recursive: bool = False) -> None:

        if recursive:
            self.rpyc_connection.modules.os.removedirs(dir_path)
        else:
            self.rpyc_connection.modules.os.rmdir(dir_path)

    def mkdir(
        self, dir_path: str, recursive: bool = False, exist_ok: bool = False
    ) -> None:
        if recursive or exist_ok:
            self.rpyc_connection.modules.os.makedirs(dir_path, exist_ok=exist_ok)
        else:
            self.rpyc_connection.modules.os.mkdir(dir_path)

    def create_file(self, file_path: str, mode: int = 0o664) -> None:
        self.rpyc_connection.modules.os.mknod(file_path, mode | stat_lib.S_IFREG)

    def create_hardlink(self, file_path: str, link_path: str) -> None:
        self.rpyc_connection.modules.os.link(file_path, link_path)

    def create_symlink(self, file_path: str, link_path: str) -> None:
        self.rpyc_connection.modules.os.symlink(file_path, link_path)

    def touch(self, file_path: str) -> None:
        self.rpyc_connection.modules.os.utime(file_path, None)

    def cp(self, src: str, dest: str, recursive: bool = False) -> None:
        if recursive:
            if self.rpyc_connection.modules.os.path.isdir(dest):
                # shutil.copytree fails if dest is an existing directory
                dest = os.path.join(dest, os.path.basename(os.path.normpath(src)))
                self.rpyc_connection.modules.shutil.copytree(src, dest)
            else:
                self.rpyc_connection.modules.shutil.copytree(src, dest)
        else:
            self.rpyc_connection.modules.shutil.copy(src, dest)

    def truncate(self, file_path: str, size: int) -> None:
        with self.rpyc_connection.builtins.open(file_path, "w") as f:
            f.truncate(size)

    def write(self, text: str | bytes, file_path: str, mode: str = "w") -> None:
        with self.rpyc_connection.builtins.open(file_path, mode) as f:
            f.write(cast(str, text))

    def read(self, file_path: str, mode: str = "r") -> str | bytes:
        with self.rpyc_connection.builtins.open(file_path, mode) as f:
            read_text = f.read()
        return read_text

    def open_file(self, file: str, mode: str = "w+") -> IO:
        return self.rpyc_connection.builtins.open(file, mode)

    def close_file(self, file: str) -> None:
        self.opened_files[file].close()

    def write_to_opened_file(self, file: str, text: str | bytes) -> None:
        self.opened_files[file].write(cast(str, text))
        self.opened_files[file].flush()

    def read_from_opened_file(self, file: str) -> str:
        return self.opened_files[file].read()

    def seek(self, file: str, offset: int) -> None:
        self.opened_files[file].seek(offset)

    def setxattr(self, file: str, name: str, value: XattrValue) -> None:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        xattrs[name] = value

    def getxattr(self, file: str, name: str) -> bytes:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        return xattrs[name]

    def get_all_xattr(self, file: str) -> Mapping[str, str]:
        return cast(Mapping[str, str], self.rpyc_connection.modules.xattr.xattr(file))

    def listxattr(self, file: str) -> list[str]:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        return xattrs.list()

    def removexattr(self, file: str, name: str) -> None:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        del xattrs[name]

    def clear_xattr(self, file: str) -> None:
        xattrs = self.rpyc_connection.modules.xattr.xattr(file)
        try:
            xattrs.clear()
        except KeyError:
            pass

    def execute(self, command: Command, output: bool = False) -> int | bytes:
        if output:
            return self.rpyc_connection.modules.subprocess.check_output(command)
        return self.rpyc_connection.modules.subprocess.call(command)

    def md5sum(self, file_path: str) -> str:
        m = hashlib.md5()
        with self.rpyc_connection.builtins.open(file_path, "r") as f:
            m.update(f.read().encode("utf-8"))
        return m.hexdigest()

    def mkstemp(self, directory: Optional[str] = None) -> str:
        _handle, abs_path = self.rpyc_connection.modules.tempfile.mkstemp(dir=directory)
        return abs_path

    def mkdtemp(self, directory: Optional[str] = None) -> str:
        return self.rpyc_connection.modules.tempfile.mkdtemp(dir=directory)

    def replace_pattern(
        self, file_path: str, pattern: str, new_text: str, output: bool = False
    ) -> CommandResult:
        cmd = f"sed -i 's/{pattern}/{new_text}/g' {escape_path(file_path)}"
        return self.run_cmd(cmd, output=output)

    def dd(
        self,
        block_size: int,
        count: int,
        output_file: str,
        unit: str = "M",
        input_file: str = "/dev/zero",
        output: bool = False,
        error: bool = False,
    ) -> CommandResult:
        cmd = "dd {input} {output} {bs} {count}"
        cmd = cmd.format(
            input=f"if={escape_path(input_file)}",
            output=f"of={escape_path(output_file)}",
            bs=f"bs={block_size}{unit}",
            count=f"count={count}",
        )
        return self.run_cmd(cmd, output=output, error=error)

    def fusermount(
        self, path: str, unmount: bool = False, lazy: bool = False, quiet: bool = False
    ) -> None:
        unmount_flag = "-u" if unmount else ""
        lazy_flag = "-z" if lazy else ""
        quiet_flag = "-q" if quiet else ""
        path = escape_path(path)
        cmd = ["fusermount", unmount_flag, lazy_flag, quiet_flag, path]
        self.run_cmd(cmd)

    def run_cmd(
        self,
        cmd: Command,
        output: bool = False,
        error: bool = False,
        retries: int = 0,
        retry_sleep: int | float = 8,
        on_retry: Optional[Callable[[], None]] = None,
        verbose: bool = False,
    ) -> CommandResult:
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

    def get_mount_path(self) -> str:
        return self._mount_path


def user_home_dir(user: str = "root") -> str:
    return os.path.join("/home", user)


def get_client_conf(
    client_id: str, client_host_alias: str, env_desc: Mapping[str, object]
) -> ClientConfig:
    client_host_mapping = cast(Mapping[str, object], env_desc.get("oneclient") or {})
    client_host_conf = cast(
        Mapping[str, object], client_host_mapping.get(client_host_alias) or {}
    )
    client_conf = cast(
        ClientConfig,
        cast(Mapping[str, object], client_host_conf.get("clients") or {}).get(client_id)
        or {},
    )
    client_conf["id"] = client_id
    return client_conf
