"""Data types shared by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from dataclasses import dataclass

from tests.demo_mode.utils.commands import Command, DemoCommands


@dataclass(frozen=True)
class RestEndpoint:
    """Host and port of a REST endpoint."""

    host: str
    port: int


@dataclass(frozen=True)
class DemoService:
    """A demo-mode service, its Docker container, and optional launcher process."""

    container: str
    process: subprocess.Popen[str] | None = None

    def stop_process(self, timeout: float = 10) -> None:
        """Stop the launcher process when this service has one."""
        if self.process is not None:
            Command.stop_process(self.process, timeout)


@dataclass(frozen=True)
class Onezone(DemoService):
    """Onezone service in a demo-mode environment."""


@dataclass(frozen=True)
class Oneprovider(DemoService):
    """Oneprovider service in a demo-mode environment."""

    def demo_access_token(self, commands: DemoCommands) -> str:
        """Return the access token exposed by the demo environment."""
        access_token = commands.access_token(self.container).run().strip()
        if not access_token:
            raise AssertionError("The access-token command returned an empty result")
        return access_token


@dataclass(frozen=True)
class DemoEnvironment:
    """Services that comprise one demo-mode environment."""

    onezone: Onezone
    oneproviders: tuple[Oneprovider, ...]


@dataclass(frozen=True)
class PersistentState:
    """Demo-mode state expected to survive an environment restart."""

    access_token: str
    provider_id: str
    space_id: str
    file_name: str
