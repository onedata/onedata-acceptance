"""Command template helpers for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from pathlib import Path
from typing import Final

DEMO_MODE_ROOT: Final = Path(__file__).resolve().parents[1]
COMMANDS_ROOT: Final = DEMO_MODE_ROOT / "commands"
RELEASE_PLACEHOLDER: Final = "xRELEASExVERSIONx"
CONTAINER_NAME_PLACEHOLDER: Final = "xCONTAINERxNAMEx"


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


def load_command(relative_path: str, release: str) -> str:
    """Load a command verbatim, replacing only its release placeholder."""
    return (
        command_path(relative_path)
        .read_text(encoding="utf-8")
        .replace(RELEASE_PLACEHOLDER, release)
    )


def substitute_container_name(command: str, container_name: str) -> str:
    """Insert a Docker container name into a command."""
    return command.replace(CONTAINER_NAME_PLACEHOLDER, container_name)
