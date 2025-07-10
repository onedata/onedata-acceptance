import boto3
from botocore.config import Config

from tests import ONES3_PORT
from tests.utils.bdd_utils import given, parsers, wt
from tests.gui.utils.generic import parse_seq
import os
import logging

logging.getLogger('botocore').setLevel(logging.DEBUG)
logging.getLogger('boto3').setLevel(logging.DEBUG)
logging.getLogger('urllib3').setLevel(logging.DEBUG)


# secret key can be set arbitrarily
SECRET_KEY = "secretKey"


def create_s3client(s3_endpoint, access_token, secret_key):
    s3_config = Config(
        # currently region_name can be set arbitrarily
        region_name='pl-reg-k1',
        connect_timeout=120,
        read_timeout=300,
        signature_version='s3v4',
        retries={
            'max_attempts': 3,
            'mode': 'standard'
        },
    s3={'addressing_style': 'path'}
    )

    return boto3.client(
        service_name='s3',
        endpoint_url=s3_endpoint,
        verify=False,
        region_name="pl-reg-k1",
        config=s3_config,
        aws_access_key_id=access_token,
        aws_secret_access_key=secret_key
    )


# def disable_payload_signing(request, **kwargs):
#     request.headers['x-amz-content-sha256'] = 'UNSIGNED-PAYLOAD'

def get_s3client(tmp_memory, tokens, hosts):
    if tmp_memory["s3 client"]:
        return tmp_memory["s3 client"]
    s3_endpoint = f"https://{hosts["oneprovider-1"]["hostname"]}:{ONES3_PORT}"
    tmp_memory["s3 client"] = create_s3client(s3_endpoint, tokens["oc_token"]["token"], SECRET_KEY)
    return tmp_memory["s3 client"]


def list_buckets(s3):
    return [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]


@wt(parsers.parse("user of {browser_id} can see {spaces_list} listed in OneS3 service"))
def wt_assert_listed_buckets(spaces_list, tmp_memory, tokens, hosts):
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_spaces = list_buckets(s3)
    assert set(actual_spaces) == set(parse_seq(spaces_list))


def does_bucket_exist(s3, bucket_name):
    return s3.head_bucket(Bucket=bucket_name)["ResponseMetadata"]["HTTPStatusCode"] == 200


@wt(parsers.parse('user of {browser_id} can see there is "{space_name}" in OneS3 service'))
def wt_assert_bucket_exists(space_name, tmp_memory, tokens, hosts):
    s3 = get_s3client(tmp_memory, tokens, hosts)
    assert does_bucket_exist(s3, space_name)


def download_file_from_bucket(s3, bucket_name, file_path, tmpdir, browser_id):
    home_dir = tmpdir.join(browser_id, "download")
    os.makedirs(home_dir, exist_ok=True)
    local_path = os.path.join(home_dir, file_path)
    s3.download_file(Bucket=bucket_name, Key=file_path, Filename=local_path)


@wt(parsers.parse('user of {browser_id} downloads "{file_name}" from "{space_name}" using OneS3 service'))
def wt_download_file_from_bucket(space_name, file_name, tmpdir, browser_id, tmp_memory, tokens, hosts):
    s3 = get_s3client(tmp_memory, tokens, hosts)
    download_file_from_bucket(s3, space_name, file_name, tmpdir, browser_id)

import io

def create_file_in_bucket(s3, bucket_name, file_name, file_content):
    data = b'hello'
    # s3.meta.events.register('before-sign.s3.PutObject', disable_payload_signing)
    # s3.meta.events.unregister('before-call.s3.PutObject', boto3.utils.add_expect_header)
    # s3.put_object(Bucket=bucket_name, Key=file_name, Body=bytes(file_content, encoding="utf-8"), ContentLength=5)
    # from unittest.mock import patch
    #
    # with patch('botocore.handlers.add_expect_header') as mock_header:
    #     mock_header.return_value = None
    bucket_name = "space2"
    s3.put_object(Bucket=bucket_name, Key=file_name,
                  Body=data)


@wt(parsers.parse('user of {browser_id} creates "{file_name}" with content "{file_content}" in "{space_name}" using OneS3 service'))
def wt_create_file_in_bucket(space_name, file_name, file_content, tmp_memory, tokens, hosts):
    s3 = get_s3client(tmp_memory, tokens, hosts)
    create_file_in_bucket(s3, space_name, file_name, file_content)


def read_file_content_from_bucket(s3, bucket_name, file_path):
    response = s3.get_object(Bucket=bucket_name, Key=file_path)
    return response['Body'].read().decode('utf-8')


@wt(parsers.parse('user of {browser_id} can see that "{file_name}" content is "{file_content}" in "{space_name}" using OneS3 service'))
def wt_assert_file_content_read_from_bucket(space_name, file_name, file_content, tmp_memory, tokens, hosts):
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_content = read_file_content_from_bucket(s3, space_name, file_name)
    assert actual_content == file_content


def list_bucket_content(s3, bucket_name):
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        return [obj["Key"] for obj in response["Contents"]]
    return []


@wt(parsers.parse('user of {browser_id} can see items {items} in "{space_name}" using OneS3 service'))
def wt_assert_bucket_content(space_name, items, tmp_memory, tokens, hosts):
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_content = list_bucket_content(s3, space_name)
    assert set(actual_content) == set(parse_seq(items))

