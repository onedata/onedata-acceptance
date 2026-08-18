"""Meta steps for OneS3 calls using lower-level boto3 helpers."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from _pytest._py.path import LocalPath

from tests.gui.steps.rest.s3_service_boto3 import (
    DEFAULT_ONES3_TIMEOUT,
    create_file_in_bucket,
    does_bucket_exist,
    download_file_from_bucket,
    get_s3client,
    list_bucket_content,
    list_buckets,
    read_file_content_from_bucket,
)
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils.generic import parse_elements_sequence
from tests.type_definitions import Hosts, Tokens
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "using OneS3 and list buckets boto3 function, user {user} can see spaces"
        ' "{spaces_list:ElementsSequence}"',
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
@wt(
    parsers.parse(
        'using OneS3, user {user} can see spaces "{spaces_list:ElementsSequence}"',
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def wt_assert_listed_buckets(
    spaces_list: list[str], tmp_memory: TmpMemory, tokens: Tokens, hosts: Hosts
) -> None:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_spaces = list_buckets(s3)
    error_message = (
        f"Expected spaces: {spaces_list},\n does not match to actual ones:"
        f" {actual_spaces}"
    )
    assert set(actual_spaces) == set(spaces_list), error_message


@wt(
    parsers.parse(
        "using OneS3 and head bucket boto3 function, user {user} can see there is"
        ' a space "{space_name}"'
    )
)
def wt_assert_bucket_exists(
    space_name: str, tmp_memory: TmpMemory, tokens: Tokens, hosts: Hosts
) -> None:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    assert does_bucket_exist(s3, space_name)


@wt(
    parsers.parse(
        'using OneS3, user {user} downloads "{file_name}" from "{space_name}"'
    )
)
def wt_download_file_from_bucket(
    space_name: str,
    file_name: str,
    tmpdir: LocalPath,
    user: str,
    tmp_memory: TmpMemory,
    tokens: Tokens,
    hosts: Hosts,
) -> None:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    download_file_from_bucket(s3, space_name, file_name, tmpdir, user)


@wt(
    parsers.parse(
        'using OneS3, user {user} creates "{file_name}" with content '
        '"{file_content}" in "{space_name}"'
    )
)
@repeat_failed(timeout=DEFAULT_ONES3_TIMEOUT)
def wt_create_file_in_bucket(
    space_name: str,
    file_name: str,
    file_content: str,
    tmp_memory: TmpMemory,
    tokens: Tokens,
    hosts: Hosts,
) -> None:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    create_file_in_bucket(s3, space_name, file_name, file_content)


@wt(
    parsers.parse(
        'using OneS3, user {user} can see that "{file_name}" content is '
        '"{file_content}" in "{space_name}"'
    )
)
def wt_assert_file_content_read_from_bucket(
    space_name: str,
    file_name: str,
    file_content: str,
    tmp_memory: TmpMemory,
    tokens: Tokens,
    hosts: Hosts,
) -> None:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_content = read_file_content_from_bucket(s3, space_name, file_name)
    error_message = (
        f"Actual content:\n {actual_content}\n is different than expected:\n"
        f" {file_content}\n for file {file_name}"
    )
    assert actual_content == file_content, error_message


@wt(
    parsers.parse(
        "using OneS3, user {user} can see items "
        '{items:ElementsSequence} in "{space_name}"',
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
def wt_assert_bucket_content(
    space_name: str,
    items: list[str],
    tmp_memory: TmpMemory,
    tokens: Tokens,
    hosts: Hosts,
) -> None:
    s3 = get_s3client(tmp_memory, tokens, hosts)
    actual_content = list_bucket_content(s3, space_name)
    assert set(actual_content) == set(items)
