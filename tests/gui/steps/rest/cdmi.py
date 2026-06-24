"""Steps for cdmi usage."""

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.utils import CDMIClient as cdmi
from tests.types import Hosts, Users
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
    user: str,
    text: str,
    path: str,
    offset: int,
    provider: str,
    hosts: Hosts,
    users: Users,
) -> None:
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
    user: str,
    path: str,
    start: int,
    end: int,
    provider: str,
    hosts: Hosts,
    users: Users,
) -> None:
    client = cdmi(hosts[provider]["ip"], users[user].token)
    print(client.read_from_file(path, read_range=(start, end)))
