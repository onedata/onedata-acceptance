"""Steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

from tests.demo_mode.constants import ONEZONE_CONTAINER
from tests.demo_mode.models import DemoService, Oneprovider, Onezone
from tests.demo_mode.utils.commands import Command, DemoCommands
from tests.demo_mode.utils.logging import log_step
from tests.utils.docker_utils import wait_for_running_container

ENVIRONMENT_START_TIMEOUT: Final = 600.0


def _await_running_container(
    service: DemoService,
    command: Command,
) -> None:
    wait_for_running_container(service.container, service.process)
    command.run_until_success(timeout=ENVIRONMENT_START_TIMEOUT)


@log_step("Running Onezone in the foreground")
def run_foreground_onezone(
    commands: DemoCommands,
) -> Onezone:
    return Onezone(
        container=ONEZONE_CONTAINER,
        process=commands.foreground_onezone().start(),
    )


@log_step("Running Oneprovider in the foreground")
def run_foreground_oneprovider(
    commands: DemoCommands,
    container: str,
    onezone: Onezone,
) -> Oneprovider:
    if onezone.process is None or onezone.process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")
    return Oneprovider(
        container=container,
        process=commands.foreground_oneprovider(container).start(),
    )


@log_step("Running Onezone in the background")
def run_background_onezone(
    commands: DemoCommands,
) -> Onezone:
    commands.background_onezone().run(timeout=ENVIRONMENT_START_TIMEOUT)
    return Onezone(container=ONEZONE_CONTAINER)


@log_step("Running Oneprovider in the background")
def run_background_oneprovider(
    commands: DemoCommands,
    container: str,
) -> Oneprovider:
    commands.background_oneprovider(container).run(timeout=ENVIRONMENT_START_TIMEOUT)
    return Oneprovider(container=container)


@log_step("Awaiting Onezone")
def await_onezone(
    commands: DemoCommands,
    onezone: Onezone,
) -> None:
    _await_running_container(
        onezone,
        commands.await_onezone(),
    )


@log_step("Awaiting Oneprovider")
def await_oneprovider(
    commands: DemoCommands,
    oneprovider: Oneprovider,
) -> None:
    _await_running_container(
        oneprovider,
        commands.await_oneprovider(oneprovider.container),
    )
