"""Steps for cdmi usage.
"""

from pytest_bdd import parsers, then, when

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.utils.generic import repeat_failed
from tests.utils.acceptance_utils import wt

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


@wt(parsers.parse('using CDMI API {user} writes "{text}" to "{path}" starting '
                  'at offset {offset:d} in "{provider}" provider'))
@repeat_failed(timeout=WAIT_BACKEND)
def partial_write_to_file_using_cdmi(user, text, path, offset, provider, cdmi,
                                     hosts, users):
    client = cdmi(hosts[provider]['ip'], users[user].token)
    client.write_to_file(path, text, offset)


@wt(parsers.parse('using CDMI API {user} reads from "{path}" in range {start:d}'
                  ' to {end:d} in "{provider}" provider'))
@repeat_failed(timeout=WAIT_BACKEND)
def partial_read_from_file_using_cdmi(user, path, start, end, provider, cdmi,
                                      hosts, users):
    client = cdmi(hosts[provider]['ip'], users[user].token)
    print client.read_from_file(path, read_range=(start, end))
