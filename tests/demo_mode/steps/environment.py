"""Steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial
from typing import Final

import pytest

from tests.demo_mode.constants import ONEZONE_CONTAINER
from tests.demo_mode.utils.command_runner import (
    retry_command_until_success,
    start_command,
    stop_command,
    wait_for_process_success,
)
from tests.demo_mode.utils.command_templates import (
    load_command,
    substitute_container_name,
)
from tests.demo_mode.utils.logging import log_step
from tests.utils.docker_utils import wait_for_running_container

FOREGROUND_ONEZONE_COMMAND_PATH: Final = "run_in_foreground/run_onezone.sh"
FOREGROUND_ONEPROVIDER_COMMAND_PATH: Final = "run_in_foreground/run_oneprovider.sh"
BACKGROUND_ONEZONE_COMMAND_PATH: Final = "run_in_background/run_onezone.sh"
BACKGROUND_ONEPROVIDER_COMMAND_PATH: Final = "run_in_background/run_oneprovider.sh"
AWAIT_ONEZONE_COMMAND_PATH: Final = "run_in_background/await_onezone.sh"
AWAIT_ONEPROVIDER_COMMAND_PATH: Final = "run_in_background/await_oneprovider.sh"


def _start_environment_command(
    release: str,
    command_path: str,
    request: pytest.FixtureRequest,
    container_name: str | None = None,
) -> subprocess.Popen[str]:
    command = load_command(command_path, release)
    if container_name is not None:
        command = substitute_container_name(command, container_name)
    process = start_command(command, command_path)
    request.addfinalizer(partial(stop_command, process))
    return process


def _await_running_container(
    release: str,
    container_name: str,
    command_path: str,
    startup_process: subprocess.Popen[str] | None = None,
) -> None:
    wait_for_running_container(container_name, startup_process)
    command = load_command(command_path, release)
    command = substitute_container_name(command, container_name)
    retry_command_until_success(command, command_path)


@log_step("Running Onezone in the foreground")
def run_foreground_onezone(
    release: str,
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    return _start_environment_command(
        release,
        FOREGROUND_ONEZONE_COMMAND_PATH,
        request,
    )


@log_step("Running Oneprovider in the foreground")
def run_foreground_oneprovider(
    release: str,
    container_name: str,
    onezone_process: subprocess.Popen[str],
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    if onezone_process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")
    return _start_environment_command(
        release,
        FOREGROUND_ONEPROVIDER_COMMAND_PATH,
        request,
        container_name,
    )


@log_step("Running Onezone in the background")
def run_background_onezone(
    release: str,
    request: pytest.FixtureRequest,
) -> None:
    process = _start_environment_command(
        release,
        BACKGROUND_ONEZONE_COMMAND_PATH,
        request,
    )
    wait_for_process_success(process, BACKGROUND_ONEZONE_COMMAND_PATH)


@log_step("Running Oneprovider in the background")
def run_background_oneprovider(
    release: str,
    container_name: str,
    request: pytest.FixtureRequest,
) -> None:
    process = _start_environment_command(
        release,
        BACKGROUND_ONEPROVIDER_COMMAND_PATH,
        request,
        container_name,
    )
    wait_for_process_success(process, BACKGROUND_ONEPROVIDER_COMMAND_PATH)


@log_step("Awaiting Onezone")
def await_onezone(
    release: str,
    startup_process: subprocess.Popen[str] | None = None,
) -> None:
    _await_running_container(
        release,
        ONEZONE_CONTAINER,
        AWAIT_ONEZONE_COMMAND_PATH,
        startup_process,
    )


@log_step("Awaiting Oneprovider")
def await_oneprovider(
    release: str,
    container_name: str,
    startup_process: subprocess.Popen[str] | None = None,
) -> None:
    _await_running_container(
        release,
        container_name,
        AWAIT_ONEPROVIDER_COMMAND_PATH,
        startup_process,
    )
