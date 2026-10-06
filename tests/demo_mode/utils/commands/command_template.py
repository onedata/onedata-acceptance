"""Rendering of demo-mode command script templates."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from dataclasses import dataclass
from pathlib import Path

from tests.demo_mode.utils.command_context import current_command_context
from tests.demo_mode.utils.commands.command import Command
from tests.demo_mode.utils.commands.helpers import (
    CONTAINER_NAME_PLACEHOLDER,
    DEMO_MODE_ROOT,
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

    def bind(
        self,
        *,
        container: str | None = None,
        cwd: Path = DEMO_MODE_ROOT,
    ) -> Command:
        """Load the command and substitute values required by its template."""
        context = current_command_context()
        command = self.path.read_text(encoding="utf-8")

        if RELEASE_PLACEHOLDER in command:
            command = command.replace(RELEASE_PLACEHOLDER, context.release)

        if CONTAINER_NAME_PLACEHOLDER in command:
            if container is None:
                raise ValueError(f"Command {self.relative_path!r} requires a container name")
            command = command.replace(CONTAINER_NAME_PLACEHOLDER, container)

        return Command(command, self.relative_path, cwd)
