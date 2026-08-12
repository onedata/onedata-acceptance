"""Tests for running the demo-mode environment in the foreground."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.steps import (
    assert_onezone_configuration,
    assert_rest_file_content,
    get_demo_access_token,
    get_rest_space_id,
    run_oneprovider,
    run_onezone,
    upload_rest_file,
)


def test_run_in_foreground(
    release: str,
    first_oneprovider_container_name: str,
    request: pytest.FixtureRequest,
) -> None:
    test_file_content = b"Onedata demo-mode foreground REST test\n"

    onezone_process = run_onezone(release, request)
    run_oneprovider(release, onezone_process, request)

    assert_onezone_configuration(release)

    access_token = get_demo_access_token(release)
    space_id = get_rest_space_id(
        first_oneprovider_container_name,
        "demo-space",
        access_token,
    )
    file_name = upload_rest_file(
        first_oneprovider_container_name,
        space_id,
        access_token,
        test_file_content,
    )
    assert_rest_file_content(
        first_oneprovider_container_name,
        access_token,
        space_id,
        file_name,
        test_file_content,
    )
