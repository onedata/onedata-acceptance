"""Steps for cdmi usage."""

from typing import Any

from tests.conftest import Hosts, Users
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.utils import CDMIClient as cdmi
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


@wt(
    parsers.parse(
        'using CDMI API {user} writes "{text}" to "{path}" starting '
        'at offset {offset:d} in "{provider}" provider'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def partial_write_to_file_using_cdmi(
    user: Any,
    text: Any,
    path: Any,
    offset: Any,
    provider: Any,
    hosts: Hosts,
    users: Users,
) -> Any:
    client = cdmi(hosts[provider]["ip"], users[user].token)
    client.write_to_file(path, text, offset)


@wt(
    parsers.parse(
        'using CDMI API {user} reads from "{path}" in range {start:d}'
        ' to {end:d} in "{provider}" provider'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def partial_read_from_file_using_cdmi(
    user: Any,
    path: Any,
    start: Any,
    end: Any,
    provider: Any,
    hosts: Hosts,
    users: Users,
) -> Any:
    client = cdmi(hosts[provider]["ip"], users[user].token)
    print(client.read_from_file(path, read_range=(start, end)))
