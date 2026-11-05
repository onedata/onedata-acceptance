"""This module contains fixtures associated with sse events"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import asyncio
import threading
from collections.abc import Generator
from concurrent.futures import CancelledError, Future
from typing import NamedTuple, Protocol

import pytest

from tests.mixed.utils.sse_utils import SpaceFilesMonitorClientImpl


class StartMonitor(Protocol):
    def __call__(
        self,
        *,
        oneprovider_authority: str,
        space_id: str,
        token: str,
        observed_dirs: list[str],
        observed_attrs: list[str],
        verify_ssl: bool = False,
    ) -> SpaceFilesMonitorClientImpl: ...


class MonitorEntry(NamedTuple):
    monitor: SpaceFilesMonitorClientImpl
    # Future representing the background execution of monitor.run()
    # used for cancellation and graceful shutdown.
    future: Future[None]


@pytest.fixture(scope="function")
def async_loop_in_thread() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Runs asyncio event loop in another thread,
    in order to run coroutines from sync code
    via asyncio.run_coroutine_threadsafe.
    """
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

    def runner() -> None:
        asyncio.set_event_loop(loop)
        try:
            loop.run_forever()
        finally:
            loop.close()

    t = threading.Thread(target=runner, daemon=True)
    t.start()

    try:
        yield loop
    finally:
        loop.call_soon_threadsafe(loop.stop)
        t.join()


@pytest.fixture(scope="function")
def monitors() -> list[MonitorEntry]:
    return []


@pytest.fixture(scope="function")
def space_files_monitor_factory(
    async_loop_in_thread: asyncio.AbstractEventLoop,
    monitors: list[MonitorEntry],
) -> Generator[StartMonitor, None, None]:
    """
    Fixture, which returns function responsible for creating and running monitor SSE
    """

    def start_monitor(
        *,
        oneprovider_authority: str,
        space_id: str,
        token: str,
        observed_dirs: list[str],
        observed_attrs: list[str],
        verify_ssl: bool = False,
    ) -> SpaceFilesMonitorClientImpl:
        monitor = SpaceFilesMonitorClientImpl(
            oneprovider_authority=oneprovider_authority,
            space_id=space_id,
            access_token=token,
            observed_dirs=observed_dirs,
            observed_attrs=observed_attrs,
            verify_ssl=verify_ssl,
        )
        # start monitor.run() in background
        future = asyncio.run_coroutine_threadsafe(
            monitor.run(),
            async_loop_in_thread,
        )
        monitors.append(MonitorEntry(monitor=monitor, future=future))
        return monitor

    # return to the test start_monitor
    yield start_monitor

    # teardown – clean monitors
    for monitor, future in monitors:
        future.cancel()
        # Give the event loop one tick so the cancelled task can process its
        # CancelledError and finish cleanly before we call future.result()
        asyncio.run_coroutine_threadsafe(
            asyncio.sleep(0), async_loop_in_thread
        ).result()
        try:
            future.result(timeout=1)
        except CancelledError:
            pass
