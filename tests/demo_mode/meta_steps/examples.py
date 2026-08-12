"""Composite assertions for demo-mode examples."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.steps.examples import (
    assert_comprehensive_example_file_name,
    assert_comprehensive_example_message_contains_file_name,
    assert_comprehensive_example_success_message_count,
)
from tests.demo_mode.steps.rest import (
    assert_rest_file_content,
    get_demo_access_token,
)


def get_comprehensive_example_file_name(command_output: str) -> str:
    """Extract the validated filename from comprehensive-example output."""
    output_lines = [
        line
        for line in command_output.splitlines()
        if line.startswith("All done! Created a file called ")
    ]
    assert_comprehensive_example_success_message_count(output_lines, command_output)

    message = output_lines[0]
    message_parts = message.split('"')
    assert_comprehensive_example_message_contains_file_name(message, message_parts)

    file_name = message_parts[1]
    assert_comprehensive_example_file_name(file_name)
    return file_name


def assert_comprehensive_example(
    release: str,
    command_output: str,
    provider_container: str,
) -> None:
    """Assert the file created by the comprehensive example."""
    file_name = get_comprehensive_example_file_name(command_output)
    access_token = get_demo_access_token(release)
    assert_rest_file_content(
        provider_container,
        access_token,
        "cb274b2b8bb1750d9be37dd4a3eb7014chb175",
        file_name,
        b"hello world\\n",
    )
