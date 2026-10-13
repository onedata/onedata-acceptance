"""Tests for the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.constants import DEMO_SPACE_ID
from tests.demo_mode.meta_steps.environment import guide_environment
from tests.demo_mode.steps.comprehensive_example import run_comprehensive_example
from tests.demo_mode.steps.environment import get_demo_access_token
from tests.demo_mode.steps.rest import assert_file_content
from tests.demo_mode.utils.comprehensive_example import (
    get_comprehensive_example_file_name,
)


def test_comprehensive_example() -> None:
    expected_file_content = b"hello world\\n"
    command_output = run_comprehensive_example()
    environment = guide_environment(oneprovider_count=1)
    (provider,) = environment.oneproviders
    access_token = get_demo_access_token(provider)
    file_name = get_comprehensive_example_file_name(command_output)
    assert_file_content(
        provider,
        space_id=DEMO_SPACE_ID,
        file_name=file_name,
        expected_content=expected_file_content,
        access_token=access_token,
    )
