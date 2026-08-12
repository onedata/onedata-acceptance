"""Pytest configuration for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import warnings
from collections.abc import Iterator
from functools import partial
from typing import cast

import pytest
from _pytest.config.argparsing import Parser
from urllib3.exceptions import InsecureRequestWarning

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
def onezone_name() -> str:
    return "Demo Onezone"


@pytest.fixture
def demo_space_name() -> str:
    return "demo-space"


@pytest.fixture
def onezone_container_name() -> str:
    return "oz_test"


@pytest.fixture
def first_oneprovider_container_name() -> str:
    return "op_test1"


@pytest.fixture
def second_oneprovider_container_name() -> str:
    return "op_test2"


@pytest.fixture
def container_names(
    first_oneprovider_container_name: str,
    second_oneprovider_container_name: str,
    onezone_container_name: str,
) -> list[str]:
    return [
        first_oneprovider_container_name,
        second_oneprovider_container_name,
        onezone_container_name,
    ]


@pytest.fixture(autouse=True)
def suppress_unverified_https_warning() -> Iterator[None]:
    """Suppress the expected warning for demo services' self-signed certificates."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", InsecureRequestWarning)
        yield


@pytest.fixture(autouse=True)
def cleanup_demo_containers(
    request: pytest.FixtureRequest,
    container_names: list[str],
) -> None:
    remove_containers(container_names)
    request.addfinalizer(partial(remove_containers, container_names))
    print(flush=True)


@pytest.fixture
def isolated_persistence_directories(
    request: pytest.FixtureRequest,
    container_names: list[str],
) -> None:
    """Own and clean the fixed host paths used by persistence commands."""
    request.addfinalizer(partial(remove_demo_persistence, container_names))
    prepare_demo_persistence(container_names)
