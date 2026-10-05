"""Shared helpers and constants for demo-mode REST clients."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

SPACE_SUPPORT_SIZE: Final = 1024**3
SPACE_APPEARANCE_TIMEOUT: Final = 60.0


def _authorization_headers(access_token: str) -> dict[str, str]:
    return {"X-Auth-Token": access_token}
