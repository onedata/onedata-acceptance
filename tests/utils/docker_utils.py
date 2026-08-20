"""This module contains utility functions for running commands in docker"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import re
import subprocess

from environment import docker  # pylint: disable=import-error

from tests.utils.time_utils import deadline_after, remaining_time, sleep_before_retry

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


def docker_ip(container: object) -> str:
    return docker.inspect(container)["NetworkSettings"]["IPAddress"]


def remove_containers(
    container_names: list[str],
    timeout: float = 60,
    interval: float = 1,
) -> None:
    """Force-remove Docker containers with the specified names."""
    if not container_names:
        return

    name_filters = [("name", rf"^/{re.escape(name)}$") for name in container_names]
    deadline = deadline_after(timeout)
    removal_started = False
    last_error: subprocess.CalledProcessError | None = None

    while remaining_time(deadline) > 0:
        containers = docker.ps(
            all=True,
            quiet=True,
            filters=name_filters,
        )
        if not containers:
            return

        if not removal_started:
            print("\nRemoved docker containers:", flush=True)
            removal_started = True

        try:
            docker.remove(
                containers,
                force=True,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError as error:
            last_error = error
            sleep_before_retry(deadline, interval)
        else:
            return

    remaining_containers = docker.ps(
        all=True,
        quiet=True,
        filters=name_filters,
    )
    if remaining_containers:
        raise AssertionError(
            "Could not remove demo-mode containers within "
            f"{timeout}s: {', '.join(container_names)}"
        ) from last_error


def wait_for_running_container(
    container_name: str,
    startup_process: subprocess.Popen[str] | None = None,
    timeout: float = 600,
    interval: float = 1,
) -> None:
    """Wait until an exact-name container is running."""
    deadline = deadline_after(timeout)
    name_filters = [("name", rf"^/{re.escape(container_name)}$")]

    while remaining_time(deadline) > 0:
        if startup_process is not None and startup_process.poll() is not None:
            raise AssertionError(
                f"Startup command exited before {container_name} was running "
                f"(exit code {startup_process.returncode})"
            )

        containers = docker.ps(
            quiet=True,
            filters=name_filters,
        )
        if containers:
            return

        sleep_before_retry(deadline, interval)

    raise AssertionError(f"Container {container_name} did not start within {timeout}s")
