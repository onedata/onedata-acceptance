"""Steps for handling workflow results in Oneprovider GUI."""

__author__ = "Jakub Karczewski, Mateusz Zajac, Katarzyna Such"
__copyright__ = "Copyright (C) 2023-2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.type_definitions import FilePath
from tests.gui.utils.common.count_checksums import (
    adler32_sum,
    md5_sum,
    sha256_sum,
    sha512_sum,
)


def count_checksums_for_downloaded_file(
    downloaded_file: FilePath, checksum_list: list[str]
) -> dict[str, str]:
    results = {}
    checksum_functions = {
        "adler32_sum": adler32_sum,
        "md5_sum": md5_sum,
        "sha256_sum": sha256_sum,
        "sha512_sum": sha512_sum,
    }

    for checksum in checksum_list:
        checksum_function_name = checksum + "_sum"
        results[checksum] = checksum_functions[checksum_function_name](downloaded_file)

    return results
