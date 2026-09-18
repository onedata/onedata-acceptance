"""Composite steps for the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.steps.comprehensive_example import (
    assert_comprehensive_example_file_name,
    assert_comprehensive_example_message_contains_file_name,
    assert_comprehensive_example_success_message_count,
)


def get_comprehensive_example_file_name(command_output: str) -> str:
    """Extract the validated filename from comprehensive-example output."""
    success_message_prefix = "All done! Created a file called "
    output_lines = [
        line
        for line in command_output.splitlines()
        if line.startswith(success_message_prefix)
    ]
    assert_comprehensive_example_success_message_count(output_lines, command_output)

    message = output_lines[0]
    message_parts = message.split('"')
    assert_comprehensive_example_message_contains_file_name(message, message_parts)

    file_name = message_parts[1]
    assert_comprehensive_example_file_name(file_name)
    return file_name
