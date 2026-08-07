"""Pytest configuration for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import cast

import pytest
from _pytest.config.argparsing import Parser

from tests.demo_mode.utils.commands import remove_demo_containers


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
def cleanup_demo_containers(request: pytest.FixtureRequest) -> None:
    remove_demo_containers()
    request.addfinalizer(remove_demo_containers)
    print(flush=True)
