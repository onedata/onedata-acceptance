"""Steps for running the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

from tests.demo_mode.utils.commands import CommandTemplate
from tests.demo_mode.utils.logging import log_step

MIN_FILENAME_MESSAGE_PARTS: Final = 3


@log_step("Running comprehensive example")
def run_comprehensive_example(release: str, timeout: float = 600) -> str:
    """Run the comprehensive example command and return its output."""
    command = CommandTemplate("comprehensive_example/example.sh", release)
    return command.run(timeout=timeout)


@log_step("Checking comprehensive example success message")
def assert_comprehensive_example_success_message_count(
    output_lines: list[str],
    command_output: str,
) -> None:
    """Assert that comprehensive-example output has one success message."""
    assert len(output_lines) == 1, (
        "Expected one comprehensive-example success message, got "
        f"{output_lines!r} in output:\n{command_output}"
    )


@log_step("Checking comprehensive example filename message")
def assert_comprehensive_example_message_contains_file_name(
    message: str,
    message_parts: list[str],
) -> None:
    """Assert that a comprehensive-example message contains a filename."""
    assert len(message_parts) >= MIN_FILENAME_MESSAGE_PARTS, (
        f"Could not extract a filename from: {message!r}"
    )


@log_step("Checking comprehensive example filename")
def assert_comprehensive_example_file_name(file_name: str) -> None:
    """Assert that the comprehensive example created a text file."""
    assert file_name.endswith(".txt"), (
        f"Expected comprehensive example to create a .txt file, got {file_name!r}"
    )
