"""Tests for retaining demo-mode state between container restarts."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.environment import assert_environment_configuration
from tests.demo_mode.meta_steps.persistence import (
    assert_persistent_state,
    save_persistent_state,
    start_persistent_environment,
    stop_persistent_environment,
)
from tests.demo_mode.steps.environment import get_demo_access_token
from tests.demo_mode.utils.commands import DemoCommands


@pytest.mark.usefixtures("isolated_persistence_directories")
def test_persistency(
    release: str,
    demo_commands: DemoCommands,
    request: pytest.FixtureRequest,
) -> None:
    space_name = "demo-mode-persistence-space"
    file_name = "persistence-rest-test.txt"
    file_content = b"Onedata demo-mode persistence REST test\n"

    environment = start_persistent_environment(demo_commands)
    (provider,) = environment.oneproviders
    access_token = get_demo_access_token(provider, demo_commands)
    assert_environment_configuration(
        environment,
        release=release,
        access_token=access_token,
    )

    persistence_state = save_persistent_state(
        environment,
        demo_commands,
        space_name=space_name,
        file_name=file_name,
        file_content=file_content,
        request=request,
    )
    stop_persistent_environment(environment)
    restarted_environment = start_persistent_environment(demo_commands)
    (restarted_provider,) = restarted_environment.oneproviders
    restarted_access_token = get_demo_access_token(restarted_provider, demo_commands)
    assert_environment_configuration(
        restarted_environment,
        release=release,
        access_token=restarted_access_token,
    )
    assert_persistent_state(
        restarted_environment,
        demo_commands,
        state=persistence_state,
    )
