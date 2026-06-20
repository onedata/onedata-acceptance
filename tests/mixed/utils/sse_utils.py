"""This module contains utils for handling sse (Server-Sent Events)"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import asyncio
import json
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Final, NotRequired, Optional, TypedDict, cast

from aiohttp_sse_client import client as sse_client  # pylint: disable=import-error
from aiohttp_sse_client.client import MessageEvent  # pylint: disable=import-error

INITIAL_BACKOFF_TIMEOUT: Final[int] = 1
MAX_BACKOFF_TIMEOUT: Final[int] = 60
BACKOFF_INCREASE_FACTOR: Final[int] = 2

type FileAttrs = dict[str, str | int]


class ChangedOrCreatedEventData(TypedDict):
    fileId: str
    parentFileId: str
    attributes: NotRequired[FileAttrs]


class DeletedEventData(TypedDict):
    fileId: str
    parentFileId: str


class SSEEvent(Enum):
    CHANGED_OR_CREATED = "changedOrCreated"
    HEARTBEAT = "heartbeat"
    DELETED = "deleted"


class SpaceFilesMonitorClient(ABC):  # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        oneprovider_authority: str,
        space_id: str,
        access_token: str,
        observed_dirs: list[str],
        observed_attrs: list[str],
        verify_ssl: bool = True,
    ) -> None:
        self.oneprovider_authority = oneprovider_authority.rstrip("/")
        self.space_id = space_id
        self.access_token = access_token
        self.observed_dirs = observed_dirs
        self.observed_attrs = observed_attrs
        self.verify_ssl = verify_ssl

        # fileId -> attrs
        self.files: dict[str, FileAttrs] = {}
        self.deleted_files: set[str] = set()
        self.last_event_id: Optional[str] = None
        self.first_event_id: Optional[str] = None

        self.changed_or_created_events: asyncio.Queue[dict[str, FileAttrs]] = (
            asyncio.Queue()
        )
        self.heartbeat_events: asyncio.Queue[tuple[str, float]] = asyncio.Queue()

        self.backoff: int = INITIAL_BACKOFF_TIMEOUT

    # ======= PUBLIC ENTRYPOINT =======

    async def run(self) -> None:
        """
        Main loop
        """
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        while True:
            try:
                print("Connecting to SSE stream...")
                if self.last_event_id:
                    print(f"Last event id {self.last_event_id}")
                await self._consume_stream(reconnect=bool(self.last_event_id))
            except asyncio.CancelledError:
                break
            except Exception as e:  # pylint: disable=broad-exception-caught
                if loop.is_closed() or not loop.is_running():
                    print("Loop is closed, breaking run()")
                    break
                try:
                    print(f"Stream error: {e}\n Reconnect in {self.backoff} s")
                    await asyncio.sleep(self.backoff)
                except asyncio.CancelledError:
                    print("Cancelled during backoff sleep, shutting down")
                    break
                self.backoff = min(
                    self.backoff * BACKOFF_INCREASE_FACTOR, MAX_BACKOFF_TIMEOUT
                )

        # clean up data structures to allow reusing this object after reconnection
        self.clean()

    async def _consume_stream(self, reconnect: bool = False) -> None:
        url: str = (
            f"https://{self.oneprovider_authority}/api/v3/oneprovider/spaces/"
            f"{self.space_id}/events/files"
        )

        headers: dict[str, str] = {
            "X-Auth-Token": self.access_token,
            "Accept": "text/event-stream",
            "Content-Type": "application/json",
        }

        if reconnect and self.last_event_id is not None:
            headers["Last-Event-Id"] = self.last_event_id

        body: dict[str, list[str]] = {
            "observedDirectories": self.observed_dirs,
            "observedAttributes": self.observed_attrs,
        }

        async with sse_client.EventSource(
            url,
            option={"method": "POST"},
            headers=headers,
            json=body,
            ssl=self.verify_ssl,
            on_open=self.reset_backoff,
        ) as event_source:
            async for event in event_source:
                await self._handle_event(event)

    async def _handle_event(self, event: MessageEvent) -> None:
        event_type: str = event.type
        data_raw: str = event.data
        self.last_event_id = event.last_event_id
        if self.first_event_id is None:
            self.first_event_id = event.last_event_id

        try:
            raw_data: object = json.loads(data_raw)
        except json.JSONDecodeError:
            print(f"Cannot decode data: {data_raw!r}")
            return

        # Heartbeat events carry JSON null rather than an object.
        if event_type == SSEEvent.HEARTBEAT.value:
            await self.heartbeat_events.put(
                (
                    event.last_event_id,
                    time.time(),
                )
            )
            return

        if not isinstance(raw_data, dict):
            print(f"Unexpected event data={raw_data!r}")
            return
        data = cast(dict[str, object], raw_data)

        if event_type == SSEEvent.CHANGED_OR_CREATED.value:
            await self._handle_changed_or_created(cast(ChangedOrCreatedEventData, data))
        elif event_type == SSEEvent.DELETED.value:
            await self._handle_deleted(cast(DeletedEventData, data))
        else:
            print(f"Unknown event type={event_type}, data={data}")

    async def _handle_changed_or_created(self, data: ChangedOrCreatedEventData) -> None:
        file_id: str = data["fileId"]
        parent_file_id: str = data["parentFileId"]
        attrs = cast(FileAttrs, data.get("attributes", {}))

        # If file is deleted ignore
        if file_id in self.deleted_files:
            return

        cached_attrs: FileAttrs = self.files.get(file_id, {}).copy()

        await self.changed_or_created_events.put({file_id: attrs})

        # First event about a file
        if not cached_attrs:
            self.files[file_id] = attrs
            await self.on_file_created(file_id=file_id, parent_file_id=parent_file_id)
            return

        # Because the observed attributes are stored in different documents,
        # they are delivered in separate events. As a result,
        # a single logical file creation may be represented
        # by multiple events (e.g. 3–4 events), each containing a different
        # subset of the observed attributes.
        #
        # The first event received for a given attribute subset is treated as the
        # “file creation” event for that subset. Subsequent events for the same
        # subset are considered updates.
        if set(attrs.keys()) - set(cached_attrs.keys()):
            self.files[file_id].update(attrs)
            return

        updated_attrs: FileAttrs = get_updated_attrs(attrs, cached_attrs)
        # Check if anything changed
        if not updated_attrs:
            return

        # Update cache
        self.files[file_id].update(updated_attrs)

        await self.on_file_updated(
            file_id=file_id,
            parent_file_id=parent_file_id,
            attrs=attrs,
            cached_attrs=cached_attrs,
        )

    async def _handle_deleted(self, data: DeletedEventData) -> None:
        file_id: str = data["fileId"]
        parent_file_id: str = data["parentFileId"]

        if file_id in self.deleted_files:
            return

        self.files.pop(file_id, None)
        self.deleted_files.add(file_id)

        await self.on_file_deleted(file_id=file_id, parent_file_id=parent_file_id)

    def reset_backoff(self) -> None:
        self.backoff = INITIAL_BACKOFF_TIMEOUT

    # ======= Interface =======

    @abstractmethod
    async def on_file_created(self, file_id: str, parent_file_id: str) -> None:
        pass

    @abstractmethod
    async def on_file_updated(
        self,
        file_id: str,
        parent_file_id: str,
        attrs: FileAttrs,
        cached_attrs: FileAttrs,
    ) -> None:
        pass

    @abstractmethod
    async def on_file_deleted(self, file_id: str, parent_file_id: str) -> None:
        pass

    @abstractmethod
    def clean(self) -> None:
        self.files = {}
        self.deleted_files = set()


# ======= EXAMPLE IMPLEMENTATION FOR TESTS =======


class SpaceFilesMonitorClientImpl(SpaceFilesMonitorClient):

    def __init__(
        self,
        oneprovider_authority: str,
        space_id: str,
        access_token: str,
        observed_dirs: list[str],
        observed_attrs: list[str],
        verify_ssl: bool = True,
    ) -> None:
        super().__init__(
            oneprovider_authority,
            space_id,
            access_token,
            observed_dirs,
            observed_attrs,
            verify_ssl=verify_ssl,
        )
        self.created_file_ids: asyncio.Queue[str] = asyncio.Queue()
        self.updated_file_attrs: asyncio.Queue[dict[str, FileAttrs]] = asyncio.Queue()
        self.deleted_file_ids: asyncio.Queue[str] = asyncio.Queue()

    async def on_file_created(self, file_id: str, parent_file_id: str) -> None:
        await self.created_file_ids.put(file_id)

    async def on_file_updated(
        self,
        file_id: str,
        parent_file_id: str,
        attrs: FileAttrs,
        cached_attrs: FileAttrs,
    ) -> None:
        await self.updated_file_attrs.put(
            {file_id: get_updated_attrs(attrs, cached_attrs)}
        )

    async def on_file_deleted(self, file_id: str, parent_file_id: str) -> None:
        await self.deleted_file_ids.put(file_id)

    def clean(self) -> None:
        super().clean()
        self.created_file_ids = asyncio.Queue()
        self.updated_file_attrs = asyncio.Queue()
        self.deleted_file_ids = asyncio.Queue()


def get_updated_attrs(attrs: FileAttrs, cached_attrs: FileAttrs) -> FileAttrs:
    return {k: attrs[k] for k in attrs if attrs[k] != cached_attrs[k]}
