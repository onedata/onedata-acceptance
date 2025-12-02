""" This module contains utils for handling sse (Server-Sent Events) """

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata.org"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import asyncio
import json
from abc import ABC, abstractmethod
from enum import Enum

from aiohttp_sse_client import client as sse_client # pylint: disable=import-error
from aiohttp_sse_client.client import MessageEvent # pylint: disable=import-error


class SSEEvent(Enum):
    CHANGEDORCREATED = "changedOrCreated"
    HEARTBEAT = "heartbeat"
    DELETED = "deleted"


class SpaceFilesMonitorClient(ABC): # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        oneprovider_url: str,
        space_id: str,
        access_token: str,
        observed_dirs: list[str],
        observed_attrs: list[str],
        ssl: bool = True,
    ):
        self.oneprovider_url = oneprovider_url.rstrip("/")
        self.space_id = space_id
        self.access_token = access_token
        self.observed_dirs = observed_dirs
        self.observed_attrs = observed_attrs
        self.ssl = ssl

        # fileId -> attrs
        self.files: dict[str, dict] = {}
        # fileId -> attrs
        self.deleted_files: dict[str, dict] = {}
        self.last_event_id: str | None = None

        self.created_events = asyncio.Queue()
        self.updated_events = asyncio.Queue()
        self.deleted_events = asyncio.Queue()

    # ======= PUBLIC ENTRYPOINT =======

    async def run(self):
        """
        Main loop
        """
        backoff = 1
        loop = asyncio.get_running_loop()
        while True:
            try:
                print("🔌 Connecting to SSE stream...")
                await self._consume_stream(reconnect=bool(self.last_event_id))
                backoff = 1
            except asyncio.CancelledError:
                break
            except Exception as e: # pylint: disable=broad-exception-caught
                if loop.is_closed() or not loop.is_running():
                    print(f"Loop is closed/running={loop.is_running()}, breaking run()")
                    break
                try:
                    print(f"Stream error: {e}\n Reconnect in {backoff} s")
                    await asyncio.sleep(backoff)
                except asyncio.CancelledError:
                    print("Cancelled during backoff sleep, shutting down")
                    break

                backoff = min(backoff * 2, 60)

    async def _consume_stream(self, reconnect: bool = False):
        url = f"{self.oneprovider_url}/api/v3/oneprovider/spaces/{self.space_id}/events/files"

        headers = {
            "X-Auth-Token": self.access_token,
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }

        if reconnect and self.last_event_id is not None:
            headers["Last-Event-Id"] = self.last_event_id

        body = {
            "observedDirectories": self.observed_dirs,
            "observedAttributes": self.observed_attrs,
        }

        async with sse_client.EventSource(
            url, option={"method": "POST"}, headers=headers, json=body, ssl=self.ssl
        ) as event_source:
            try:
                async for event in event_source:
                    await self._handle_event(event)
            except asyncio.CancelledError as e:
                print(f"Closing connection due to: {e}")
                raise
            except ConnectionError:
                pass

    async def _handle_event(self, event: MessageEvent):
        event_type = event.type
        data_raw = event.data

        self.last_event_id = event.last_event_id

        try:
            data: dict = json.loads(data_raw)
        except json.JSONDecodeError:
            print(f"Cannot decode data: {data_raw!r}")
            return

        if event_type == SSEEvent.HEARTBEAT.value:
            return
        if event_type == SSEEvent.CHANGEDORCREATED.value:
            await self._handle_changed_or_created(data)
        elif event_type == SSEEvent.DELETED.value:
            await self._handle_deleted(data)
        else:
            print(f"Unknown event type={event_type}, data={data}")

    async def _handle_changed_or_created(self, data: dict):
        file_id: str = data.get("fileId")
        parent_file_id: str = data.get("parentFileId")
        new_attrs: dict[str : str | int] = data.get("attributes", {})

        if not file_id:
            return

        # If file is deleted ignore
        if file_id in self.deleted_files:
            return

        old_attrs = self.files.get(file_id)

        # first event about a file
        if old_attrs is None:
            self.files[file_id] = new_attrs
            await self.on_file_created(file_id=file_id, parent_file_id=parent_file_id)
            return

        # events about attrs of newly created file,
        # we already handled file creation event so only update attrs
        if set(new_attrs.keys()) - set(old_attrs.keys()):
            self.files[file_id].update(new_attrs)
            return

        # important, because we update referenced object
        old_attrs = old_attrs.copy()
        updated_attrs = get_updated_attrs(new_attrs, old_attrs)

        # Check if anything changed
        if not updated_attrs:
            return

        # Update cache
        self.files[file_id].update(updated_attrs)

        await self.on_file_updated(
            file_id=file_id,
            parent_file_id=parent_file_id,
            new_attrs=new_attrs,
            old_attrs=old_attrs,
        )

    async def _handle_deleted(self, data: dict):
        file_id: str = data.get("fileId")
        parent_file_id: str = data.get("parentFileId")
        if not file_id:
            return

        if file_id in self.deleted_files:
            return

        old_attrs = self.files.pop(file_id, None)
        self.deleted_files[file_id] = old_attrs

        await self.on_file_deleted(file_id=file_id, parent_file_id=parent_file_id)

    # ======= Interface =======

    @abstractmethod
    async def on_file_created(self, file_id: str, parent_file_id: str):
        pass

    @abstractmethod
    async def on_file_updated(
        self, file_id: str, parent_file_id: str, new_attrs: dict, old_attrs: dict
    ):
        pass

    @abstractmethod
    async def on_file_deleted(self, file_id: str, parent_file_id: str):
        pass


# ======= EXAMPLE IMPLEMENTATION FOR TESTS =======


class SpaceFilesMonitorClientImpl(SpaceFilesMonitorClient):
    async def on_file_created(self, file_id, parent_file_id):
        await self.created_events.put(file_id)

    async def on_file_updated(self, file_id, parent_file_id, new_attrs, old_attrs):
        await self.updated_events.put(
            {file_id: get_updated_attrs(new_attrs, old_attrs)}
        )

    async def on_file_deleted(self, file_id, parent_file_id):
        await self.deleted_events.put(file_id)


def get_updated_attrs(new_attrs, old_attrs):
    return {k: new_attrs[k] for k in new_attrs if new_attrs[k] != old_attrs[k]}
