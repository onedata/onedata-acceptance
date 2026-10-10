"""Meta steps for S3 operations using lower-level request helpers."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from contextlib import suppress
from http import HTTPStatus

from requests.exceptions import HTTPError

from tests.gui.constants import WAIT_BACKEND
from tests.gui.steps.rest.provider import get_provider_service_nodes_statuses
from tests.gui.steps.rest.s3 import (
    assert_bucket_exists,
    create_bucket,
)
from tests.gui.utils.enums import OnedataService, OneS3ServiceState
from tests.type_definitions import HostDescription, Hosts
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.http_exceptions import HTTPNotFound
from tests.utils.user_utils import User
from tests.utils.utils import repeat_failed


@given(parsers.parse('using REST, user creates S3 bucket "{bucket_name}"'))
@wt(parsers.parse('using REST, user creates S3 bucket "{bucket_name}"'))
def create_s3_bucket_rest(bucket_name: str) -> None:
    ensure_bucket_exists(bucket_name)


@repeat_failed(timeout=WAIT_BACKEND)
def ensure_bucket_exists(bucket_name: str) -> None:
    try:
        create_bucket(bucket_name)
    except HTTPError as ex:
        # Creating an existing bucket is an idempotent success.
        if ex.response.status_code != HTTPStatus.CONFLICT:
            raise

    # Do not trust the bucket initializer's exit status. It can succeed after
    # contacting an old MinIO pod during a rolling update.
    assert_bucket_exists(bucket_name)


def provider_has_ones3_node(
    hosts: Hosts,
    provider: str,
    onepanel_credentials: User,
) -> bool:
    desc: HostDescription = hosts[provider]
    host = desc["pod_name"] + "." + desc["hostname"]
    start = time.time()

    while time.time() - start < WAIT_BACKEND:
        with suppress(HTTPNotFound):
            statuses = get_provider_service_nodes_statuses(
                hosts,
                provider,
                onepanel_credentials,
                OnedataService.ONES3,
            )
            if statuses.get(host) == OneS3ServiceState.HEALTHY:
                return True

        time.sleep(0.1)

    return False
