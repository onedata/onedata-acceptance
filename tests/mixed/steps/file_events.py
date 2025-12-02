""" This module contains steps featuring file events"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata.org"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import asyncio

import yaml

from tests import OP_REST_PORT
from tests.gui.utils.generic import parse_seq
from tests.mixed.utils.sse_utils import SpaceFilesMonitorClientImpl
from tests.utils.bdd_utils import parsers, wt
from tests.utils.entities_setup.spaces import get_file_id_by_rest

DEFAULT_FILE_EVENT_TIMEOUT = 30


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
    op_url = f"https://{provider_hostname}:{OP_REST_PORT}"
    dir_path = f"{space}/{dir_path}"
    file_id = get_file_id_by_rest(dir_path, provider_hostname, user, users)

    start_observing_file_events(
        space_files_monitor, tmp_memory, op_url, space_id, token, [file_id], attrs
    )


def start_observing_file_events(
    space_files_monitor,
    tmp_memory,
    op_url,
    space_id,
    token,
    observed_dirs,
    observed_attrs,
):
    monitor = space_files_monitor(
        oneprovider_url=op_url,
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
def wt_assert_new_file_event_in_obs_dir(
    user, users, host, hosts, path, space, tmp_memory, async_loop_in_thread
):
    provider_hostname = hosts[host]["hostname"]
    file_id = get_file_id_by_rest(f"{space}/{path}", provider_hostname, user, users)
    ex_res = file_id
    assert_file_event_in_obs_dir(tmp_memory, async_loop_in_thread, "created", ex_res)


@wt(
    parsers.parse(
        'user {user} can see deleted file event about "{path}" in space "{space}" in'
        " {host}"
    )
)
def wt_assert_deleted_file_event_in_obs_dir(
    user, users, host, hosts, path, space, tmp_memory, async_loop_in_thread
):
    provider_hostname = hosts[host]["hostname"]
    file_id = get_file_id_by_rest(f"{space}/{path}", provider_hostname, user, users)
    ex_res = file_id
    assert_file_event_in_obs_dir(tmp_memory, async_loop_in_thread, "deleted", ex_res)


@wt(
    parsers.parse(
        'user {user} can see following updated file events of "{path}" in space'
        ' "{space}" in {host}:\n{config}'
    )
)
def wt_assert_updated_file_events_in_obs_dir(
    user, users, config, path, space, host, hosts, tmp_memory, async_loop_in_thread
):
    """
    Expected config format:
    - attr_name
    OR
    - attr_name: <actual_value>
    """
    expected_data = yaml.load(config, yaml.Loader)
    formatted_data = {}
    for el in expected_data:
        if isinstance(el, dict):
            for k, v in el.items():
                formatted_data[k] = v
        else:
            formatted_data[el] = None
    provider_hostname = hosts[host]["hostname"]
    file_id = get_file_id_by_rest(f"{space}/{path}", provider_hostname, user, users)
    assert_file_events_in_obs_dir(
        tmp_memory, async_loop_in_thread, file_id, formatted_data
    )


def assert_file_events_in_obs_dir(tmp_memory, async_loop_in_thread, file_id, data):
    event_type = "updated"
    found = set()
    expected_attrs = set(data.keys())

    # look for an event in previous events
    for _ in range(10):
        try:
            res = get_file_event_in_observed_dir(
                tmp_memory, async_loop_in_thread, event_type
            )
            if file_id in res:
                attrs = res[file_id]
            else:
                continue
            for attr in attrs:
                if attr in data:
                    if data[attr] is not None:
                        if attrs[attr] == data[attr]:
                            found.add(attr)
                    else:
                        found.add(attr)
            if found == expected_attrs:
                return
        except TimeoutError as e:
            raise AssertionError(
                f"{event_type} events about {expected_attrs - found} not found"
            ) from e


def assert_file_event_in_obs_dir(tmp_memory, async_loop_in_thread, event_type, ex_res):
    # look for an event in previous events
    for _ in range(10):
        try:
            res = get_file_event_in_observed_dir(
                tmp_memory, async_loop_in_thread, event_type
            )
            if res == ex_res:
                return
        except TimeoutError as e:
            raise AssertionError(f"{event_type} event {ex_res} not found") from e


def get_file_event_in_observed_dir(tmp_memory, async_loop_in_thread, event_type):
    monitor: SpaceFilesMonitorClientImpl = tmp_memory["monitor"]
    fut = asyncio.run_coroutine_threadsafe(
        getattr(monitor, f"{event_type}_events").get(),
        async_loop_in_thread,
    )
    try:
        return fut.result(timeout=DEFAULT_FILE_EVENT_TIMEOUT)
    except TimeoutError:
        fut.cancel()
        raise
