"""Persistence-directory lifecycle helpers for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from functools import partial
from pathlib import Path
from shutil import rmtree
from typing import Final

import pytest

from tests.demo_mode.type_definitions import PersistentService
from tests.demo_mode.utils.commands import (
    load_command,
    start_command,
    stop_command,
    wait_for_successful_command,
)
from tests.utils.docker_utils import remove_containers

HOST_TMP_ENVIRONMENT_VARIABLE: Final = "DEMO_MODE_HOST_TMP"
PERSISTENCE_DIRECTORY_NAMES: Final = ("oz-pers", "op-pers", "op-storage")
OWNERSHIP_MARKER_NAME: Final = ".onedata-demo-mode-persistence-test-owned"
OWNERSHIP_MARKER_CONTENT: Final = "onedata-demo-mode-persistence-test-v1\n"


def run_persistent_service(
    command_path: str,
    await_command_path: str,
    release: str,
    container_name: str,
    request: pytest.FixtureRequest,
) -> PersistentService:
    """Start a persistent service and register its command for cleanup."""
    command = load_command(command_path, release)
    process = start_command(command, command_path)
    request.addfinalizer(partial(stop_command, process))
    wait_for_successful_command(
        load_command(await_command_path, release),
        await_command_path,
    )

    return PersistentService(container_name=container_name, process=process)


def _host_tmp_path() -> Path:
    return Path(os.environ.get(HOST_TMP_ENVIRONMENT_VARIABLE, "/tmp"))


def _persistence_paths() -> tuple[Path, ...]:
    host_tmp_path = _host_tmp_path()
    return tuple(host_tmp_path / name for name in PERSISTENCE_DIRECTORY_NAMES)


def _path_exists(path: Path) -> bool:
    """Return whether a path or symlink exists, including a broken symlink."""
    return os.path.lexists(path)


def _is_valid_ownership_marker(marker: Path) -> bool:
    return (
        marker.is_file()
        and not marker.is_symlink()
        and marker.read_text(encoding="utf-8") == OWNERSHIP_MARKER_CONTENT
    )


def _get_unowned_paths(existing_paths: list[Path]) -> list[Path]:
    return [path for path in existing_paths if not path.is_dir() or path.is_symlink()]


def _assert_and_get_test_owns_existing_paths() -> tuple[list[Path], Path, bool]:
    marker = _host_tmp_path() / OWNERSHIP_MARKER_NAME
    marker_exists = _path_exists(marker)
    existing_paths = [path for path in _persistence_paths() if _path_exists(path)]

    if marker_exists:
        if not _is_valid_ownership_marker(marker):
            raise AssertionError(
                f"Invalid demo-mode persistence test ownership marker: {marker}"
            )
    elif existing_paths:
        formatted_paths = ", ".join(str(path) for path in existing_paths)
        raise AssertionError(
            "Refusing to remove demo-mode persistence paths not owned by the test: "
            f"{formatted_paths}"
        )

    unowned_paths = _get_unowned_paths(existing_paths)
    if unowned_paths:
        formatted_paths = ", ".join(str(path) for path in unowned_paths)
        raise AssertionError(
            "Refusing to remove demo-mode persistence paths not owned by the test: "
            f"{formatted_paths}"
        )

    return existing_paths, marker, marker_exists


def _remove_persistence_paths_and_marker(
    existing_paths: list[Path],
    marker: Path,
    marker_exists: bool,
) -> None:
    for path in existing_paths:
        rmtree(path)
    if marker_exists:
        marker.unlink()


def remove_demo_persistence(container_names: list[str]) -> None:
    """Remove containers and all bind-mounted state owned by the persistence test."""
    remove_containers(container_names)
    existing_paths, marker, marker_exists = _assert_and_get_test_owns_existing_paths()
    _remove_persistence_paths_and_marker(existing_paths, marker, marker_exists)

    remaining_paths = [path for path in _persistence_paths() if _path_exists(path)]
    if _path_exists(marker):
        remaining_paths.append(marker)
    assert not remaining_paths, (
        "Demo-mode persistence paths remain after cleanup: "
        f"{', '.join(str(path) for path in remaining_paths)}"
    )


def prepare_demo_persistence(container_names: list[str]) -> None:
    """Reserve the clean fixed host paths used by persistence commands."""
    remove_demo_persistence(container_names)
    marker = _host_tmp_path() / OWNERSHIP_MARKER_NAME
    marker.write_text(OWNERSHIP_MARKER_CONTENT, encoding="utf-8")
