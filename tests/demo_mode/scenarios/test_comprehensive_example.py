"""Tests for the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.constants import FIRST_ONEPROVIDER_CONTAINER, ONEZONE_CONTAINER
from tests.demo_mode.meta_steps.comprehensive_example import (
    get_comprehensive_example_file_name,
)
from tests.demo_mode.meta_steps.rest import assert_onezone_configuration
from tests.demo_mode.models import Oneprovider, Onezone
from tests.demo_mode.steps.comprehensive_example import run_comprehensive_example
from tests.demo_mode.steps.rest import download_rest_file
from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.rest import OneproviderRestClient, OnezoneRestClient


def test_comprehensive_example(
    release: str,
    demo_commands: DemoCommands,
) -> None:
    demo_space_id = "cb274b2b8bb1750d9be37dd4a3eb7014chb175"
    expected_file_content = b"hello world\\n"
    command_output = run_comprehensive_example(demo_commands)
    onezone = OnezoneRestClient(Onezone(ONEZONE_CONTAINER))
    assert_onezone_configuration(onezone, release=release)
    file_name = get_comprehensive_example_file_name(command_output)
    provider_service = Oneprovider(FIRST_ONEPROVIDER_CONTAINER)
    access_token = provider_service.demo_access_token()
    provider = OneproviderRestClient(provider_service, access_token)
    downloaded_content = download_rest_file(
        provider,
        space_id=demo_space_id,
        file_name=file_name,
    )
    assert downloaded_content == expected_file_content, (
        f"{provider.container} returned {downloaded_content!r}, expected {expected_file_content!r}"
    )
