"""Meta steps for S3 operations using lower-level request helpers."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import requests
from requests.exceptions import HTTPError

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.rest.s3 import (
    assert_bucket_exists,
    copy_item_between_buckets,
    create_bucket,
)
from tests.gui.type_definitions import Clipboard
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@given(parsers.parse('using REST, user creates S3 bucket "{bucket_name}"'))
@wt(parsers.parse('using REST, user creates S3 bucket "{bucket_name}"'))
def create_s3_bucket_rest(bucket_name: str) -> None:
    ensure_bucket_exists(bucket_name)


@wt(
    parsers.parse(
        "using REST, user of {browser_id} copies item with "
        'recently copied path from "{src_bucket}" bucket into "{dst_bucket}" bucket'
    )
)
def copy_item_s3_bucket(
    browser_id: str,
    dst_bucket: str,
    src_bucket: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    path = clipboard.paste(display=displays[browser_id])
    copy_item_between_buckets(
        dst_bucket, f"{src_bucket}{path}/999999", f"{path[1::]}/999999"
    )


@repeat_failed(timeout=WAIT_BACKEND, exceptions=(requests.RequestException,))
def ensure_bucket_exists(bucket_name: str) -> None:
    try:
        create_bucket(bucket_name)
    except HTTPError as ex:
        # Creating an existing bucket is an idempotent success.
        if ex.response.status_code != 409:
            raise

    # Do not trust the bucket initializer's exit status. It can succeed after
    # contacting an old MinIO pod during a rolling update.
    assert_bucket_exists(bucket_name)
