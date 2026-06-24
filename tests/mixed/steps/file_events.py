"""This module contains steps featuring file events"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import asyncio
import time
from collections.abc import Coroutine, Mapping
from enum import Enum
from typing import Protocol, cast

import yaml

from tests import OP_REST_PORT
from tests.conftest import Hosts
from tests.gui.sse_fixtures import MonitorEntry
from tests.gui.utils.generic import parse_seq
from tests.mixed.types import EventMemory, EventResult, ExpectedAttrs, FileAttrs
from tests.mixed.utils.common import UsersWithToken
from tests.mixed.utils.sse_utils import SpaceFilesMonitorClientImpl
from tests.utils.bdd_utils import parsers, wt
from tests.utils.entities_setup.spaces import get_file_id_by_rest, get_file_id_cached


class ObservedFileAction(Enum):
    CREATION = "creation"
    DELETION = "deletion"
    CHANGED_OR_CREATED = "changed_or_created"
    HEARTBEAT = "heartbeat"


DEFAULT_FILE_EVENT_TIMEOUT: int = 30
NUMBER_OF_EVENTS_TO_LOOK_BACK: int = 10


class SpaceFilesMonitorFactory(Protocol):
    def __call__(
        self,
        *,
        oneprovider_authority: str,
        space_id: str,
        token: str,
        observed_dirs: list[str],
        observed_attrs: list[str],
    ) -> SpaceFilesMonitorClientImpl: ...


@wt(
    parsers.parse(
        'user {user} starts observing file events on "{attrs}" on dir "{dir_path}" in'
        ' space "{space}" in {host}'
    )
)
def wt_start_observing_file_events(
    user: str,
    attrs: str,
    dir_path: str,
    space: str,
    space_files_monitor_factory: SpaceFilesMonitorFactory,
    tmp_memory: EventMemory,
    hosts: Hosts,
    host: str,
    spaces: Mapping[str, str],
    users: UsersWithToken,
) -> None:
    space_id = spaces[space]
    token = users[user].token
    observed_attrs = parse_seq(attrs)
    provider_hostname = hosts[host]["hostname"]
    op_authority = f"{provider_hostname}:{OP_REST_PORT}"
    dir_path = f"{space}/{dir_path}"
    file_id = get_file_id_by_rest(dir_path, provider_hostname, users[user].token)

    start_observing_file_events(
        space_files_monitor_factory,
        tmp_memory,
        op_authority,
        space_id,
        token,
        [file_id],
        observed_attrs,
    )


def start_observing_file_events(
    space_files_monitor_factory: SpaceFilesMonitorFactory,
    tmp_memory: EventMemory,
    op_authority: str,
    space_id: str,
    token: str,
    observed_dirs: list[str],
    observed_attrs: list[str],
) -> None:
    monitor = space_files_monitor_factory(
        oneprovider_authority=op_authority,
        space_id=space_id,
        token=token,
        observed_dirs=observed_dirs,
        observed_attrs=observed_attrs,
    )
    tmp_memory["monitor"] = monitor


@wt(
    parsers.parse(
        'user {user} can see new file event about "{path}" in space "{space}" in {host}'
    )
)
def wt_assert_new_file_event_in_observed_directory(
    user: str,
    users: UsersWithToken,
    host: str,
    hosts: Hosts,
    path: str,
    space: str,
    tmp_memory: EventMemory,
    async_loop_in_thread: asyncio.AbstractEventLoop,
) -> None:
    provider_hostname = hosts[host]["hostname"]
    file_id = get_file_id_cached(
        f"{space}/{path}", provider_hostname, users[user].token
    )
    expected_result = file_id
    assert_file_action_in_observed_directory(
        tmp_memory, async_loop_in_thread, ObservedFileAction.CREATION, expected_result
    )


@wt(
    parsers.parse(
        'user {user} can see deleted file event about "{path}" in space "{space}" in'
        " {host}"
    )
)
def wt_assert_deleted_file_event_in_observed_directory(
    user: str,
    users: UsersWithToken,
    host: str,
    hosts: Hosts,
    path: str,
    space: str,
    tmp_memory: EventMemory,
    async_loop_in_thread: asyncio.AbstractEventLoop,
) -> None:
    provider_hostname = hosts[host]["hostname"]
    file_id = get_file_id_cached(
        f"{space}/{path}", provider_hostname, users[user].token
    )
    expected_result = file_id
    assert_file_action_in_observed_directory(
        tmp_memory, async_loop_in_thread, ObservedFileAction.DELETION, expected_result
    )


@wt(
    parsers.parse(
        "user {user} can see that the heartbeat event has just arrived in {host}"
    )
)
def assert_new_heartbeat_event(
    tmp_memory: EventMemory, async_loop_in_thread: asyncio.AbstractEventLoop
) -> None:
    for _ in range(NUMBER_OF_EVENTS_TO_LOOK_BACK):
        try:
            result = get_file_action_in_observed_directory(
                tmp_memory, async_loop_in_thread, ObservedFileAction.HEARTBEAT
            )
            heartbeat = cast(tuple[str, float], result)
            # event came in last 10s
            if time.time() - heartbeat[1] < 10:
                return
        except TimeoutError as e:
            raise AssertionError("heartbeat event not found") from e


@wt(
    parsers.parse(
        'user {user} can see following changed_or_created file events of "{path}" in'
        ' space "{space}" in {host}:\n{config}'
    )
)
def wt_assert_updated_file_events_in_observed_directory(
    user: str,
    users: UsersWithToken,
    config: str,
    path: str,
    space: str,
    host: str,
    hosts: Hosts,
    tmp_memory: EventMemory,
    async_loop_in_thread: asyncio.AbstractEventLoop,
) -> None:
    """
    Expected config format:
    - attr_name
    OR
    - attr_name: <actual_value>
    """
    expected_data = yaml.load(config, yaml.Loader)
    expected_attrs = {}
    for item in expected_data:
        if isinstance(item, dict):
            for attr_name, attr_val in item.items():
                expected_attrs[attr_name] = attr_val
        else:
            expected_attrs[item] = None
    provider_hostname = hosts[host]["hostname"]
    file_id = get_file_id_cached(
        f"{space}/{path}", provider_hostname, users[user].token
    )
    assert_file_actions_in_observed_directory(
        tmp_memory,
        async_loop_in_thread,
        file_id,
        expected_attrs,
        ObservedFileAction.CHANGED_OR_CREATED,
    )


def assert_file_actions_in_observed_directory(
    tmp_memory: EventMemory,
    async_loop_in_thread: asyncio.AbstractEventLoop,
    file_id: str,
    expected_attrs: ExpectedAttrs,
    file_action: ObservedFileAction,
) -> None:
    found: set[str] = set()
    expected_attrs_keys = set(expected_attrs.keys())

    # look for an event in previous events
    for _ in range(NUMBER_OF_EVENTS_TO_LOOK_BACK):
        try:
            result = get_file_action_in_observed_directory(
                tmp_memory, async_loop_in_thread, file_action
            )
            changed_files = cast(dict[str, FileAttrs], result)
            if file_id not in changed_files:
                continue
            attrs = changed_files[file_id]
            for attr in attrs:
                if attr in expected_attrs_keys:
                    if expected_attrs[attr] is not None:
                        if attrs[attr] == expected_attrs[attr]:
                            found.add(attr)
                    else:
                        found.add(attr)
            if found == expected_attrs_keys:
                return
        except TimeoutError as e:
            raise AssertionError(
                f"{file_action} file actions about {expected_attrs_keys - found} not"
                " found"
            ) from e


def assert_file_action_in_observed_directory(
    tmp_memory: EventMemory,
    async_loop_in_thread: asyncio.AbstractEventLoop,
    file_action: ObservedFileAction,
    expected_result: str,
) -> None:
    # look for an event in previous events
    for _ in range(NUMBER_OF_EVENTS_TO_LOOK_BACK):
        try:
            result = get_file_action_in_observed_directory(
                tmp_memory, async_loop_in_thread, file_action
            )
            if result == expected_result:
                return
        except TimeoutError as e:
            raise AssertionError(
                f"{file_action} file action {expected_result} not found"
            ) from e


def get_file_action_in_observed_directory(
    tmp_memory: EventMemory,
    async_loop_in_thread: asyncio.AbstractEventLoop,
    file_action: ObservedFileAction,
) -> EventResult:
    monitor = tmp_memory["monitor"]
    coroutine: Coroutine[object, object, EventResult]
    if file_action == ObservedFileAction.CREATION:
        coroutine = cast(
            Coroutine[object, object, EventResult], monitor.created_file_ids.get()
        )
    elif file_action == ObservedFileAction.DELETION:
        coroutine = cast(
            Coroutine[object, object, EventResult], monitor.deleted_file_ids.get()
        )
    elif file_action == ObservedFileAction.CHANGED_OR_CREATED:
        coroutine = cast(
            Coroutine[object, object, EventResult],
            monitor.changed_or_created_events.get(),
        )
    elif file_action == ObservedFileAction.HEARTBEAT:
        coroutine = cast(
            Coroutine[object, object, EventResult], monitor.heartbeat_events.get()
        )
    else:
        raise AssertionError(f"file action: {file_action} not found")

    future = asyncio.run_coroutine_threadsafe(
        coroutine,
        async_loop_in_thread,
    )
    try:
        return future.result(timeout=DEFAULT_FILE_EVENT_TIMEOUT)
    except TimeoutError:
        future.cancel()
        raise


@wt(parsers.parse("user {user} disconnects from SSE Stream"))
def disconnect_from_sse_stream(
    monitors: list[MonitorEntry], async_loop_in_thread: asyncio.AbstractEventLoop
) -> None:
    stop_last_file_monitor(monitors, async_loop_in_thread)


@wt(
    parsers.parse(
        "user {user} reconnects to SSE Stream starting from first captured event id"
    )
)
def reconnect_to_sse_stream(
    monitors: list[MonitorEntry], async_loop_in_thread: asyncio.AbstractEventLoop
) -> None:
    start_last_file_monitor(monitors, async_loop_in_thread)


def stop_last_file_monitor(
    monitors: list[MonitorEntry], async_loop_in_thread: asyncio.AbstractEventLoop
) -> None:
    monitors[-1].future.cancel()
    asyncio.run_coroutine_threadsafe(asyncio.sleep(0), async_loop_in_thread).result()


def start_last_file_monitor(
    monitors: list[MonitorEntry], async_loop_in_thread: asyncio.AbstractEventLoop
) -> None:
    last_monitor: SpaceFilesMonitorClientImpl = monitors[-1].monitor
    last_monitor.last_event_id = last_monitor.first_event_id
    future = asyncio.run_coroutine_threadsafe(
        last_monitor.run(),
        async_loop_in_thread,
    )
    monitors[-1] = MonitorEntry(
        monitor=last_monitor,
        future=future,
    )
