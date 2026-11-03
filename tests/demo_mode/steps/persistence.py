"""Steps for persistent demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess

from environment import docker

from tests.demo_mode.constants import (
    ONEZONE_CONTAINER,
    SERVICE_READY_TIMEOUT,
)
from tests.demo_mode.type_definitions import DemoService, Oneprovider, Onezone
from tests.demo_mode.utils.commands import (
    RUN_ONEPROVIDER_PERSISTENT,
    RUN_ONEZONE_PERSISTENT,
)
from tests.demo_mode.utils.logging import log_step
from tests.utils.docker_utils import wait_for_running_container


@log_step("Starting persistent Onezone")
def start_persistent_onezone() -> Onezone:
    """Start Onezone using the unmodified persistence command."""
    onezone = Onezone(
        container=ONEZONE_CONTAINER,
        process=RUN_ONEZONE_PERSISTENT.start(),
    )
    wait_for_running_container(
        onezone.container,
        onezone.process,
        timeout=SERVICE_READY_TIMEOUT,
    )
    return onezone


@log_step("Starting persistent Oneprovider")
def start_persistent_oneprovider(
    container: str,
    onezone: Onezone,
) -> Oneprovider:
    """Start Oneprovider using the unmodified persistence command."""
    if onezone.process is None or onezone.process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")

    return Oneprovider(
        container=container,
        process=RUN_ONEPROVIDER_PERSISTENT.start(container),
    )


@log_step("Stopping persistent demo-mode service")
def stop_persistent_service(service: DemoService, timeout: float) -> None:
    docker.stop(
        service.container,
        command_timeout=timeout,
    )
    if service.process is None:
        raise AssertionError(f"Persistent service {service.container} has no launcher process")
    try:
        service.process.wait(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"The command running {service.container} did not exit after Docker stop"
        ) from error
