"""This module contains gherkin steps to run acceptance tests featuring
OneS3 calls using boto3 lib.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import boto3  # pylint: disable=import-error
from botocore.config import Config  # pylint: disable=import-error

from tests import ONES3_PORT
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

DEFAULT_ONES3_TIMEOUT = 10


# secret key can be set arbitrarily
SECRET_KEY = "secretKey"


def create_s3client(s3_endpoint, access_token, secret_key):
    s3_config = Config(
        # currently region_name can be set arbitrarily
        region_name="pl-reg-k1",
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
        region_name="pl-reg-k1",
        config=s3_config,
        aws_access_key_id=access_token,
        aws_secret_access_key=secret_key,
    )


def get_s3client(tmp_memory, tokens, hosts):
    if tmp_memory["s3 client"]:
        return tmp_memory["s3 client"]
    s3_endpoint = f"https://{hosts["oneprovider-1"]["hostname"]}:{ONES3_PORT}"
    tmp_memory["s3 client"] = create_s3client(
        s3_endpoint, tokens["oc_token"]["token"], SECRET_KEY
    )
    return tmp_memory["s3 client"]


def list_buckets(s3):
    return [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]


@wt(parsers.parse('using OneS3, user {user} can see spaces "{spaces_list}"'))
@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def wt_assert_listed_buckets(spaces_list, tmp_memory, tokens, hosts):
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_spaces = list_buckets(s3)
    spaces_list = parse_seq(spaces_list)
    err_msg = (
        f"Expected spaces: {spaces_list},\n does not match to actual ones:"
        f" {actual_spaces}"
    )
    assert set(actual_spaces) == set(spaces_list), err_msg
