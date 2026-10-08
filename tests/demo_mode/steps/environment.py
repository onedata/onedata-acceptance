"""Steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.constants import ONEZONE_CONTAINER, SERVICE_READY_TIMEOUT
from tests.demo_mode.type_definitions import DemoService, Oneprovider, Onezone
from tests.demo_mode.utils.commands import (
    AWAIT_ONEPROVIDER,
    AWAIT_ONEZONE,
    GET_ACCESS_TOKEN,
    RUN_ONEPROVIDER_BACKGROUND,
    RUN_ONEPROVIDER_FOREGROUND,
    RUN_ONEZONE_BACKGROUND,
    RUN_ONEZONE_FOREGROUND,
)
from tests.demo_mode.utils.logging import log_step
from tests.utils.docker_utils import wait_for_running_container


def get_demo_access_token(service: DemoService) -> str:
    access_token = GET_ACCESS_TOKEN.run(service.container).strip()
    if not access_token:
        raise AssertionError("The access-token command returned an empty result")
    return access_token


def _await_running_container(
    service: DemoService,
) -> None:
    wait_for_running_container(service.container, service.process, timeout=SERVICE_READY_TIMEOUT)


@log_step("Running Onezone in the foreground")
def run_foreground_onezone() -> Onezone:
    return Onezone(
        container=ONEZONE_CONTAINER,
        process=RUN_ONEZONE_FOREGROUND.start(),
    )


@log_step("Running Oneprovider in the foreground")
def run_foreground_oneprovider(
    container: str,
    onezone: Onezone,
) -> Oneprovider:
    if onezone.process is None or onezone.process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")
    return Oneprovider(
        container=container,
        process=RUN_ONEPROVIDER_FOREGROUND.start(container),
    )


@log_step("Running Onezone in the background")
def run_background_onezone() -> Onezone:
    RUN_ONEZONE_BACKGROUND.run(timeout=SERVICE_READY_TIMEOUT)
    return Onezone(container=ONEZONE_CONTAINER)


@log_step("Running Oneprovider in the background")
def run_background_oneprovider(
    container: str,
) -> Oneprovider:
    RUN_ONEPROVIDER_BACKGROUND.run(container, timeout=SERVICE_READY_TIMEOUT)
    return Oneprovider(container=container)


@log_step("Awaiting Onezone")
def await_onezone(
    onezone: Onezone,
) -> None:
    _await_running_container(onezone)
    AWAIT_ONEZONE.run_until_success(timeout=SERVICE_READY_TIMEOUT)


@log_step("Awaiting Oneprovider")
def await_oneprovider(
    oneprovider: Oneprovider,
) -> None:
    _await_running_container(oneprovider)
    AWAIT_ONEPROVIDER.run_until_success(
        oneprovider.container,
        timeout=SERVICE_READY_TIMEOUT,
    )
