"""Steps for provider management using REST API."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests import ONES3_PORT, OP_REST_PORT
from tests.utils.bdd_utils import parsers, wt
from tests.utils.rest_utils import get_provider_rest_path, http_get


def get_provider_id(provider, hosts, users):
    user = "admin"
    provider_hostname = hosts[provider]["hostname"]
    provider_conf = http_get(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("configuration"),
        auth=(user, users[user].password),
    ).json()
    return provider_conf["providerId"]


@wt(
    parsers.parse(
        "using REST, user {user} sees that status of OneS3 of {provider} is ok"
    )
)
def assert_provider_ones3_status_ok(provider, hosts):
    provider_hostname = hosts[provider]["hostname"]
    status = http_get(
        ip=provider_hostname,
        port=ONES3_PORT,
        path="/.__onedata__status__",
    ).json()
    err_msg = f"Status of OneS3 is of status {status["isOk"]}"
    assert status["isOk"], err_msg
