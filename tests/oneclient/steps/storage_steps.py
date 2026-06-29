"""This module contains gherkin steps to run acceptance tests featuring
storage parameter modifications in Onepanel using REST API in Oneclient tests.
"""

__author__ = "Bartek Kryza"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.oneclient.steps.rest.onepanel.storages import modify_storage_parameters
from tests.type_definitions import Hosts, Storages
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import User


@wt(
    parsers.parse(
        'using REST, {user} changes storage "{storage_type}" named "{storage}" '
        'parameter "{parameter}" to "{value}" at provider "{provider}"'
    )
)
def modify_storage_parameter(
    user: str,
    storage_type: str,
    storage: str,
    parameter: str,
    value: str,
    provider: str,
    storages: Storages,
    hosts: Hosts,
    onepanel_credentials: User,
) -> None:
    storage_id = storages[provider][storage]
    onepanel_host = None

    for host in hosts:
        if "name" in hosts[host] and hosts[host]["name"] == provider:
            onepanel_host = hosts[host]["hostname"]
    if not onepanel_host:
        raise RuntimeError(f"onepanel host {provider} not found")

    modify_params = {"type": storage_type, parameter: value}
    modify_storage_parameters(
        user,
        provider,
        storage_id,
        storage,
        modify_params,
        onepanel_host,
        onepanel_credentials,
    )
