"""This module contains meta steps for operations on transfers."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Mapping

from _pytest._py.path import LocalPath

from tests.gui.meta_steps.oneprovider.common import (
    migrate_file_to_provider,
    replicate_files_to_provider,
)
from tests.gui.meta_steps.oneprovider.data import go_to_filebrowser
from tests.gui.meta_steps.oneprovider.transfers import (
    evict_file,
    open_transfers_page,
    wait_for_all_transfers_to_start_and_finish,
)
from tests.gui.meta_steps.onezone.common import wt_visit_file_browser
from tests.gui.steps.oneprovider.data_tab import upload_file_to_cwd_in_data_tab
from tests.gui.steps.oneprovider.transfers import assert_ended_transfer
from tests.gui.type_definitions import TmpMemory
from tests.mixed.steps.rest.oneprovider.transfers import (
    assert_recent_transfer_details_rest,
    assert_recent_transfer_finished_rest,
    create_transfer_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import Users


@wt(
    parsers.parse(
        'using {client}, {user} replicates {file_type} "{path}" in space "{space}" to'
        " provider {provider_to}"
    )
)
def replicate_file_to_provider_op(
    client: str,
    user: str,
    path: str,
    space: str,
    provider_to: str,
    users: Users,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
) -> None:
    transfer_type = "replication"
    if client.lower() == "rest":
        path = space + "/" + path
        create_transfer_rest(
            user,
            users,
            provider_to,
            hosts,
            transfer_type,
            path,
            replicating_provider=provider_to,
        )
    elif client.lower() == "web gui":
        result = "replicates"
        go_to_filebrowser(selenium, user, tmp_memory, space)
        replicate_files_to_provider(
            selenium, user, [path], tmp_memory, [provider_to], hosts, result
        )
    else:
        raise NoSuchClientException(f"Client {client} not found")


@wt(
    parsers.parse(
        'using {client}, {user} migrates {file_type} "{path}" in space "{space}" to'
        " provider {provider_to} from {provider_from}"
    )
)
def migrate_file_to_provider_op(
    client: str,
    user: str,
    path: str,
    space: str,
    provider_to: str,
    provider_from: str,
    users: Users,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
) -> None:
    transfer_type = "migration"
    if client.lower() == "rest":
        path = space + "/" + path
        create_transfer_rest(
            user,
            users,
            provider_from,
            hosts,
            transfer_type,
            path,
            replicating_provider=provider_to,
            evicting_provider=provider_from,
        )
    elif client.lower() == "web gui":
        result = "migrates"
        go_to_filebrowser(selenium, user, tmp_memory, space)
        migrate_file_to_provider(
            selenium,
            user,
            path,
            tmp_memory,
            provider_from,
            provider_to,
            hosts,
            result,
        )
    else:
        raise NoSuchClientException(f"Client {client} not found")


@wt(
    parsers.parse(
        'using {client}, {user} evicts {file_type} "{path}" in space "{space}" from'
        " provider {provider_from}"
    )
)
def evict_file_to_provider_op(
    client: str,
    user: str,
    path: str,
    space: str,
    provider_from: str,
    users: Users,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
) -> None:
    transfer_type = "eviction"
    if client.lower() == "rest":
        path = space + "/" + path
        create_transfer_rest(
            user,
            users,
            provider_from,
            hosts,
            transfer_type,
            path,
            evicting_provider=provider_from,
        )
    elif client.lower() == "web gui":
        go_to_filebrowser(selenium, user, tmp_memory, space)
        evict_file(selenium, user, provider_from, path, tmp_memory, hosts)
    else:
        raise NoSuchClientException(f"Client {client} not found")


@wt(
    parsers.parse(
        "using {client}, {user} sees details about last transfer of {item_type} in"
        ' space "{space}" in provider {host}:\n{config}'
    )
)
def assert_details_of_recent_transfer_op(
    client: str,
    user: str,
    users: Users,
    host: str,
    hosts: Hosts,
    spaces: Mapping[str, str],
    item_type: str,
    space: str,
    config: str,
    selenium: SeleniumDrivers,
) -> None:
    if client.lower() == "rest":
        assert_recent_transfer_details_rest(
            user, users, host, hosts, space, spaces, config
        )
    elif client.lower() == "web gui":
        open_transfers_page(selenium, user, host, space, hosts)
        assert_ended_transfer(selenium, user, item_type, config, hosts)
    else:
        raise NoSuchClientException(f"Client {client} not found")


@wt(
    parsers.parse(
        'using {client}, {user} waits for last transfer to finish in space "{space}" in'
        " provider {host}"
    )
)
def wait_for_recent_transfer_to_finish_op(
    client: str,
    user: str,
    users: Users,
    host: str,
    hosts: Hosts,
    space: str,
    spaces: Mapping[str, str],
    selenium: SeleniumDrivers,
) -> None:
    if client.lower() == "rest":
        assert_recent_transfer_finished_rest(user, users, host, hosts, spaces, space)
    elif client.lower() == "web gui":
        open_transfers_page(selenium, user, host, space, hosts)
        wait_for_all_transfers_to_start_and_finish(selenium, user, host, space, hosts)
    else:
        raise NoSuchClientException(f"Client {client} not found")


@wt(
    parsers.parse(
        'using {client}, {user} uploads file "{path}" to {provider} Oneprovider file'
        ' browser in space "{space}"'
    )
)
def upload_file_to_provider_browser(
    selenium: SeleniumDrivers,
    client: str,
    user: str,
    path: str,
    provider: str,
    space: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
    tmpdir: LocalPath,
) -> None:
    if client.lower() == "web gui":
        wt_visit_file_browser(selenium, [provider], [space], [user], tmp_memory, hosts)
        upload_file_to_cwd_in_data_tab(selenium, user, path, tmpdir)
    else:
        raise NoSuchClientException(f"Client {client} not found")
