"""This module contains steps featuring file events"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import asyncio
import time

import yaml

from tests import OP_REST_PORT
from tests.gui.utils.generic import parse_seq, transform
from tests.mixed.utils.sse_utils import SpaceFilesMonitorClientImpl
from tests.utils.bdd_utils import parsers, wt
from tests.utils.entities_setup.spaces import get_file_id_by_rest, get_file_id_cached

DEFAULT_FILE_EVENT_TIMEOUT: int = 30
NUMBER_OF_EVENTS_TO_LOOK_BACK: int = 10
EVENT_TYPES_MAP: dict[str, str] = {
    "creation": "created_file_ids",
    "deletion": "deleted_file_ids",
    "changed_or_created": "changed_or_created_events",
    "heartbeat": "heartbeat_events",
}


@wt(
    parsers.parse(
        'user {user} starts observing file events on "{attrs}" on dir "{dir_path}" in'
        ' space "{space}" in {host}'
    )
)
def wt_start_observing_file_events(
    user,
    attrs,
    dir_path,
    space,
    space_files_monitor,
    tmp_memory,
    hosts,
    host,
    spaces,
    users,
):
    space_id = spaces[space]
    token = users[user].token
    attrs = parse_seq(attrs)
    provider_hostname = hosts[host]["hostname"]
    op_authority = f"{provider_hostname}:{OP_REST_PORT}"
    dir_path = f"{space}/{dir_path}"
    file_id = get_file_id_by_rest(dir_path, provider_hostname, user, users)

    start_observing_file_events(
        space_files_monitor, tmp_memory, op_authority, space_id, token, [file_id], attrs
    )


def start_observing_file_events(
    space_files_monitor,
    tmp_memory,
    op_authority,
    space_id,
    token,
    observed_dirs,
    observed_attrs,
):
    monitor = space_files_monitor(
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
    user, users, host, hosts, path, space, tmp_memory, async_loop_in_thread
):
    provider_hostname = hosts[host]["hostname"]
    file_id = get_file_id_cached(
        f"{space}/{path}", provider_hostname, user, frozenset(users.items())
    )
    expected_result = file_id
    assert_file_event_in_observed_directory(
        tmp_memory, async_loop_in_thread, "creation", expected_result
    )


@wt(
    parsers.parse(
        'user {user} can see deleted file event about "{path}" in space "{space}" in'
        " {host}"
    )
)
def wt_assert_deleted_file_event_in_observed_directory(
    user, users, host, hosts, path, space, tmp_memory, async_loop_in_thread
):
    provider_hostname = hosts[host]["hostname"]
    file_id = get_file_id_cached(
        f"{space}/{path}", provider_hostname, user, frozenset(users.items())
    )
    expected_result = file_id
    assert_file_event_in_observed_directory(
        tmp_memory, async_loop_in_thread, "deletion", expected_result
    )


@wt(
    parsers.parse(
        "user {user} can see that the heartbeat event has just arrived in {host}"
    )
)
def assert_new_heartbeat_event(tmp_memory, async_loop_in_thread):
    event_type = "heartbeat"
    for _ in range(NUMBER_OF_EVENTS_TO_LOOK_BACK):
        try:
            res = get_file_event_in_observed_directory(
                tmp_memory, async_loop_in_thread, event_type
            )
            # event came in last 10s
            if time.time() - res[1] < 10:
                return
        except TimeoutError as e:
            raise AssertionError("heartbeat event not found") from e


@wt(
    parsers.parse(
        'user {user} can see following {event_type} file events of "{path}" in space'
        ' "{space}" in {host}:\n{config}'
    )
)
def wt_assert_updated_file_events_in_observed_directory(
    user,
    users,
    config,
    path,
    space,
    host,
    hosts,
    tmp_memory,
    async_loop_in_thread,
    event_type,
):
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
        f"{space}/{path}", provider_hostname, user, frozenset(users.items())
    )
    assert_file_events_in_observed_directory(
        tmp_memory, async_loop_in_thread, file_id, expected_attrs, transform(event_type)
    )


def assert_file_events_in_observed_directory(
    tmp_memory, async_loop_in_thread, file_id, expected_attrs, event_type
):
    found = set()
    expected_attrs_keys = set(expected_attrs.keys())

    # look for an event in previous events
    for _ in range(NUMBER_OF_EVENTS_TO_LOOK_BACK):
        try:
            result = get_file_event_in_observed_directory(
                tmp_memory, async_loop_in_thread, event_type
            )
            if file_id not in result:
                continue
            attrs = result[file_id]
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
                f"{event_type} events about {expected_attrs_keys - found} not found"
            ) from e


def assert_file_event_in_observed_directory(
    tmp_memory, async_loop_in_thread, event_type, expected_result
):
    # look for an event in previous events
    for _ in range(NUMBER_OF_EVENTS_TO_LOOK_BACK):
        try:
            result = get_file_event_in_observed_directory(
                tmp_memory, async_loop_in_thread, event_type
            )
            if result == expected_result:
                return
        except TimeoutError as e:
            raise AssertionError(
                f"{event_type} event {expected_result} not found"
            ) from e


def get_file_event_in_observed_directory(tmp_memory, async_loop_in_thread, event_type):
    monitor: SpaceFilesMonitorClientImpl = tmp_memory["monitor"]
    future = asyncio.run_coroutine_threadsafe(
        getattr(monitor, EVENT_TYPES_MAP[event_type]).get(),
        async_loop_in_thread,
    )
    try:
        return future.result(timeout=DEFAULT_FILE_EVENT_TIMEOUT)
    except TimeoutError:
        future.cancel()
        raise


@wt(parsers.parse("user {user} disconnects from SSE Stream"))
def disconnect_from_sse_stream(monitors, async_loop_in_thread):
    stop_last_file_monitor(monitors, async_loop_in_thread)


@wt(
    parsers.parse(
        "user {user} reconnects to SSE Stream starting from first captured event id"
    )
)
def reconnect_to_sse_stream(monitors, async_loop_in_thread):
    start_last_file_monitor(monitors, async_loop_in_thread)


def stop_last_file_monitor(monitors, async_loop_in_thread):
    monitors[-1][1].cancel()
    asyncio.run_coroutine_threadsafe(asyncio.sleep(0), async_loop_in_thread).result()


def start_last_file_monitor(monitors, async_loop_in_thread):
    monitors[-1][0].last_event_id = monitors[-1][0].first_event_id
    future = asyncio.run_coroutine_threadsafe(
        monitors[-1][0].run(),
        async_loop_in_thread,
    )
    monitors[-1] = (
        monitors[-1][0],
        future,
    )


# def get_file_id_cached(file_path, provider_hostname, user, users,):
#     if not hasattr(get_file_id_cached, "cache"):
#         get_file_id_cached.cache = {}
#     cache = get_file_id_cached.cache
#     if file_path in cache:
#         return cache[file_path]
#     file_id = get_file_id_by_rest(file_path, provider_hostname, user, users)
#     cache[file_path] = file_id
#     return file_id
