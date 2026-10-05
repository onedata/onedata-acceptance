"""Steps for running the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.logging import log_step


@log_step("Running comprehensive example")
def run_comprehensive_example(commands: DemoCommands, timeout: float = 600) -> str:
    """Run the comprehensive example command and return its output."""
    return commands.comprehensive_example().run(timeout=timeout)
