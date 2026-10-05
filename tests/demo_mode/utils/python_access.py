"""Helpers for running the Python-access demo-mode example."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial
from pathlib import Path
from shutil import rmtree

import pytest


def prepare_python_access_directory(request: pytest.FixtureRequest) -> Path:
    """Create the temporary directory used by the Python-access example."""
    environment_root = Path("/tmp/demo-mode-python-access")
    if environment_root.exists():
        raise FileExistsError(f"Python access directory already exists: {environment_root}")
    environment_root.mkdir()
    request.addfinalizer(partial(rmtree, environment_root, ignore_errors=True))
    return environment_root


def read_setup_log(setup_log_path: Path) -> str:
    """Read the Python-access setup log, returning a fallback when absent."""
    if not setup_log_path.exists():
        return "Setup log was not created"

    return setup_log_path.read_text(encoding="utf-8", errors="replace")
