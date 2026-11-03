"""This module contains utility functions for running commands in docker"""

__author__ = "Jakub Kudzia, Mateusz Zajac"
__copyright__ = "Copyright (C) 2016-2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import re
import subprocess
from collections.abc import Collection

from environment import docker

from tests.utils.utils import perform_action_with_timeout

DockerCommand = str | list[str]


def run_cmd(
    username: str,
    client: object,
    cmd: DockerCommand,
    detach: bool = False,
    output: bool = False,
    error: bool = False,
) -> object:
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

    if username != "root" and isinstance(cmd, str):
        cmd = ["su", "-c", cmd, str(username)]
    elif username != "root" and isinstance(cmd, list):
        cmd = ["su", "-c"] + cmd + [str(username)]

    return docker.exec_(
        container=client,
        command=cmd,
        output=output,
        tty=True,
        stderr=subprocess.STDOUT if error else None,
        detach=detach,
    )


def container_ip(container: str) -> str:
    inspection = docker.inspect(container)
    networks = inspection["NetworkSettings"]["Networks"]

    addresses = [network["IPAddress"] for network in networks.values() if network.get("IPAddress")]

    if len(addresses) != 1:
        raise AssertionError(
            f"Expected {container!r} to have exactly one IP address, got {addresses!r}"
        )

    return addresses[0]


def remove_containers(
    container_names: Collection[str],
    *,
    timeout: float,
    interval: float = 1,
) -> None:
    """Force-remove Docker containers with the specified names."""
    if not container_names:
        return

    name_filters = [("name", rf"^/{re.escape(name)}$") for name in container_names]

    def remove_existing_containers() -> None:
        containers = docker.ps(
            all=True,
            quiet=True,
            filters=name_filters,
        )
        if not containers:
            return

        print("\nRemoved docker containers:", flush=True)

        docker.remove(
            containers,
            force=True,
            stderr=subprocess.DEVNULL,
        )

    perform_action_with_timeout(
        remove_existing_containers,
        timeout=timeout,
        ignored_exceptions=subprocess.CalledProcessError,
        interval=interval,
    )


def wait_for_running_container(
    container_name: str,
    startup_process: subprocess.Popen[str] | None = None,
    *,
    timeout: float,
    interval: float = 1,
) -> None:
    """Wait until an exact-name container is running."""
    name_filters = [("name", rf"^/{re.escape(container_name)}$")]

    def assert_container_is_running() -> None:
        if startup_process is not None and startup_process.poll() is not None:
            raise AssertionError(
                f"Startup command exited before {container_name} was running "
                f"(exit code {startup_process.returncode})"
            )

        containers = docker.ps(
            quiet=True,
            filters=name_filters,
        )
        if not containers:
            raise _ContainerNotRunningError(
                f"Container {container_name} did not start within {timeout}s"
            )

    perform_action_with_timeout(
        assert_container_is_running,
        timeout=timeout,
        ignored_exceptions=_ContainerNotRunningError,
        interval=interval,
    )


class _ContainerNotRunningError(AssertionError):
    """Raised when a container has not reached the running state yet."""
