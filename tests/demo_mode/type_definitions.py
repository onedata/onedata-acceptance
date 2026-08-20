"""Data types shared by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class PersistentService:
    """A persistent demo-mode service and its Docker container."""

    container_name: str
    process: subprocess.Popen[str]


@dataclass(frozen=True)
class PersistentState:
    """Demo-mode state expected to survive an environment restart."""

    access_token: str
    provider_id: str
    space_id: str
    file_name: str
