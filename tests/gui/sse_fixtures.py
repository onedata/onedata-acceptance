"""This module contains fixtures associated with sse events"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata.org"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest
import asyncio
import threading

from tests.mixed.utils.sse_utils import SpaceFilesMonitorClientImpl

from concurrent.futures._base import CancelledError


@pytest.fixture(scope="session")
def async_loop_in_thread():
    """
    Runs asyncio event loop in another thread,
    in order to run coroutines from sync code
    via asyncio.run_coroutine_threadsafe.
    """
    loop = asyncio.new_event_loop()

    def runner():
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


@pytest.fixture(scope="session")
def space_files_monitor(async_loop_in_thread) -> SpaceFilesMonitorClientImpl:
    """
    Fixture, which returns function responsible for creating and running monitor SSE
    """
    monitors: list[tuple[SpaceFilesMonitorClientImpl, asyncio.Future]] = []

    def start_monitor(
        *,
        oneprovider_url: str,
        space_id: str,
        token: str,
        observed_dirs: list[str],
        observed_attrs: list[str],
        ssl: bool = False,
    ) -> SpaceFilesMonitorClientImpl:
        monitor = SpaceFilesMonitorClientImpl(
            oneprovider_url=oneprovider_url,
            space_id=space_id,
            access_token=token,
            observed_dirs=observed_dirs,
            observed_attrs=observed_attrs,
            ssl=ssl,
        )
        # start monitor.run() in background
        fut = asyncio.run_coroutine_threadsafe(
            monitor.run(),
            async_loop_in_thread,
        )
        monitors.append((monitor, fut))
        return monitor

    # return to the test start_monitor
    yield start_monitor

    # teardown – clean monitors
    for monitor, fut in monitors:
        fut.cancel()
        # let event-loop handle CancelledError
        asyncio.run_coroutine_threadsafe(asyncio.sleep(0),
                                         async_loop_in_thread).result()
        try:
            fut.result(timeout=1)
        except CancelledError:
            pass
