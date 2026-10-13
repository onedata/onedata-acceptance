"""Data types shared by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class DemoImages:
    """Docker images selected for a demo-mode test session."""

    onezone: str
    oneprovider: str


@dataclass(frozen=True)
class DemoService:
    """A demo-mode service, its Docker container, and optional launcher process."""

    container: str
    process: subprocess.Popen[str] | None = None


@dataclass(frozen=True)
class Onezone(DemoService):
    """Onezone service in a demo-mode environment."""


@dataclass(frozen=True)
class Oneprovider(DemoService):
    """Oneprovider service in a demo-mode environment."""


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
    file_content: bytes
