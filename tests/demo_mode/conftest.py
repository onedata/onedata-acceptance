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

from tests.demo_mode.utils.common import remove_demo_containers
from tests.demo_mode.utils.persistence import (
    prepare_demo_persistence,
    remove_demo_persistence,
)


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
def suppress_unverified_https_warning() -> Iterator[None]:
    """Suppress the expected warning for demo services' self-signed certificates."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InsecureRequestWarning)
        yield


@pytest.fixture(autouse=True)
def cleanup_demo_containers(request: pytest.FixtureRequest) -> None:
    remove_demo_containers()
    request.addfinalizer(remove_demo_containers)
    print(flush=True)


@pytest.fixture
def isolated_persistence_directories(
    request: pytest.FixtureRequest,
) -> None:
    """Own and clean the fixed host paths used by persistence commands."""
    request.addfinalizer(remove_demo_persistence)
    prepare_demo_persistence()
