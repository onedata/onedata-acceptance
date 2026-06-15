"""This module contains gherkin steps to run mixed acceptance tests featuring
quality of service using web GUI and REST.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Mapping

from tests.conftest import SeleniumDrivers
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.qos import (
    add_qos_requirement_in_modal,
    assert_qos_file_status_in_op_gui,
    delete_qos_requirement_in_op_gui,
)
from tests.gui.types import TmpMemory
from tests.mixed.steps.rest.oneprovider.qos import (
    HostsConfig,
    UserLike,
    assert_qos_file_status_in_op_rest,
    create_qos_requirement_in_op_rest,
    delete_qos_requirement_in_op_rest,
)
from tests.mixed.utils.common import NoSuchClientException
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) creates "
        '"(?P<expression>.*)" QoS requirement for "(?P<file_name>.*)" in'
        ' space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_qos_requirement_in_op(
    client: str,
    user: str,
    selenium: SeleniumDrivers,
    file_name: str,
    tmp_memory: TmpMemory,
    expression: str,
    space_name: str,
    users: Mapping[str, UserLike],
    hosts: HostsConfig,
    host: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        add_qos_requirement_in_modal(
            selenium,
            user,
            file_name,
            tmp_memory,
            expression,
            space_name,
        )
    elif client_lower == "rest":
        create_qos_requirement_in_op_rest(
            user, users, hosts, host, expression, space_name, file_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that file "
        '"(?P<file_name>.*)" (?P<option>has not got|has some) QoS '
        'requirements in space "(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_qos_file_status_in_op(
    client: str,
    user: str,
    file_name: str,
    space_name: str,
    host: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    users: Mapping[str, UserLike],
    hosts: HostsConfig,
    option: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        assert_qos_file_status_in_op_gui(
            user,
            file_name,
            space_name,
            tmp_memory,
            selenium,
            option,
        )
    elif client_lower == "rest":
        assert_qos_file_status_in_op_rest(
            user, users, hosts, host, space_name, file_name, option
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) deletes all QoS "
        'requirements for "(?P<file_name>.*)" in space '
        '"(?P<space_name>.*)" in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def delete_qos_requirement_in_op(
    client: str,
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    file_name: str,
    tmp_memory: TmpMemory,
    users: Mapping[str, UserLike],
    hosts: HostsConfig,
    host: str,
) -> None:
    client_lower = client.lower()
    if client_lower == "web gui":
        delete_qos_requirement_in_op_gui(
            selenium,
            user,
            space_name,
            file_name,
            tmp_memory,
        )
    elif client_lower == "rest":
        delete_qos_requirement_in_op_rest(
            user, users, hosts, host, space_name, file_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found")
