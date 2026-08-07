"""Common helpers for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

from tests.utils.docker_utils import remove_container

ONEZONE_CONTAINER_NAME: Final = "oz_test"
FIRST_ONEPROVIDER_CONTAINER_NAME: Final = "op_test1"
SECOND_ONEPROVIDER_CONTAINER_NAME: Final = "op_test2"
DEMO_CONTAINER_NAMES: Final = (
    FIRST_ONEPROVIDER_CONTAINER_NAME,
    SECOND_ONEPROVIDER_CONTAINER_NAME,
    ONEZONE_CONTAINER_NAME,
)


def remove_demo_containers() -> None:
    """Remove containers left by a current or interrupted demo-mode test."""
    for container_name in DEMO_CONTAINER_NAMES:
        remove_container(container_name)
