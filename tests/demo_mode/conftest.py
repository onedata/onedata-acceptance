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

from tests.demo_mode.constants import (
    CONTAINER_NAMES,
    CONTAINER_REMOVAL_TIMEOUT,
    PROCESS_EXIT_TIMEOUT,
)
from tests.demo_mode.utils.command_context import command_context
from tests.demo_mode.utils.commands import DemoCommands
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


@pytest.fixture
def demo_commands() -> DemoCommands:
    return DemoCommands()


@pytest.fixture(autouse=True)
def suppress_unverified_https_warning() -> Iterator[None]:
    """Suppress the expected warning for demo services' self-signed certificates."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InsecureRequestWarning)
        yield


@pytest.fixture
def isolated_persistence_directories() -> Iterator[None]:
    """Own and clean the fixed host paths used by persistence commands."""
    try:
        prepare_demo_persistence()
        yield
    finally:
        remove_demo_persistence()


@pytest.fixture(autouse=True)
def demo_test_context(
    request: pytest.FixtureRequest,
    release: str,
) -> Iterator[None]:
    remove_containers(CONTAINER_NAMES, timeout=CONTAINER_REMOVAL_TIMEOUT)

    with command_context(request.node.name, release) as context:
        try:
            yield
        finally:
            try:
                remove_containers(CONTAINER_NAMES, timeout=CONTAINER_REMOVAL_TIMEOUT)
            finally:
                context.reap_processes(PROCESS_EXIT_TIMEOUT)
