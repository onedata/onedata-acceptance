"""Composite steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess

import pytest

from tests.demo_mode.steps.environment import (
    run_oneprovider,
    run_onezone,
    run_second_oneprovider,
)


def run_onezone_with_oneprovider(
    release: str,
    provider_container: str,
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    """Start Onezone and one Oneprovider and wait until they are ready."""
    onezone_process = run_onezone(release, request)
    run_oneprovider(
        release,
        onezone_process,
        provider_container,
        request,
    )
    return onezone_process


def run_onezone_with_two_oneproviders(
    release: str,
    first_provider_container: str,
    second_provider_container: str,
    request: pytest.FixtureRequest,
) -> None:
    """Start Onezone and two Oneproviders and wait until they are ready."""
    onezone_process = run_onezone_with_oneprovider(
        release,
        first_provider_container,
        request,
    )
    run_second_oneprovider(
        release,
        onezone_process,
        second_provider_container,
        request,
    )
