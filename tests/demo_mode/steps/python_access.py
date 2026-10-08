"""Steps for running the Python-access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from pathlib import Path

from tests.demo_mode.constants import EXAMPLE_TIMEOUT
from tests.demo_mode.utils.command_context import current_command_context
from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.python_access import read_setup_log


@log_step("Running Python access example and checking the output")
def assert_python_access_example_output(
    commands: DemoCommands,
    *,
    expected_output: str,
    environment_root: Path,
    timeout: float = EXAMPLE_TIMEOUT,
) -> None:
    setup_log_path = current_command_context().logs_directory / "setup.log"
    command = commands.python_access(
        environment_root=environment_root,
        setup_log_path=setup_log_path,
    )
    try:
        actual_output = command.run(timeout=timeout)
    except AssertionError as error:
        setup_log = read_setup_log(setup_log_path)
        raise AssertionError(
            f"Python access example failed:\nsetup output:\n{setup_log}\n{error}"
        ) from error
    assert actual_output == expected_output, (
        f"Expected Python access output {expected_output!r}, got {actual_output!r}"
    )
