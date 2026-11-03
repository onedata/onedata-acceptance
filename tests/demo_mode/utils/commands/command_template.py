"""Rendering of demo-mode command script templates."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from tests.demo_mode.constants import SHORT_COMMAND_TIMEOUT
from tests.demo_mode.utils.command_context import current_command_context
from tests.demo_mode.utils.commands.command import Command

_COMMANDS_ROOT: Final = Path(__file__).resolve().parents[2] / "commands"
_ONEZONE_IMAGE_PLACEHOLDER: Final = "xONEZONExIMAGEx"
_ONEPROVIDER_IMAGE_PLACEHOLDER: Final = "xONEPROVIDERxIMAGEx"
_CONTAINER_NAME_PLACEHOLDER: Final = "xCONTAINERxNAMEx"
_PLACEHOLDER_PATTERN: Final = re.compile(r"x[A-Z][A-Z0-9]*(?:x[A-Z][A-Z0-9]*)*x")


@dataclass(frozen=True)
class CommandTemplate:
    """A command script whose image and container placeholders are rendered."""

    relative_path: str

    @property
    def path(self) -> Path:
        """Return the validated path of this command script."""
        return command_path(self.relative_path)

    def render(self, container: str | None = None) -> str:
        """Render and validate all placeholders using the active test context."""
        context = current_command_context()
        command = self.path.read_text(encoding="utf-8")

        requires_container = _CONTAINER_NAME_PLACEHOLDER in command

        if requires_container and container is None:
            raise ValueError(f"Command {self.relative_path!r} requires a container name")

        if not requires_container and container is not None:
            raise ValueError(f"Command {self.relative_path!r} does not accept a container name")

        command = command.replace(
            _ONEZONE_IMAGE_PLACEHOLDER,
            shlex.quote(context.images.onezone),
        )
        command = command.replace(
            _ONEPROVIDER_IMAGE_PLACEHOLDER,
            shlex.quote(context.images.oneprovider),
        )

        if container is not None:
            command = command.replace(_CONTAINER_NAME_PLACEHOLDER, container)

        remaining_placeholders = _PLACEHOLDER_PATTERN.findall(command)
        if remaining_placeholders:
            raise ValueError(
                f"Command {self.relative_path!r} contains unresolved placeholders: "
                f"{remaining_placeholders}"
            )

        return command

    def run(
        self,
        container: str | None = None,
        *,
        timeout: float = SHORT_COMMAND_TIMEOUT,
    ) -> str:
        """Render and run the command once, returning its stdout."""
        return self._bind(container=container).run(timeout=timeout)

    def start(
        self,
        container: str | None = None,
    ) -> subprocess.Popen[str]:
        """Render and start the command, registering its process for cleanup."""
        return self._bind(container=container).start()

    def run_until_success(
        self,
        container: str | None = None,
        *,
        timeout: float,
    ) -> str:
        """Render and retry, keeping all attempts in one command log."""
        return self._bind(container=container).run_until_success(timeout=timeout)

    def _bind(
        self,
        *,
        container: str | None = None,
    ) -> Command:
        """Render this template into a low-level executable command."""
        return Command(self.render(container), self.relative_path)


def command_path(relative_path: str) -> Path:
    """Return a validated path to an unmodified file in `commands`."""
    path = (_COMMANDS_ROOT / relative_path).resolve()
    if not path.is_relative_to(_COMMANDS_ROOT):
        raise ValueError(
            f"Command path must resolve within {_COMMANDS_ROOT}, but "
            f"{relative_path!r} resolves to {path}"
        )

    if not path.is_file():
        raise FileNotFoundError(path)
    return path
