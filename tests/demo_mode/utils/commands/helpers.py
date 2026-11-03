"""Low-level helpers for running demo-mode commands."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from pathlib import Path
from typing import Final

DEMO_MODE_ROOT: Final = Path(__file__).resolve().parents[2]
COMMANDS_ROOT: Final = DEMO_MODE_ROOT / "commands"
ONEZONE_IMAGE_PLACEHOLDER: Final = "xONEZONExIMAGEx"
ONEPROVIDER_IMAGE_PLACEHOLDER: Final = "xONEPROVIDERxIMAGEx"
CONTAINER_NAME_PLACEHOLDER: Final = "xCONTAINERxNAMEx"

PLACEHOLDER_PATTERN: Final = re.compile(r"x[A-Z][A-Z0-9]*(?:x[A-Z][A-Z0-9]*)*x")


def command_path(relative_path: str) -> Path:
    """Return a validated path to an unmodified file in ``commands``."""
    path = (COMMANDS_ROOT / relative_path).resolve()
    if not path.is_relative_to(COMMANDS_ROOT):
        raise ValueError(
            f"Command path must resolve within {COMMANDS_ROOT}, but "
            f"{relative_path!r} resolves to {path}"
        )

    if not path.is_file():
        raise FileNotFoundError(path)
    return path
