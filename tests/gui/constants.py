"""Common names, characters etc. used in all GUIs."""

from dataclasses import dataclass
from enum import Enum
from typing import Final

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

# A character used to separate name from a fragment of unique ID of records
# that have the same name.
CONFLICT_NAME_SEPARATOR: Final[str] = "@"

# Default element lookup timeout in seconds; 0 disables Selenium's implicit wait.
SELENIUM_IMPLICIT_WAIT: Final[float] = 0

# use this const when using: WebDriverWait(selenium, WAIT_FRONTEND).until(lambda s: ...)
# when waiting for frontend changes
WAIT_FRONTEND: Final[int] = 4

# use this const when using: WebDriverWait(selenium, WAIT_BACKEND).until(lambda s: ...)
# when waiting for backend changes
WAIT_BACKEND: Final[int] = 15

# use this const when using: WebDriverWait(selenium, WAIT_NORMAL_UPLOAD).until(lambda s: ...)
# when waiting for normal uploads to finish
WAIT_NORMAL_UPLOAD: Final[int] = 90

# use this const when using: WebDriverWait(selenium, WAIT_EXTENDED_UPLOAD).until(lambda s: ...)
# when waiting for extended uploads to finish
WAIT_EXTENDED_UPLOAD: Final[int] = 600

# number of times tests will try to start Webdriver instance
DRIVER_CREATION_RETRIES: Final[int] = 5

# use when waiting for normal download to finish
WAIT_NORMAL_DOWNLOAD: Final[int] = 10

# use when waiting for workflow executions to finish
WAIT_NORMAL_WORKFLOW_EXECUTION: Final[int] = 360
WAIT_EXTENDED_WORKFLOW_EXECUTION: Final[int] = 1500

# use when waiting for pods to terminate
WAIT_PODS_TERMINATION: Final[int] = 180

RESPONSIVE_LAYOUT_DELAY: Final[float] = 1.0

NUMERALS: Final[dict[str, int]] = {
    "first": 0,
    "second": 1,
    "third": 2,
    "fourth": 3,
    "fifth": 4,
    "sixth": 5,
    "seventh": 6,
    "eighth": 7,
    "ninth": 8,
    "tenth": 9,
    "last": -1,
}


@dataclass(frozen=True)
class WindowSize:
    width: int
    height: int


class ScreenSize(Enum):
    LARGE = WindowSize(width=1366, height=1024)
    MEDIUM = WindowSize(width=1024, height=768)
    SMALL = WindowSize(width=800, height=600)


SCREEN_PARAMETERS: Final[dict[str, int]] = {
    "width": ScreenSize.LARGE.value.width,
    "height": ScreenSize.LARGE.value.height,
    "depth": 24,
}
