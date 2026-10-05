"""Composite steps for the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

MIN_FILENAME_MESSAGE_PARTS: Final = 3


def get_comprehensive_example_file_name(command_output: str) -> str:
    """Extract the validated filename from comprehensive-example output."""
    success_message_prefix = "All done! Created a file called "
    output_lines = [
        line for line in command_output.splitlines() if line.startswith(success_message_prefix)
    ]
    assert len(output_lines) == 1, (
        "Expected one comprehensive-example success message, got "
        f"{output_lines!r} in output:\n{command_output}"
    )

    message = output_lines[0]
    message_parts = message.split('"')
    assert len(message_parts) >= MIN_FILENAME_MESSAGE_PARTS, (
        f"Could not extract a filename from: {message!r}"
    )

    file_name = message_parts[1]
    assert file_name.endswith(".txt"), (
        f"Expected comprehensive example to create a .txt file, got {file_name!r}"
    )
    return file_name
