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
from tests.demo_mode.type_definitions import DemoEnvironment


def start_foreground_environment(
    release: str,
    request: pytest.FixtureRequest,
) -> DemoEnvironment:
    """Start and await a foreground Onezone and Oneprovider."""
    onezone = run_foreground_onezone(release, request)
    oneprovider = run_foreground_oneprovider(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
        onezone,
        request,
    )

    await_onezone(onezone)
    await_oneprovider(oneprovider)
    return DemoEnvironment(
        onezone=onezone,
        oneproviders=(oneprovider,),
    )


def start_distributed_environment(
    release: str,
    request: pytest.FixtureRequest,
) -> DemoEnvironment:
    """Start and await a foreground Onezone and two Oneproviders."""
    onezone = run_foreground_onezone(release, request)
    first_oneprovider = run_foreground_oneprovider(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
        onezone,
        request,
    )
    second_oneprovider = run_foreground_oneprovider(
        release,
        SECOND_ONEPROVIDER_CONTAINER,
        onezone,
        request,
    )

    await_onezone(onezone)
    await_oneprovider(first_oneprovider)
    await_oneprovider(second_oneprovider)
    return DemoEnvironment(
        onezone=onezone,
        oneproviders=(first_oneprovider, second_oneprovider),
    )


def start_background_environment(
    release: str,
) -> DemoEnvironment:
    """Start and await a detached Onezone and Oneprovider."""
    onezone = run_background_onezone(release)
    oneprovider = run_background_oneprovider(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
    )

    await_onezone(onezone)
    await_oneprovider(oneprovider)
    return DemoEnvironment(
        onezone=onezone,
        oneproviders=(oneprovider,),
    )
