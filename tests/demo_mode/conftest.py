"""Pytest configuration for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import warnings
from collections.abc import Iterator
from typing import cast

import pytest
from _pytest.config.argparsing import Parser
from urllib3.exceptions import InsecureRequestWarning

from tests.demo_mode.constants import CONTAINER_NAMES
from tests.demo_mode.utils.logging import command_logs_for_test
from tests.demo_mode.utils.persistence import (
    prepare_demo_persistence,
    remove_demo_persistence,
)
from tests.utils.docker_utils import remove_containers


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--release",
        required=True,
        help="Onedata Docker image release, for example 25.1",
    )


@pytest.fixture
def release(request: pytest.FixtureRequest) -> str:
    return cast(str, request.config.getoption("release"))


@pytest.fixture(autouse=True)
def command_log_directory(request: pytest.FixtureRequest) -> Iterator[None]:
    test_name = request.node.name.removeprefix("test_")
    with command_logs_for_test(test_name):
        yield


@pytest.fixture(autouse=True)
def suppress_unverified_https_warning() -> Iterator[None]:
    """Suppress the expected warning for demo services' self-signed certificates."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InsecureRequestWarning)
        yield


@pytest.fixture(autouse=True)
def cleanup_demo_containers() -> Iterator[None]:
    remove_containers(CONTAINER_NAMES)
    print(flush=True)
    try:
        yield
    finally:
        remove_containers(CONTAINER_NAMES)


@pytest.fixture
def isolated_persistence_directories() -> Iterator[None]:
    """Own and clean the fixed host paths used by persistence commands."""
    try:
        prepare_demo_persistence()
        yield
    finally:
        remove_demo_persistence()
