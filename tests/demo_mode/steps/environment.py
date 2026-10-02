"""Steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

import pytest

from tests.demo_mode.constants import ONEZONE_CONTAINER
from tests.demo_mode.type_definitions import DemoService, Oneprovider, Onezone
from tests.demo_mode.utils.commands import CommandTemplate
from tests.demo_mode.utils.logging import log_step
from tests.utils.docker_utils import wait_for_running_container

FOREGROUND_ONEZONE_COMMAND_PATH: Final = "run_in_foreground/run_onezone.sh"
FOREGROUND_ONEPROVIDER_COMMAND_PATH: Final = "run_in_foreground/run_oneprovider.sh"
BACKGROUND_ONEZONE_COMMAND_PATH: Final = "run_in_background/run_onezone.sh"
BACKGROUND_ONEPROVIDER_COMMAND_PATH: Final = "run_in_background/run_oneprovider.sh"
AWAIT_ONEZONE_COMMAND_PATH: Final = "run_in_background/await_onezone.sh"
AWAIT_ONEPROVIDER_COMMAND_PATH: Final = "run_in_background/await_oneprovider.sh"
ENVIRONMENT_START_TIMEOUT: Final = 600.0


def _await_running_container(
    service: DemoService,
    command: CommandTemplate,
) -> None:
    wait_for_running_container(service.container, service.process)
    command.run_until_success(
        service.container,
        timeout=ENVIRONMENT_START_TIMEOUT,
    )


@log_step("Running Onezone in the foreground")
def run_foreground_onezone(
    release: str,
    request: pytest.FixtureRequest,
) -> Onezone:
    command = CommandTemplate(FOREGROUND_ONEZONE_COMMAND_PATH, release)
    onezone = Onezone(
        container=ONEZONE_CONTAINER,
        process=command.start(),
    )
    request.addfinalizer(onezone.stop_process)
    return onezone


@log_step("Running Oneprovider in the foreground")
def run_foreground_oneprovider(
    release: str,
    container: str,
    onezone: Onezone,
    request: pytest.FixtureRequest,
) -> Oneprovider:
    if onezone.process is None or onezone.process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")
    command = CommandTemplate(FOREGROUND_ONEPROVIDER_COMMAND_PATH, release)
    oneprovider = Oneprovider(
        container=container,
        process=command.start(container),
    )
    request.addfinalizer(oneprovider.stop_process)
    return oneprovider


@log_step("Running Onezone in the background")
def run_background_onezone(
    release: str,
) -> Onezone:
    command = CommandTemplate(BACKGROUND_ONEZONE_COMMAND_PATH, release)
    command.run(timeout=ENVIRONMENT_START_TIMEOUT)
    return Onezone(container=ONEZONE_CONTAINER)


@log_step("Running Oneprovider in the background")
def run_background_oneprovider(
    release: str,
    container: str,
) -> Oneprovider:
    command = CommandTemplate(BACKGROUND_ONEPROVIDER_COMMAND_PATH, release)
    command.run(
        container,
        timeout=ENVIRONMENT_START_TIMEOUT,
    )
    return Oneprovider(container=container)


@log_step("Awaiting Onezone")
def await_onezone(
    onezone: Onezone,
) -> None:
    _await_running_container(
        onezone,
        CommandTemplate(AWAIT_ONEZONE_COMMAND_PATH),
    )


@log_step("Awaiting Oneprovider")
def await_oneprovider(
    oneprovider: Oneprovider,
) -> None:
    _await_running_container(
        oneprovider,
        CommandTemplate(AWAIT_ONEPROVIDER_COMMAND_PATH),
    )
