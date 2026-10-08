"""Rendering of demo-mode command script templates."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from dataclasses import dataclass
from pathlib import Path

from tests.demo_mode.constants import SHORT_COMMAND_TIMEOUT
from tests.demo_mode.utils.command_context import current_command_context
from tests.demo_mode.utils.commands.command import Command
from tests.demo_mode.utils.commands.helpers import (
    CONTAINER_NAME_PLACEHOLDER,
    DEMO_MODE_ROOT,
    PLACEHOLDER_PATTERN,
    RELEASE_PLACEHOLDER,
    command_path,
)


@dataclass(frozen=True)
class CommandTemplate:
    """A command script whose release and container placeholders are rendered."""

    relative_path: str

    @property
    def path(self) -> Path:
        """Return the validated path of this command script."""
        return command_path(self.relative_path)

    def render(self, container: str | None = None) -> str:
        """Render and validate all placeholders using the active test context."""
        context = current_command_context()
        command = self.path.read_text(encoding="utf-8")

        requires_container = CONTAINER_NAME_PLACEHOLDER in command

        if requires_container and container is None:
            raise ValueError(f"Command {self.relative_path!r} requires a container name")

        if not requires_container and container is not None:
            raise ValueError(f"Command {self.relative_path!r} does not accept a container name")

        command = command.replace(RELEASE_PLACEHOLDER, context.release)

        if container is not None:
            command = command.replace(CONTAINER_NAME_PLACEHOLDER, container)

        remaining_placeholders = PLACEHOLDER_PATTERN.findall(command)
        if remaining_placeholders:
            raise ValueError(
                f"Command {self.relative_path!r} contains unresolved placeholders: "
                f"{remaining_placeholders}"
            )

        return command

    def _bind(
        self,
        *,
        container: str | None = None,
        cwd: Path = DEMO_MODE_ROOT,
    ) -> Command:
        """Render this template into a low-level executable command."""
        return Command(self.render(container), self.relative_path, cwd)

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
