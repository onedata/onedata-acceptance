"""Tests for retaining demo-mode state between container restarts."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps import (
    assert_persistence_state,
    create_persistence_state,
)
from tests.demo_mode.steps import (
    run_persistent_oneprovider,
    run_persistent_onezone,
    stop_persistent_environment,
)

TEST_FILE_CONTENT = b"Onedata demo-mode persistence REST test\n"


@pytest.mark.usefixtures("isolated_persistence_directories")
def test_persistency(release: str, request: pytest.FixtureRequest) -> None:
    onezone_process = run_persistent_onezone(release, request)
    oneprovider_process = run_persistent_oneprovider(
        release,
        onezone_process,
        request,
    )
    access_token, provider_id, space_id, file_name = create_persistence_state(
        release,
        TEST_FILE_CONTENT,
    )

    stop_persistent_environment(oneprovider_process, onezone_process)

    restarted_onezone_process = run_persistent_onezone(release, request)
    run_persistent_oneprovider(
        release,
        restarted_onezone_process,
        request,
    )
    assert_persistence_state(
        release,
        TEST_FILE_CONTENT,
        access_token,
        provider_id,
        space_id,
        file_name,
    )
