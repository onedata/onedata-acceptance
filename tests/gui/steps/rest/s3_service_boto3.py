"""Low-level OneS3 helpers using the boto3 library."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from typing import Protocol, TypedDict, cast

import boto3  # pylint: disable=import-error
from _pytest._py.path import LocalPath
from botocore.config import Config  # pylint: disable=import-error

DEFAULT_ONES3_TIMEOUT = 10

S3_REGION_NAME = "pl-reg-k1"


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


def list_buckets(s3: S3Client) -> list[str]:
    return [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]


def does_bucket_exist(s3: S3Client, bucket_name: str) -> bool:
    return (
        s3.head_bucket(Bucket=bucket_name)["ResponseMetadata"]["HTTPStatusCode"] == 200
    )


def download_file_from_bucket(
    s3: S3Client, bucket_name: str, file_path: str, tmpdir: LocalPath, user: str
) -> None:
    home_dir = tmpdir.join(user, "download")
    os.makedirs(home_dir, exist_ok=True)
    local_path = os.path.join(home_dir, file_path)
    s3.download_file(Bucket=bucket_name, Key=file_path, Filename=local_path)


def create_file_in_bucket(
    s3: S3Client, bucket_name: str, file_name: str, file_content: str
) -> None:
    s3.put_object(
        Bucket=bucket_name, Key=file_name, Body=bytes(file_content, encoding="utf-8")
    )


def read_file_content_from_bucket(
    s3: S3Client, bucket_name: str, file_path: str
) -> str:
    response = s3.get_object(Bucket=bucket_name, Key=file_path)
    return response["Body"].read().decode("utf-8")


def list_bucket_content(s3: S3Client, bucket_name: str) -> list[str]:
    response = s3.list_objects_v2(Bucket=bucket_name)
    if "Contents" in response:
        return [obj["Key"] for obj in response["Contents"]]
    return []
