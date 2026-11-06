"""Start demo-mode pytest with access to Docker but as the host user.

The runner starts as root only to join the Docker socket's group. Before
executing pytest, it prepares a writable home outside the read-only repository
and drops to the host UID and GID. As a result, bind-mounted logs, reports, and
persistence directories are not left owned by root on the host.
"""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import sys
from typing import Final, NoReturn

HOST_UID_ENV: Final = "DEMO_MODE_HOST_UID"
HOST_GID_ENV: Final = "DEMO_MODE_HOST_GID"
DOCKER_SOCKET: Final = "/var/run/docker.sock"
RUNNER_HOME: Final = "/tmp/demo-mode-test-runner"


def main() -> NoReturn:
    """Prepare Docker access, drop root privileges, and replace the runner with pytest."""
    host_uid = _read_host_id(HOST_UID_ENV)
    host_gid = _read_host_id(HOST_GID_ENV)
    docker_gid = os.stat(DOCKER_SOCKET).st_gid

    _prepare_runner_home(host_uid, host_gid)
    os.setgroups([docker_gid])
    os.setregid(host_gid, host_gid)
    os.setreuid(host_uid, host_uid)
    os.execv(
        sys.executable,
        [sys.executable, "-m", "pytest", *sys.argv[1:]],
    )


def _read_host_id(variable: str) -> int:
    try:
        return int(os.environ.pop(variable))
    except KeyError as error:
        raise RuntimeError(f"Required environment variable {variable} is not set") from error


def _prepare_runner_home(host_uid: int, host_gid: int) -> None:
    os.makedirs(RUNNER_HOME, exist_ok=True)
    os.chown(RUNNER_HOME, host_uid, host_gid)
    os.environ["HOME"] = RUNNER_HOME


if __name__ == "__main__":
    main()
