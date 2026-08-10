"""Logical steps used by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial
from shlex import quote
from shutil import rmtree
from typing import Final

import pytest

from tests.demo_mode.utils.commands import (
    DEMO_MODE_ROOT,
    command_path,
    get_access_token,
    load_command,
    run_command,
    start_command,
    stop_command,
    wait_for_successful_command,
)
from tests.demo_mode.utils.common import (
    SECOND_ONEPROVIDER_CONTAINER_NAME,
)
from tests.demo_mode.utils.logging import (
    log_running_command,
    log_step_done,
    log_step_start,
)
from tests.demo_mode.utils.rest import (
    create_and_support_space,
    download_and_remove_file,
    get_oneprovider_configuration,
    get_onezone_configuration,
    get_provider_supported_space_ids,
    upload_and_download_file,
)

PYTHON_ACCESS_VENV: Final = DEMO_MODE_ROOT / "venv"


def run_onezone(release: str, request: pytest.FixtureRequest) -> subprocess.Popen[str]:
    """Start Onezone and wait until it is ready."""
    description = "Running Onezone"
    log_step_start(description)

    command = load_command("run_in_foreground/run_onezone.sh", release)
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))

    await_command = load_command(
        "run_in_background/await_onezone.sh",
        release,
    )
    wait_for_successful_command(await_command)

    log_step_done(description)
    return process


def run_oneprovider(
    release: str,
    onezone_process: subprocess.Popen[str],
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    """Start Oneprovider and wait until it is ready."""
    description = "Running Oneprovider"
    log_step_start(description)

    if onezone_process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")

    command = load_command("run_in_foreground/run_oneprovider.sh", release)
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))

    await_command = load_command(
        "run_in_background/await_oneprovider.sh",
        release,
    )
    wait_for_successful_command(await_command)

    log_step_done(description)
    return process


def run_second_oneprovider(
    release: str,
    onezone_process: subprocess.Popen[str],
    first_oneprovider_process: subprocess.Popen[str],
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    """Start the second Oneprovider and wait until it is ready."""
    description = "Running second Oneprovider"
    log_step_start(description)

    if onezone_process.poll() is not None:
        raise AssertionError("Onezone stopped before the second Oneprovider startup")
    if first_oneprovider_process.poll() is not None:
        raise AssertionError("First Oneprovider stopped before its peer startup")

    command = load_command(
        "distributed_environment/run_second_oneprovider.sh",
        release,
    )
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))

    wait_for_successful_command(
        f"docker exec {SECOND_ONEPROVIDER_CONTAINER_NAME} await-demo"
    )

    log_step_done(description)
    return process


def _run_background_command(command: str, timeout: float = 480) -> None:
    log_running_command(command)
    result = run_command(command, timeout=timeout, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(
            f"Background command failed with exit code {result.returncode}:\n"
            f"{command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def run_onezone_in_background(release: str) -> None:
    """Start Onezone in detached mode and actively wait until it is ready."""
    description = "Running Onezone in background"
    log_step_start(description)

    command = load_command("run_in_background/run_onezone.sh", release)
    _run_background_command(command)

    await_command = load_command(
        "run_in_background/await_onezone.sh",
        release,
    )
    wait_for_successful_command(await_command)

    log_step_done(description)


def run_oneprovider_in_background(release: str) -> None:
    """Start Oneprovider in detached mode and actively wait until it is ready."""
    description = "Running Oneprovider in background"
    log_step_start(description)

    command = load_command("run_in_background/run_oneprovider.sh", release)
    _run_background_command(command)

    await_command = load_command(
        "run_in_background/await_oneprovider.sh",
        release,
    )
    wait_for_successful_command(await_command)

    log_step_done(description)


def run_comprehensive_example(release: str, timeout: float = 480) -> str:
    """Run the comprehensive example command and return its output."""
    description = "Running comprehensive example"
    log_step_start(description)

    command = load_command("comprehensive_example/example.sh", release)
    log_running_command(command)
    try:
        result = run_command(command, timeout=timeout, capture_output=True)
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"Comprehensive example did not finish within {timeout}s"
        ) from error
    assert result.returncode == 0, (
        "Comprehensive example failed with exit code "
        f"{result.returncode}:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    log_step_done(description)
    return result.stdout


def _remove_python_access_environment() -> None:
    rmtree(PYTHON_ACCESS_VENV, ignore_errors=True)


def run_python_access_example(
    request: pytest.FixtureRequest,
    timeout: float = 480,
) -> str:
    """Prepare and run the Python access example in its generated venv."""
    description = "Running Python access example"
    log_step_start(description)

    request.addfinalizer(_remove_python_access_environment)
    _remove_python_access_environment()

    setup_script = command_path("python_access/setup_environment.sh")
    access_script = command_path("python_access/check_python_access.py")
    python = PYTHON_ACCESS_VENV / "bin" / "python"
    command = "\n".join(
        (
            "set -e",
            f"source {quote(str(setup_script))} > /dev/null",
            f"{quote(str(python))} {quote(str(access_script))}",
        )
    )
    log_running_command(command)
    try:
        result = run_command(command, timeout=timeout, capture_output=True)
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"Python access example did not finish within {timeout}s"
        ) from error
    assert result.returncode == 0, (
        "Python access example failed with exit code "
        f"{result.returncode}:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    log_step_done(description)
    return result.stdout


def assert_onezone_configuration(release: str) -> None:
    """Assert that Onezone exposes a valid public REST configuration."""
    description = "Asserting Onezone configuration"
    log_step_start(description)

    onezone_configuration = get_onezone_configuration()
    onezone_name = onezone_configuration.get("name")
    onezone_version = onezone_configuration.get("version")
    assert (
        isinstance(onezone_name, str) and onezone_name
    ), f"Expected a non-empty Onezone name, got {onezone_name!r}"
    assert (
        onezone_version == release
    ), f"Expected Onezone version {release!r}, got {onezone_version!r}"

    log_step_done(description)


def get_demo_access_token(release: str) -> str:
    """Get the access token exposed by the demo environment."""
    description = "Getting demo access token"
    log_step_start(description)

    access_token = get_access_token(release)
    log_step_done(description)
    return access_token


def get_comprehensive_example_file_name(command_output: str) -> str:
    """Extract the created filename from comprehensive-example output."""
    description = "Checking comprehensive example output"
    log_step_start(description)

    output_lines = [
        line
        for line in command_output.splitlines()
        if line.startswith("All done! Created a file called ")
    ]
    assert len(output_lines) == 1, (
        "Expected one comprehensive-example success message, got "
        f"{output_lines!r} in output:\n{command_output}"
    )
    message_parts = output_lines[0].split('"')
    assert (
        len(message_parts) >= 3
    ), f"Could not extract a filename from: {output_lines[0]!r}"
    file_name = message_parts[1]
    assert file_name.endswith(
        ".txt"
    ), f"Expected comprehensive example to create a .txt file, got {file_name!r}"

    log_step_done(description)
    return file_name


def assert_rest_file_content(
    provider_container: str,
    access_token: str,
    space_id: str,
    file_name: str,
    expected_content: bytes,
) -> None:
    """Download, verify, and remove an existing file through REST."""
    description = f"Checking {file_name} through {provider_container}"
    log_step_start(description)

    downloaded_content = download_and_remove_file(
        provider_container,
        access_token,
        space_id,
        file_name,
    )
    assert downloaded_content == expected_content, (
        f"{provider_container} returned {downloaded_content!r}, "
        f"expected {expected_content!r}"
    )

    log_step_done(description)


def _get_oneprovider_id(provider_container: str, release: str) -> str:
    configuration = get_oneprovider_configuration(provider_container)
    provider_id = configuration.get("providerId")
    provider_version = configuration.get("version")
    assert isinstance(provider_id, str) and provider_id, (
        f"Expected {provider_container} to expose a non-empty provider ID, "
        f"got {provider_id!r}"
    )
    assert (
        provider_version == release
    ), f"Expected {provider_container} version {release!r}, got {provider_version!r}"
    return provider_id


def assert_file_contents_are_distinct(
    first_file_content: bytes,
    second_file_content: bytes,
) -> None:
    """Assert that distributed providers are tested with different data."""
    description = "Asserting distributed file contents differ"
    log_step_start(description)

    assert (
        first_file_content != second_file_content
    ), "Distributed providers must be tested with different file contents"
    log_step_done(description)


def assert_oneproviders_are_distinct(
    first_provider_container: str,
    second_provider_container: str,
    release: str,
) -> None:
    """Assert that two containers expose distinct Oneprovider services."""
    description = "Asserting Oneproviders are distinct"
    log_step_start(description)

    first_provider_id = _get_oneprovider_id(
        first_provider_container,
        release,
    )
    second_provider_id = _get_oneprovider_id(
        second_provider_container,
        release,
    )
    assert (
        first_provider_id != second_provider_id
    ), f"Distributed Oneproviders expose the same ID: {first_provider_id}"
    log_step_done(description)


def create_space_for_provider(
    provider_container: str,
    space_name: str,
    access_token: str,
) -> str:
    """Create a space supported by the selected Oneprovider."""
    description = f"Creating space for {provider_container}"
    log_step_start(description)

    space_id = create_and_support_space(
        provider_container,
        space_name,
        access_token,
    )
    log_step_done(description)
    return space_id


def assert_space_support_is_isolated(
    first_provider_container: str,
    first_space_id: str,
    second_provider_container: str,
    second_space_id: str,
    access_token: str,
) -> None:
    """Assert that each provider exclusively supports its assigned space."""
    description = "Asserting provider space support is isolated"
    log_step_start(description)

    assert (
        first_space_id != second_space_id
    ), "Distributed providers unexpectedly use the same test space"
    first_provider_spaces = get_provider_supported_space_ids(
        first_provider_container,
        access_token,
    )
    second_provider_spaces = get_provider_supported_space_ids(
        second_provider_container,
        access_token,
    )
    assert (
        first_space_id in first_provider_spaces
    ), "First Oneprovider does not support its assigned test space"
    assert (
        first_space_id not in second_provider_spaces
    ), "Second Oneprovider unexpectedly supports the first provider's test space"
    assert (
        second_space_id in second_provider_spaces
    ), "Second Oneprovider does not support its assigned test space"
    assert (
        second_space_id not in first_provider_spaces
    ), "First Oneprovider unexpectedly supports the second provider's test space"
    log_step_done(description)


def assert_provider_rest_file_roundtrip(
    provider_container: str,
    access_token: str,
    file_content: bytes,
    space_id: str | None = None,
) -> None:
    """Assert a file upload and download through one provider."""
    description = f"Uploading and downloading a file through {provider_container}"
    log_step_start(description)

    downloaded_content = upload_and_download_file(
        access_token,
        file_content,
        provider_container,
        space_id,
    )
    assert downloaded_content == file_content, (
        f"{provider_container} returned {downloaded_content!r}, "
        f"expected {file_content!r}"
    )

    log_step_done(description)
