"""Constants shared by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final


def oneprovider_container(number: int) -> str:
    if number < 1:
        raise ValueError("Oneprovider number must be positive")
    return f"op_test{number}"


DEMO_SPACE_ID: Final = "cb274b2b8bb1750d9be37dd4a3eb7014chb175"
MAX_ONEPROVIDERS: Final = 2

PERSISTENCE_HOST_DIRS: Final = (
    "oz-pers",
    *(
        directory
        for number in range(1, MAX_ONEPROVIDERS + 1)
        for directory in (
            f"{oneprovider_container(number)}-pers",
            f"{oneprovider_container(number)}-storage",
        )
    ),
)

SPACE_SYNC_TIMEOUT: Final = 60
SERVICE_READY_TIMEOUT: Final = 600
EXAMPLE_TIMEOUT: Final = 600
SHORT_COMMAND_TIMEOUT: Final = 60
CONTAINER_REMOVAL_TIMEOUT: Final = 60
PROCESS_EXIT_TIMEOUT: Final = 10

ONEZONE_NAME: Final = "Demo Onezone"
DEMO_SPACE_NAME: Final = "demo-space"
ONEZONE_CONTAINER: Final = "oz_test"
CONTAINER_NAMES: Final = (
    ONEZONE_CONTAINER,
    *(oneprovider_container(number) for number in range(1, MAX_ONEPROVIDERS + 1)),
)
