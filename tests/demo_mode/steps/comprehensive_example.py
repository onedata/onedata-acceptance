"""Steps for running the comprehensive demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.constants import EXAMPLE_TIMEOUT
from tests.demo_mode.utils.commands import RUN_COMPREHENSIVE_EXAMPLE
from tests.demo_mode.utils.logging import log_step


@log_step("Running comprehensive example")
def run_comprehensive_example(timeout: float = EXAMPLE_TIMEOUT) -> str:
    """Run the comprehensive example command and return its output."""
    return RUN_COMPREHENSIVE_EXAMPLE.run(timeout=timeout)
