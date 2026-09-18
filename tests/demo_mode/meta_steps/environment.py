"""Composite steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.constants import (
    FIRST_ONEPROVIDER_CONTAINER,
    SECOND_ONEPROVIDER_CONTAINER,
)
from tests.demo_mode.steps.environment import (
    await_oneprovider,
    await_onezone,
    run_background_oneprovider,
    run_background_onezone,
    run_foreground_oneprovider,
    run_foreground_onezone,
)


def start_foreground_environment(
    release: str,
    request: pytest.FixtureRequest,
) -> None:
    """Start and await a foreground Onezone and Oneprovider."""
    onezone_process = run_foreground_onezone(release, request)
    oneprovider_process = run_foreground_oneprovider(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
        onezone_process,
        request,
    )

    await_onezone(release, onezone_process)
    await_oneprovider(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
        oneprovider_process,
    )


def start_distributed_environment(
    release: str,
    request: pytest.FixtureRequest,
) -> None:
    """Start and await a foreground Onezone and two Oneproviders."""
    onezone_process = run_foreground_onezone(release, request)
    first_oneprovider_process = run_foreground_oneprovider(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
        onezone_process,
        request,
    )
    second_oneprovider_process = run_foreground_oneprovider(
        release,
        SECOND_ONEPROVIDER_CONTAINER,
        onezone_process,
        request,
    )

    await_onezone(release, onezone_process)
    await_oneprovider(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
        first_oneprovider_process,
    )
    await_oneprovider(
        release,
        SECOND_ONEPROVIDER_CONTAINER,
        second_oneprovider_process,
    )


def start_background_environment(
    release: str,
    request: pytest.FixtureRequest,
) -> None:
    """Start and await a detached Onezone and Oneprovider."""
    run_background_onezone(release, request)
    run_background_oneprovider(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
        request,
    )

    await_onezone(release)
    await_oneprovider(release, FIRST_ONEPROVIDER_CONTAINER)
