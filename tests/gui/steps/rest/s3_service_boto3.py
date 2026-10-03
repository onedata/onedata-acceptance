# ruff: noqa: N803 - boto3 keyword names are part of the external API
"""Low-level OneS3 helpers using the boto3 library."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from collections.abc import Callable
from typing import Any, Protocol, TypedDict, cast

import boto3
import pytest
from botocore.config import Config
from botocore.exceptions import ClientError  # pylint: disable=import-error

from tests import ONES3_PORT
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils.generic import ELEMENTS_SEQUENCE_PATTERN, parse_seq
from tests.type_definitions import Hosts, Tokens
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

DEFAULT_ONES3_TIMEOUT = 10

S3_CONFIG = {"token": "oc_token"}

# secret key can be set arbitrarily
SECRET_KEY = "secretKey"

S3_REGION_NAME = "pl-reg-k1"


def expect_error(
    operation: Callable[..., Any],
    *args: Any,
    error_code: int | None = None,
    message_contains: str | None = None,
    **kwargs,
):
    with pytest.raises(ClientError) as exc:
        operation(*args, **kwargs)

    error = exc.value.response.get("Error", {})
    code = error.get("Code")
    message = error.get("Message", "")

    if error_code is not None:
        assert code == error_code, (
            f"Expected error code {error_code}, got {code}, full error: {exc.value}"
        )

    if message_contains is not None:
        assert message_contains in message, (
            f'Expected error message to contain "{message_contains}", '
            f'got "{message}", full error: {exc.value}'
        )


def run_ones3_operation(
    tmp_memory: TmpMemory,
    tokens: Tokens,
    hosts: Hosts,
    operation: Callable[..., Any],
    *operation_args: Any,
    expected_error: dict[str, Any] | None = None,
):
    s3 = get_s3client(tmp_memory, tokens, hosts)

    if expected_error is not None:
        return expect_error(operation, s3, *operation_args, **expected_error)

    return operation(s3, *operation_args)


class S3Bucket(TypedDict):
    Name: str


class ObjectDescription(TypedDict):
    Key: str


class ResponseMetadata(TypedDict):
    HTTPStatusCode: int


class ReadableBody(Protocol):
    def read(self) -> bytes: ...


class S3Client(Protocol):
    def list_buckets(self) -> dict[str, list[S3Bucket]]: ...

    def head_bucket(self, *, Bucket: str) -> dict[str, ResponseMetadata]: ...

    def download_file(self, *, Bucket: str, Key: str, Filename: str) -> None: ...

    def put_object(self, *, Bucket: str, Key: str, Body: bytes) -> object: ...

    def get_object(self, *, Bucket: str, Key: str) -> dict[str, ReadableBody]: ...

    def list_objects_v2(self, *, Bucket: str) -> dict[str, list[ObjectDescription]]: ...


def create_s3client(s3_endpoint: str, access_token: str, secret_key: str) -> S3Client:
    s3_config = Config(
        # currently region_name can be set arbitrarily
        region_name=S3_REGION_NAME,
        connect_timeout=120,
        read_timeout=300,
        signature_version="s3v4",
        retries={"max_attempts": 3, "mode": "standard"},
        s3={"addressing_style": "path"},
    )

    return cast(
        S3Client,
        boto3.client(
            service_name="s3",
            endpoint_url=s3_endpoint,
            verify=False,
            region_name=S3_REGION_NAME,
            config=s3_config,
            aws_access_key_id=access_token,
            aws_secret_access_key=secret_key,
        ),
    )


def get_s3client(tmp_memory: TmpMemory, tokens: Tokens, hosts: Hosts):
    token_name = S3_CONFIG["token"]
    if token_name in tmp_memory["s3 client"]:
        return tmp_memory["s3 client"][token_name]
    s3_endpoint = f"https://{hosts['oneprovider-1']['hostname']}:{ONES3_PORT}"
    tmp_memory["s3 client"][token_name] = create_s3client(
        s3_endpoint, tokens[token_name]["token"], SECRET_KEY
    )
    return tmp_memory["s3 client"][token_name]


@wt(parsers.parse('user starts using token "{token_name}" in OneS3'))
def wt_start_using_token_for_s3_client(token_name: str):
    S3_CONFIG["token"] = token_name


def download_file_from_bucket(
    s3: S3Client, bucket_name: str, file_path: str, tmpdir: str, user: str
):
    home_dir = tmpdir.join(user, "download")
    os.makedirs(home_dir, exist_ok=True)
    local_path = os.path.join(home_dir, file_path)
    s3.download_file(Bucket=bucket_name, Key=file_path, Filename=local_path)


@wt(parsers.parse('using OneS3, user {user} downloads "{file_name}" from "{space_name}"'))
def wt_download_file_from_bucket(space_name, file_name, tmpdir, user, tmp_memory, tokens, hosts):
    s3 = get_s3client(tmp_memory, tokens, hosts)
    download_file_from_bucket(s3, space_name, file_name, tmpdir, user)


def list_buckets(s3: S3Client) -> list[str]:
    return [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]


@wt(
    parsers.re(
        rf"using OneS3 and list buckets boto3 function, user (?P<browser_id>\w+?) can see spaces (?P<spaces_list>{ELEMENTS_SEQUENCE_PATTERN})"
    )
)
@wt(
    parsers.re(
        rf"using OneS3, user (?P<browser_id>\w+?) can see spaces (?P<spaces_list>{ELEMENTS_SEQUENCE_PATTERN})"
    )
)
@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def wt_assert_listed_buckets(spaces_list: str, tmp_memory: TmpMemory, tokens: Tokens, hosts: Hosts):
    actual_spaces = run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        list_buckets,
    )

    spaces_list = parse_seq(spaces_list)

    assert set(actual_spaces) == set(spaces_list), (
        f"Expected spaces: {spaces_list}, got: {actual_spaces}"
    )


@wt(parsers.parse("using OneS3, user {user} fails to list spaces"))
def wt_fail_list_buckets(tmp_memory: TmpMemory, tokens: Tokens, hosts: Hosts):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        list_buckets,
        expected_error={"error_code": "AccessDenied"},
    )


def does_bucket_exist(s3: S3Client, bucket_name: str) -> bool:
    success_code = 200
    return s3.head_bucket(Bucket=bucket_name)["ResponseMetadata"]["HTTPStatusCode"] == success_code


@wt(
    parsers.parse(
        "using OneS3 and head bucket boto3 function, user {user} can see there is a"
        ' space "{space_name}"'
    )
)
def wt_assert_bucket_exists(space_name: str, tmp_memory: TmpMemory, tokens: Tokens, hosts: Hosts):
    exists = run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        does_bucket_exist,
        space_name,
    )

    assert exists, f"There is no space {space_name}"


@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def create_file_in_bucket(s3, bucket_name, file_name, file_content):
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=file_content.encode("utf-8"),
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} creates "{file_name}" with content '
        '"{file_content}" in "{space_name}"'
    )
)
def wt_create_file_in_bucket(space_name, file_name, file_content, tmp_memory, tokens, hosts):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        create_file_in_bucket,
        space_name,
        file_name,
        file_content,
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} fails to create "{file_name}" with content '
        '"{file_content}" in "{space_name}"'
    )
)
def wt_fail_to_create_file_in_bucket(
    space_name, file_name, file_content, tmp_memory, tokens, hosts
):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        create_file_in_bucket,
        space_name,
        file_name,
        file_content,
        expected_error={"error_code": "AccessDenied"},
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} fails to create "{file_name}" with content '
        '"{file_content}" in "{space_name}", because of NoSuchBucket error'
    )
)
def wt_fail_to_create_file_in_bucket_nosuchbucket_error(
    space_name, file_name, file_content, tmp_memory, tokens, hosts
):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        create_file_in_bucket,
        space_name,
        file_name,
        file_content,
        expected_error={"error_code": "NoSuchBucket"},
    )


@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def delete_file_in_bucket(s3, bucket_name, file_name):
    s3.delete_object(
        Bucket=bucket_name,
        Key=file_name,
    )


@wt(parsers.parse('using OneS3, user {user} deletes "{file_name}" in "{space_name}"'))
def wt_delete_file_in_bucket(space_name, file_name, tmp_memory, tokens, hosts):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        delete_file_in_bucket,
        space_name,
        file_name,
    )


@wt(parsers.parse('using OneS3, user {user} fails to delete "{file_name}" in "{space_name}"'))
def wt_fail_to_delete_file_in_bucket(space_name, file_name, tmp_memory, tokens, hosts):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        delete_file_in_bucket,
        space_name,
        file_name,
        expected_error={"error_code": "AccessDenied"},
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} fails to delete "{file_name}" '
        'in "{space_name}", because of NoSuchBucket error'
    )
)
def wt_fail_to_delete_file_in_bucket_nosuchbucket_error(
    space_name, file_name, tmp_memory, tokens, hosts
):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        delete_file_in_bucket,
        space_name,
        file_name,
        expected_error={"error_code": "NoSuchBucket"},
    )


def read_file_content_from_bucket(s3, bucket_name, file_path):
    response = s3.get_object(Bucket=bucket_name, Key=file_path)
    return response["Body"].read().decode("utf-8")


@wt(
    parsers.parse(
        'using OneS3, user {user} can see that "{file_name}" content is '
        '"{file_content}" in "{space_name}"'
    )
)
def wt_assert_file_content_read_from_bucket(
    space_name, file_name, file_content, tmp_memory, tokens, hosts
):
    actual_content = run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        read_file_content_from_bucket,
        space_name,
        file_name,
    )

    assert actual_content == file_content, (
        f"Actual content:\n{actual_content}\n!= expected:\n{file_content}\nfor file {file_name}"
    )


def list_bucket_content(s3, bucket_name):
    response = s3.list_objects_v2(Bucket=bucket_name)
    if "Contents" in response:
        return [obj["Key"] for obj in response["Contents"]]
    return []


@wt(parsers.parse('using OneS3, user {user} can see items {items} in "{space_name}"'))
@wt(parsers.parse('using OneS3, user {user} can see only items {items} in "{space_name}"'))
def wt_assert_bucket_content(space_name, items, tmp_memory, tokens, hosts):
    actual_content = run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        list_bucket_content,
        space_name,
    )

    assert set(actual_content) == set(parse_seq(items)), (
        f"Actual content:\n{actual_content}\n!= expected:\n{parse_seq(items)}\n"
        f"for space {space_name}"
    )


@wt(parsers.parse('using OneS3, user {user} fails to list items in "{space_name}"'))
def wt_fail_list_bucket_content(space_name, tmp_memory, tokens, hosts):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        list_bucket_content,
        space_name,
        expected_error={"error_code": "AccessDenied"},
    )


@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def copy_file_in_bucket(s3, bucket_name, source_file_name, target_file_name):
    s3.copy_object(
        Bucket=bucket_name,
        CopySource={"Bucket": bucket_name, "Key": source_file_name},
        Key=target_file_name,
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} copies "{source_file_name}" '
        'to "{target_file_name}" in "{space_name}"'
    )
)
def wt_copy_file_in_bucket(
    space_name, source_file_name, target_file_name, tmp_memory, tokens, hosts
):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        copy_file_in_bucket,
        space_name,
        source_file_name,
        target_file_name,
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} fails to copy "{source_file_name}" '
        'to "{target_file_name}" in "{space_name}"'
    )
)
def wt_fail_to_copy_file_in_bucket(
    space_name, source_file_name, target_file_name, tmp_memory, tokens, hosts
):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        copy_file_in_bucket,
        space_name,
        source_file_name,
        target_file_name,
        expected_error={"error_code": "AccessDenied"},
    )


@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def put_file_tagging_in_bucket(s3, bucket_name, file_name, tag_key, tag_value):
    s3.put_object_tagging(
        Bucket=bucket_name,
        Key=file_name,
        Tagging={
            "TagSet": [
                {
                    "Key": tag_key,
                    "Value": tag_value,
                }
            ]
        },
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} puts tag "{tag_key}"="{tag_value}" '
        'on "{file_name}" in "{space_name}"'
    )
)
def wt_put_file_tagging_in_bucket(
    space_name, file_name, tag_key, tag_value, tmp_memory, tokens, hosts
):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        put_file_tagging_in_bucket,
        space_name,
        file_name,
        tag_key,
        tag_value,
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} fails to put tag "{tag_key}"="{tag_value}" '
        'on "{file_name}" in "{space_name}"'
    )
)
def wt_fail_to_put_file_tagging_in_bucket(
    space_name, file_name, tag_key, tag_value, tmp_memory, tokens, hosts
):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        put_file_tagging_in_bucket,
        space_name,
        file_name,
        tag_key,
        tag_value,
        expected_error={"error_code": "AccessDenied"},
    )


@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def delete_file_tagging_in_bucket(s3, bucket_name, file_name):
    s3.delete_object_tagging(
        Bucket=bucket_name,
        Key=file_name,
    )


@wt(parsers.parse('using OneS3, user {user} deletes tags from "{file_name}" in "{space_name}"'))
def wt_delete_file_tagging_in_bucket(space_name, file_name, tmp_memory, tokens, hosts):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        delete_file_tagging_in_bucket,
        space_name,
        file_name,
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} fails to delete tags from "{file_name}" in "{space_name}"'
    )
)
def wt_fail_to_delete_file_tagging_in_bucket(space_name, file_name, tmp_memory, tokens, hosts):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        delete_file_tagging_in_bucket,
        space_name,
        file_name,
        expected_error={"error_code": "AccessDenied"},
    )


@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def put_file_acl_in_bucket(s3, bucket_name, file_name, acl):
    s3.put_object_acl(
        Bucket=bucket_name,
        Key=file_name,
        ACL=acl,
    )


@wt(parsers.parse('using OneS3, user {user} puts ACL "{acl}" on "{file_name}" in "{space_name}"'))
def wt_put_file_acl_in_bucket(space_name, file_name, acl, tmp_memory, tokens, hosts):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        put_file_acl_in_bucket,
        space_name,
        file_name,
        acl,
    )


@wt(
    parsers.parse(
        'using OneS3, user {user} fails to put ACL "{acl}" on "{file_name}" in "{space_name}"'
    )
)
def wt_fail_to_put_file_acl_in_bucket(space_name, file_name, acl, tmp_memory, tokens, hosts):
    run_ones3_operation(
        tmp_memory,
        tokens,
        hosts,
        put_file_acl_in_bucket,
        space_name,
        file_name,
        acl,
        expected_error={"error_code": "AccessDenied"},
    )
