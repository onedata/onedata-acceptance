"""Steps for amazon s3 buckets usage."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import hashlib
import hmac
import json
import subprocess as sp
from datetime import datetime, timezone

import requests
from requests.exceptions import HTTPError

from tests.conftest import REQUEST_TIMEOUT
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.type_definitions import Clipboard
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed

HOST_URL = "dev-volume-s3-krakow.default:9000"
S3_APP_LABEL = "dev-volume-s3-krakow"

ACCESS_KEY = "accessKey"
SECRET_KEY = "verySecretKey"


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


def sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def get_signature_key(key: str, date_stamp: str) -> bytes:
    k_date = sign(("AWS4" + key).encode("utf-8"), date_stamp)
    k_region = sign(k_date, "eu-central-1")
    k_service = sign(k_region, "s3")
    k_signing = sign(k_service, "aws4_request")
    return k_signing


def create_canonical_request(
    method: str,
    uri: str,
    query_string: str,
    headers: dict[str, str],
    signed_headers: str,
    payload_hash: str,
) -> str:
    canonical_headers = "".join(f"{k}:{v}\n" for k, v in sorted(headers.items()))
    return (
        f"{method}\n"
        f"{uri}\n"
        f"{query_string}\n"
        f"{canonical_headers}\n"
        f"{signed_headers}\n"
        f"{payload_hash}"
    )


def create_string_to_sign(
    date_stamp: str,
    credential_scope: str,
    hashed_canonical_request: str,
) -> str:
    return (
        "AWS4-HMAC-SHA256\n"
        f"{date_stamp}\n"
        f"{credential_scope}\n"
        f"{hashed_canonical_request}"
    )


def create_authorization_header(
    access_key: str,
    credential_scope: str,
    signed_headers: str,
    signature: str,
) -> str:
    return (
        f"AWS4-HMAC-SHA256 Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )


def s3_authorization(
    method: str,
    headers: dict[str, str],
    canonical_uri: str,
    canonical_querystring: str,
    payload_hash: str,
    date_stamp: str,
    amz_date: str,
) -> str:
    signed_headers = ";".join(headers.keys())
    canonical_request = create_canonical_request(
        method,
        canonical_uri,
        canonical_querystring,
        headers,
        signed_headers,
        payload_hash,
    )
    hashed_canonical_request = hashlib.sha256(
        canonical_request.encode("utf-8")
    ).hexdigest()
    credential_scope = f"{date_stamp}/eu-central-1/s3/aws4_request"
    string_to_sign = create_string_to_sign(
        amz_date, credential_scope, hashed_canonical_request
    )
    signing_key = get_signature_key(SECRET_KEY, date_stamp)
    signature = hmac.new(
        signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    authorization_header = create_authorization_header(
        ACCESS_KEY, credential_scope, signed_headers, signature
    )
    return authorization_header


def create_bucket(bucket_name: str) -> None:
    now = datetime.now(timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    payload_hash = "UNSIGNED-PAYLOAD"
    canonical_uri = f"/{bucket_name}"
    canonical_querystring = ""
    headers = {
        "host": HOST_URL,
        "x-amz-content-sha256": payload_hash,
        "x-amz-date": amz_date,
    }

    authorization_header = s3_authorization(
        "PUT",
        headers,
        canonical_uri,
        canonical_querystring,
        payload_hash,
        date_stamp,
        amz_date,
    )

    headers["Authorization"] = authorization_header

    url = f"{get_s3_endpoint_url()}{canonical_uri}"
    response = requests.put(url, headers=headers, timeout=REQUEST_TIMEOUT)

    response.raise_for_status()


def assert_bucket_exists(bucket_name: str) -> None:
    now = datetime.now(timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    payload_hash = "UNSIGNED-PAYLOAD"
    canonical_uri = f"/{bucket_name}"
    headers = {
        "host": HOST_URL,
        "x-amz-content-sha256": payload_hash,
        "x-amz-date": amz_date,
    }

    headers["Authorization"] = s3_authorization(
        "HEAD",
        headers,
        canonical_uri,
        "",
        payload_hash,
        date_stamp,
        amz_date,
    )

    response = requests.head(
        f"{get_s3_endpoint_url()}{canonical_uri}",
        headers=headers,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()


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


def copy_item_between_buckets(dst_bucket: str, src: str, dst: str) -> None:
    now = datetime.now(timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    payload_hash = "UNSIGNED-PAYLOAD"
    canonical_uri = f"/{dst_bucket}/{dst}"
    canonical_querystring = ""

    headers = {
        "host": f"{dst_bucket}.s3.amazonaws.com",
        "x-amz-content-sha256": payload_hash,
        "x-amz-copy-source": f"/{src}",
        "x-amz-date": amz_date,
    }
    authorization_header = s3_authorization(
        "PUT",
        headers,
        canonical_uri,
        canonical_querystring,
        payload_hash,
        date_stamp,
        amz_date,
    )

    headers["Authorization"] = authorization_header

    url = f"{get_s3_endpoint_url()}{canonical_uri}"
    response = requests.put(url, headers=headers, timeout=REQUEST_TIMEOUT)

    response.raise_for_status()


@repeat_failed(timeout=WAIT_BACKEND)
def get_current_s3_pod_ip() -> str:
    output = sp.check_output(
        [
            "kubectl",
            "get",
            "pods",
            "-l",
            f"app={S3_APP_LABEL}",
            "-o",
            "json",
        ],
        text=True,
    )
    pods = json.loads(output)["items"]
    ready_pods = [
        pod
        for pod in pods
        if pod["metadata"].get("deletionTimestamp") is None
        and pod["status"].get("phase") == "Running"
        and any(
            status.get("ready", False)
            for status in pod["status"].get("containerStatuses", [])
        )
        and pod["status"].get("podIP")
    ]
    if not ready_pods:
        raise RuntimeError(f'No ready pod found for app "{S3_APP_LABEL}"')

    newest_pod = max(ready_pods, key=lambda pod: pod["metadata"]["creationTimestamp"])
    return newest_pod["status"]["podIP"]


def get_s3_endpoint_url() -> str:
    return f"http://{get_current_s3_pod_ip()}:9000"
