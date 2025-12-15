"""This module contains fixtures associated with sse events"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata (onedata.org)"
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
def monitors() -> list[tuple[SpaceFilesMonitorClientImpl, asyncio.Future]]:
    return []


@pytest.fixture(scope="session")
def space_files_monitor(async_loop_in_thread, monitors) -> SpaceFilesMonitorClientImpl:
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
        monitors.append((monitor, future))
        return monitor

    # return to the test start_monitor
    yield start_monitor

    # teardown – clean monitors
    for monitor, future in monitors:
        future.cancel()
        # Give the event loop one tick so the cancelled task can process its
        # CancelledError and finish cleanly before we call future.result()
        asyncio.run_coroutine_threadsafe(
            asyncio.sleep(0), async_loop_in_thread).result()
        try:
            future.result(timeout=1)
        except CancelledError:
            pass
