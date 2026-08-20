"""Steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial

import pytest

from tests.demo_mode.utils.commands import (
    load_command,
    start_command,
    stop_command,
    wait_for_successful_command,
)
from tests.utils.docker_utils import wait_for_running_container


def start_environment_command(
    release: str,
    command_path: str,
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    command = load_command(command_path, release)
    process = start_command(command, command_path)
    request.addfinalizer(partial(stop_command, process))
    return process


def await_running_container(
    release: str,
    container_name: str,
    command_path: str,
    startup_process: subprocess.Popen[str] | None = None,
) -> None:
    wait_for_running_container(container_name, startup_process)
    command = load_command(command_path, release)
    wait_for_successful_command(command, command_path)
