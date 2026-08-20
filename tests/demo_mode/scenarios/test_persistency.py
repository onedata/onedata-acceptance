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


@pytest.mark.usefixtures("isolated_persistence_directories")
def test_persistency(
    release: str,
    onezone_name: str,
    onezone_container: str,
    first_oneprovider_container: str,
    request: pytest.FixtureRequest,
) -> None:
    test_file_content = b"Onedata demo-mode persistence REST test\n"

    onezone, oneprovider = start_persistent_environment(
        release,
        onezone_container,
        first_oneprovider_container,
        request,
    )
    assert_onezone_configuration(release, onezone_name)

    persistence_state = save_persistent_state(
        release,
        test_file_content,
        first_oneprovider_container,
        request,
    )
    stop_persistent_environment([oneprovider, onezone])
    start_persistent_environment(
        release,
        onezone_container,
        first_oneprovider_container,
        request,
    )
    assert_onezone_configuration(release, onezone_name)
    assert_persistence_state(
        release,
        test_file_content,
        first_oneprovider_container,
        persistence_state,
    )
