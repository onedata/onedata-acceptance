"""This module contains gherkin steps to run acceptance tests featuring
OneS3 calls using boto3 lib.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from typing import Any

import boto3  # pylint: disable=import-error
from botocore.config import Config  # pylint: disable=import-error

from tests import ONES3_PORT
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

DEFAULT_ONES3_TIMEOUT = 10


# secret key can be set arbitrarily
SECRET_KEY = "secretKey"

S3_REGION_NAME = "pl-reg-k1"


def create_s3client(s3_endpoint: Any, access_token: Any, secret_key: Any) -> Any:
    s3_config = Config(
        # currently region_name can be set arbitrarily
        region_name=S3_REGION_NAME,
        connect_timeout=120,
        read_timeout=300,
        signature_version="s3v4",
        retries={"max_attempts": 3, "mode": "standard"},
        s3={"addressing_style": "path"},
    )

    return boto3.client(
        service_name="s3",
        endpoint_url=s3_endpoint,
        verify=False,
        region_name=S3_REGION_NAME,
        config=s3_config,
        aws_access_key_id=access_token,
        aws_secret_access_key=secret_key,
    )


def get_s3client(tmp_memory: Any, tokens: Any, hosts: Any) -> Any:
    if tmp_memory["s3 client"]:
        return tmp_memory["s3 client"]
    s3_endpoint = f"https://{hosts["oneprovider-1"]["hostname"]}:{ONES3_PORT}"
    tmp_memory["s3 client"] = create_s3client(
        s3_endpoint, tokens["oc_token"]["token"], SECRET_KEY
    )
    return tmp_memory["s3 client"]


def list_buckets(s3: Any) -> Any:
    return [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]


@wt(
    parsers.parse(
        "using OneS3 and list buckets boto3 function, user {user} can see spaces"
        ' "{spaces_list}"'
    )
)
@wt(parsers.parse('using OneS3, user {user} can see spaces "{spaces_list}"'))
@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def wt_assert_listed_buckets(
    spaces_list: Any, tmp_memory: Any, tokens: Any, hosts: Any
) -> Any:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_spaces = list_buckets(s3)
    spaces_list = parse_seq(spaces_list)
    err_msg = (
        f"Expected spaces: {spaces_list},\n does not match to actual ones:"
        f" {actual_spaces}"
    )
    assert set(actual_spaces) == set(spaces_list), err_msg


def does_bucket_exist(s3: Any, bucket_name: Any) -> Any:
    return (
        s3.head_bucket(Bucket=bucket_name)["ResponseMetadata"]["HTTPStatusCode"] == 200
    )


@wt(
    parsers.parse(
        "using OneS3 and head bucket boto3 function, user {user} can see there is a"
        ' space "{space_name}"'
    )
)
def wt_assert_bucket_exists(
    space_name: Any, tmp_memory: Any, tokens: Any, hosts: Any
) -> Any:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    assert does_bucket_exist(s3, space_name)


def download_file_from_bucket(
    s3: Any, bucket_name: Any, file_path: Any, tmpdir: Any, user: Any
) -> Any:
    home_dir = tmpdir.join(user, "download")
    os.makedirs(home_dir, exist_ok=True)
    local_path = os.path.join(home_dir, file_path)
    s3.download_file(Bucket=bucket_name, Key=file_path, Filename=local_path)


@wt(
    parsers.parse(
        'using OneS3, user {user} downloads "{file_name}" from "{space_name}"'
    )
)
def wt_download_file_from_bucket(
    space_name: Any,
    file_name: Any,
    tmpdir: Any,
    user: Any,
    tmp_memory: Any,
    tokens: Any,
    hosts: Any,
) -> Any:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    download_file_from_bucket(s3, space_name, file_name, tmpdir, user)


@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def create_file_in_bucket(
    s3: Any, bucket_name: Any, file_name: Any, file_content: Any
) -> Any:
    s3.put_object(
        Bucket=bucket_name, Key=file_name, Body=bytes(file_content, encoding="utf-8")
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} creates "{file_name}" with content '
        '"{file_content}" in "{space_name}"'
    )
)
def wt_create_file_in_bucket(
    space_name: Any,
    file_name: Any,
    file_content: Any,
    tmp_memory: Any,
    tokens: Any,
    hosts: Any,
) -> Any:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    create_file_in_bucket(s3, space_name, file_name, file_content)


def read_file_content_from_bucket(s3: Any, bucket_name: Any, file_path: Any) -> Any:
    response = s3.get_object(Bucket=bucket_name, Key=file_path)
    return response["Body"].read().decode("utf-8")


@wt(
    parsers.parse(
        'using OneS3, user {user} can see that "{file_name}" content is '
        '"{file_content}" in "{space_name}"'
    )
)
def wt_assert_file_content_read_from_bucket(
    space_name: Any,
    file_name: Any,
    file_content: Any,
    tmp_memory: Any,
    tokens: Any,
    hosts: Any,
) -> Any:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_content = read_file_content_from_bucket(s3, space_name, file_name)
    err_msg = (
        f"Actual content:\n {actual_content}\n is different than expected:\n"
        f" {file_content}\n for file {file_name}"
    )
    assert actual_content == file_content, err_msg


def list_bucket_content(s3: Any, bucket_name: Any) -> Any:
    response = s3.list_objects_v2(Bucket=bucket_name)
    if "Contents" in response:
        return [obj["Key"] for obj in response["Contents"]]
    return []


@wt(parsers.parse('using OneS3, user {user} can see items {items} in "{space_name}"'))
def wt_assert_bucket_content(
    space_name: Any, items: Any, tmp_memory: Any, tokens: Any, hosts: Any
) -> Any:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_content = list_bucket_content(s3, space_name)
    assert set(actual_content) == set(parse_seq(items))
