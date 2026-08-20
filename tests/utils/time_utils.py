"""Helpers for timeout and retry timing."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from time import monotonic, sleep


def deadline_after(timeout: float) -> float:
    """Return a monotonic deadline after the given timeout."""
    return monotonic() + timeout


def remaining_time(deadline: float) -> float:
    """Return seconds remaining until a monotonic deadline."""
    return max(0, deadline - monotonic())


def sleep_before_retry(deadline: float, interval: float) -> None:
    """Sleep for a retry interval without passing the deadline."""
    sleep(min(interval, remaining_time(deadline)))
