"""Constants shared by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final


def oneprovider_container(number: int) -> str:
    if number < 1:
        raise ValueError("Oneprovider number must be positive")
    return f"op_test{number}"


ONEZONE_NAME: Final = "Demo Onezone"
DEMO_SPACE_NAME: Final = "demo-space"
ONEZONE_CONTAINER: Final = "oz_test"
CONTAINER_NAMES: Final = (
    oneprovider_container(1),
    oneprovider_container(2),
    ONEZONE_CONTAINER,
)
