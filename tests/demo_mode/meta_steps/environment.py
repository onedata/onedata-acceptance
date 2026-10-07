"""Composite steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.constants import (
    ONEZONE_CONTAINER,
    oneprovider_container,
)
from tests.demo_mode.steps.environment import (
    await_oneprovider,
    await_onezone,
    run_background_oneprovider,
    run_background_onezone,
    run_foreground_oneprovider,
    run_foreground_onezone,
)
from tests.demo_mode.type_definitions import DemoEnvironment, Oneprovider, Onezone
from tests.demo_mode.utils.commands import DemoCommands


def start_foreground_environment(
    commands: DemoCommands,
    *,
    oneprovider_count: int = 1,
) -> DemoEnvironment:
    """Start and await a foreground Onezone and Oneprovider."""
    onezone = run_foreground_onezone(commands)

    oneproviders = tuple(
        run_foreground_oneprovider(
            commands,
            oneprovider_container(number),
            onezone,
        )
        for number in range(1, oneprovider_count + 1)
    )

    await_onezone(commands, onezone)
    for oneprovider in oneproviders:
        await_oneprovider(commands, oneprovider)

    return DemoEnvironment(
        onezone=onezone,
        oneproviders=oneproviders,
    )


def start_background_environment(
    commands: DemoCommands, *, oneprovider_count: int = 1
) -> DemoEnvironment:
    """Start and await a detached Onezone and Oneprovider."""
    onezone = run_background_onezone(commands)

    oneproviders = tuple(
        run_background_oneprovider(
            commands,
            oneprovider_container(number),
        )
        for number in range(1, oneprovider_count + 1)
    )

    await_onezone(commands, onezone)
    for oneprovider in oneproviders:
        await_oneprovider(commands, oneprovider)

    return DemoEnvironment(
        onezone=onezone,
        oneproviders=oneproviders,
    )


def guide_environment(
    *,
    oneprovider_count: int = 1,
) -> DemoEnvironment:
    """Describe an environment started externally by a guide script."""
    return DemoEnvironment(
        onezone=Onezone(container=ONEZONE_CONTAINER),
        oneproviders=tuple(
            Oneprovider(container=oneprovider_container(number))
            for number in range(1, oneprovider_count + 1)
        ),
    )
