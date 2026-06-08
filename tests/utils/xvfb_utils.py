"""This module implements utility functions for management of xvfb."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import errno
import fnmatch
import os
import subprocess as sp
import tempfile
import time
from itertools import chain
from typing import Any


def start_session(
    display: Any, screens: Any, screen_width: Any, screen_height: Any, screen_depth: Any
) -> Any:
    whd = f"{screen_width}x{screen_height}x{screen_depth}"
    cmd = ["Xvfb", "-br", "-nolisten", "tcp", f":{display}"]
    for screen in screens:
        cmd.extend(["-screen", str(screen), whd])

    with open(os.devnull, "w") as dev_null:
        proc = sp.Popen(  # pylint: disable=consider-using-with
            cmd, stdout=dev_null, stderr=dev_null, close_fds=True
        )

    # let Xvfb start
    time.sleep(0.5)
    if proc.poll() is not None:
        raise RuntimeError("Xvfb did not start")
    return proc


def stop_session(proc: Any) -> Any:
    try:
        proc.terminate()
        proc.wait()
    except IOError as ex:
        if ex.errno not in (errno.EINVAL, errno.EPIPE):
            raise


def find_free_display(min_display_num: Any = 1005) -> Any:
    tmp_dir = tempfile.gettempdir()
    lock_files = fnmatch.filter(os.listdir(tmp_dir), ".X*-lock")
    displays_in_use = (
        int(name.split("X")[1].split("-")[0])
        for name in lock_files
        if os.path.isfile(os.path.join(tmp_dir, name))
    )
    return max(chain([min_display_num], displays_in_use)) + 1
