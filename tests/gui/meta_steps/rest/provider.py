"""Meta steps for provider management using REST API helpers."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.steps.rest.provider import get_provider_ones3_status
from tests.type_definitions import Hosts
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.parse(
        "using REST, user {user} sees that status of OneS3 of {provider} is ok"
    )
)
def assert_provider_ones3_status_ok(provider: str, hosts: Hosts) -> None:
    status = get_provider_ones3_status(hosts[provider]["hostname"])
    error_message = f"Status of OneS3 is {status['isOk']}"
    assert status["isOk"], error_message
