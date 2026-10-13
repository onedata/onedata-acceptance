"""Pytest configuration for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import warnings
from collections.abc import Iterator

import pytest
from _pytest.config.argparsing import Parser
from urllib3.exceptions import InsecureRequestWarning

from bamboos.docker.environment.docker import pull_image_with_retries
from bamboos.docker.images_branch_config import resolve_image
from tests.demo_mode.constants import (
    CONTAINER_NAMES,
    CONTAINER_REMOVAL_TIMEOUT,
    PROCESS_EXIT_TIMEOUT,
)
from tests.demo_mode.type_definitions import DemoImages
from tests.demo_mode.utils.command_context import command_context
from tests.demo_mode.utils.persistence import (
    prepare_demo_persistence,
    remove_demo_persistence,
)
from tests.utils.docker_utils import remove_containers


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--onezone-image",
        help="Onezone image; defaults to the image resolved from branchConfig.yaml",
    )
    parser.addoption(
        "--oneprovider-image",
        help="Oneprovider image; defaults to the image resolved from branchConfig.yaml",
    )


def _select_image(override: object, service: str) -> str:
    image = override or resolve_image(service)
    if not isinstance(image, str) or not image:
        raise RuntimeError(f"No Docker image configured for {service}")
    return image


@pytest.fixture(scope="session")
def demo_images(request: pytest.FixtureRequest) -> DemoImages:
    """Resolve and pull the service images once for the whole test session."""
    images = DemoImages(
        onezone=_select_image(request.config.getoption("--onezone-image"), "onezone"),
        oneprovider=_select_image(
            request.config.getoption("--oneprovider-image"),
            "oneprovider",
        ),
    )

    for service, image in (
        ("onezone", images.onezone),
        ("oneprovider", images.oneprovider),
    ):
        print(f"\n[INFO] Using image {image} for service {service}")
        pull_image_with_retries(image)

    return images


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
    demo_images: DemoImages,
) -> Iterator[None]:
    remove_containers(CONTAINER_NAMES, timeout=CONTAINER_REMOVAL_TIMEOUT)

    with command_context(request.node.name, demo_images) as context:
        try:
            yield
        finally:
            try:
                remove_containers(CONTAINER_NAMES, timeout=CONTAINER_REMOVAL_TIMEOUT)
            finally:
                context.reap_processes(PROCESS_EXIT_TIMEOUT)
