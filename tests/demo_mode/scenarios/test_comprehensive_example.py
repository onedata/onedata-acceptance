"""Tests for the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.meta_steps.comprehensive_example import (
    get_comprehensive_example_file_name,
)
from tests.demo_mode.meta_steps.environment import guide_environment
from tests.demo_mode.meta_steps.rest import assert_onezone_configuration
from tests.demo_mode.steps.comprehensive_example import run_comprehensive_example
from tests.demo_mode.steps.environment import get_demo_access_token
from tests.demo_mode.steps.rest import download_rest_file
from tests.demo_mode.utils.commands import DemoCommands


def test_comprehensive_example(
    release: str,
    demo_commands: DemoCommands,
) -> None:
    demo_space_id = "cb274b2b8bb1750d9be37dd4a3eb7014chb175"
    expected_file_content = b"hello world\\n"
    command_output = run_comprehensive_example(demo_commands)
    environment = guide_environment(oneprovider_count=1)
    onezone = environment.onezone
    assert_onezone_configuration(onezone, release=release)
    file_name = get_comprehensive_example_file_name(command_output)
    provider = environment.oneproviders[0]
    access_token = get_demo_access_token(provider, demo_commands)
    downloaded_content = download_rest_file(
        provider,
        space_id=demo_space_id,
        file_name=file_name,
        access_token=access_token,
    )
    assert downloaded_content == expected_file_content, (
        f"{provider.container} returned {downloaded_content!r}, expected {expected_file_content!r}"
    )
