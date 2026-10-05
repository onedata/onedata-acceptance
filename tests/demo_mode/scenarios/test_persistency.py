"""Tests for retaining demo-mode state between container restarts."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.persistence import (
    assert_persistence_state,
    save_persistent_state,
    start_persistent_environment,
)
from tests.demo_mode.meta_steps.rest import assert_onezone_configuration
from tests.demo_mode.steps.persistence import stop_persistent_environment
from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.rest import OnezoneRestClient


@pytest.mark.usefixtures("isolated_persistence_directories")
def test_persistency(
    release: str,
    demo_commands: DemoCommands,
    request: pytest.FixtureRequest,
) -> None:
    test_file_content = b"Onedata demo-mode persistence REST test\n"

    environment = start_persistent_environment(demo_commands, request)
    assert_onezone_configuration(
        OnezoneRestClient(environment.onezone),
        release=release,
    )

    persistence_state = save_persistent_state(
        environment,
        release=release,
        file_content=test_file_content,
        request=request,
    )
    stop_persistent_environment(environment)
    restarted_environment = start_persistent_environment(demo_commands, request)
    assert_onezone_configuration(
        OnezoneRestClient(restarted_environment.onezone),
        release=release,
    )
    assert_persistence_state(
        restarted_environment,
        release=release,
        file_content=test_file_content,
        state=persistence_state,
    )
