"""Meta steps for S3 operations using lower-level request helpers."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from http import HTTPStatus

from requests.exceptions import HTTPError

from tests.gui.steps.rest.s3 import (
    assert_bucket_exists,
    create_bucket,
)
from tests.gui.utils.common.constants import WAIT_BACKEND
from tests.utils.bdd_utils import given, parsers, wt
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
