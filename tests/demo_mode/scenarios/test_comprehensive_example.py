"""Tests for the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.meta_steps.examples import get_comprehensive_example_file_name
from tests.demo_mode.meta_steps.rest import assert_onezone_configuration
from tests.demo_mode.steps.examples import run_comprehensive_example
from tests.demo_mode.steps.rest import (
    assert_file_content,
    download_rest_file,
    get_demo_access_token,
)


def test_comprehensive_example(
    release: str,
    onezone_name: str,
    first_oneprovider_container: str,
) -> None:
    demo_space_id = "cb274b2b8bb1750d9be37dd4a3eb7014chb175"
    expected_file_content = b"hello world\\n"
    command_output = run_comprehensive_example(release)
    assert_onezone_configuration(release, onezone_name)
    file_name = get_comprehensive_example_file_name(command_output)
    access_token = get_demo_access_token(release)
    downloaded_content = download_rest_file(
        first_oneprovider_container,
        access_token,
        demo_space_id,
        file_name,
    )
    assert_file_content(
        first_oneprovider_container,
        downloaded_content,
        expected_file_content,
    )
