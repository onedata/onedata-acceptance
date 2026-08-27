"""Common names, characters etc. used in all GUIs."""

from dataclasses import dataclass
from enum import Enum

__author__ = "Jakub Liput"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

# A character used to separate name from a fragment of unique ID of records
# that have the same name.
CONFLICT_NAME_SEPARATOR = "@"

# Default element lookup timeout in seconds; 0 disables Selenium's implicit wait.
SELENIUM_IMPLICIT_WAIT = 0

# use this const when using: WebDriverWait(selenium, WAIT_FRONTEND).until(lambda s: ...)
# when waiting for frontend changes
WAIT_FRONTEND = 4

# use this const when using: WebDriverWait(selenium, WAIT_BACKEND).until(lambda s: ...)
# when waiting for backend changes
WAIT_BACKEND = 15

# use this const when using: WebDriverWait(selenium, WAIT_NORMAL_UPLOAD).until(lambda s: ...)
# when waiting for normal uploads to finish
WAIT_NORMAL_UPLOAD = 90

# use this const when using: WebDriverWait(selenium, WAIT_EXTENDED_UPLOAD).until(lambda s: ...)
# when waiting for extended uploads to finish
WAIT_EXTENDED_UPLOAD = 600

# number of times tests will try to start Webdriver instance
DRIVER_CREATION_RETRIES = 5

# use when waiting for normal download to finish
WAIT_NORMAL_DOWNLOAD = 10

# use when waiting for workflow executions to finish
WAIT_NORMAL_WORKFLOW_EXECUTION = 360
WAIT_EXTENDED_WORKFLOW_EXECUTION = 1500

# use when waiting for pods to terminate
WAIT_PODS_TERMINATION = 180

NUMERALS = {
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


SCREEN_PARAMETERS: dict[str, int] = {
    "width": ScreenSize.LARGE.value.width,
    "height": ScreenSize.LARGE.value.height,
    "depth": 24,
}
