"""Tests for running the demo-mode environment in the background."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.steps.environment import (
    run_oneprovider_in_background,
    run_onezone_in_background,
)
from tests.demo_mode.steps.rest import (
    assert_onezone_configuration,
    assert_rest_file_content,
    get_demo_access_token,
    get_rest_space_id,
    upload_rest_file,
)


def test_run_in_background(
    release: str,
    onezone_name: str,
    demo_space_name: str,
    first_oneprovider_container_name: str,
    request: pytest.FixtureRequest,
) -> None:
    test_file_content = b"Onedata demo-mode background REST test\n"

    run_onezone_in_background(release)
    run_oneprovider_in_background(release)

    assert_onezone_configuration(release, onezone_name)

    access_token = get_demo_access_token(release)
    space_id = get_rest_space_id(
        first_oneprovider_container_name,
        demo_space_name,
        access_token,
    )
    file_name = upload_rest_file(
        first_oneprovider_container_name,
        space_id,
        access_token,
        test_file_content,
        request,
    )
    assert_rest_file_content(
        first_oneprovider_container_name,
        access_token,
        space_id,
        file_name,
        test_file_content,
    )
