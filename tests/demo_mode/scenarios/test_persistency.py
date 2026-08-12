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
    assert_onezone_configuration,
    run_persistent_oneprovider,
    run_persistent_onezone,
    stop_persistent_environment,
)


@pytest.mark.usefixtures("isolated_persistence_directories")
def test_persistency(
    release: str,
    onezone_name: str,
    onezone_container_name: str,
    first_oneprovider_container_name: str,
    request: pytest.FixtureRequest,
) -> None:
    test_file_content = b"Onedata demo-mode persistence REST test\n"

    onezone_process = run_persistent_onezone(release, request)
    oneprovider_process = run_persistent_oneprovider(
        release,
        onezone_process,
        request,
    )
    assert_onezone_configuration(release, onezone_name)
    access_token, provider_id, space_id, file_name = create_persistence_state(
        release,
        test_file_content,
        first_oneprovider_container_name,
        request,
    )

    stop_persistent_environment(
        oneprovider_process,
        onezone_process,
        first_oneprovider_container_name,
        onezone_container_name,
    )

    restarted_onezone_process = run_persistent_onezone(release, request)
    run_persistent_oneprovider(
        release,
        restarted_onezone_process,
        request,
    )
    assert_onezone_configuration(release, onezone_name)
    assert_persistence_state(
        release,
        test_file_content,
        first_oneprovider_container_name,
        access_token,
        provider_id,
        space_id,
        file_name,
    )
