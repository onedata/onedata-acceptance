"""Steps for running the Python-access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.python_access import (
    prepare_python_access_directory,
    read_setup_log,
)


@log_step("Running Python access example")
def run_python_access_example(
    commands: DemoCommands,
    request: pytest.FixtureRequest,
    timeout: float = 600,
) -> str:
    """Prepare and run the Python access example in its generated venv."""
    environment_root = prepare_python_access_directory(request)
    setup_log_path = environment_root / "setup.log"
    command = commands.python_access(
        environment_root=environment_root,
        setup_log_path=setup_log_path,
    )
    try:
        return command.run(timeout=timeout)
    except AssertionError as error:
        setup_log = read_setup_log(setup_log_path)
        raise AssertionError(
            f"Python access example failed:\nsetup output:\n{setup_log}\n{error}"
        ) from error
