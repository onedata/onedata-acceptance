"""This module contains functions that counts different checksums"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import hashlib
from zlib import adler32


def md5_sum(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def sha256_sum(file_name):
    hash_sha256 = hashlib.sha256()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def sha512_sum(file_name):
    hash_sha512 = hashlib.sha512()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha512.update(chunk)
    return hash_sha512.hexdigest()


def adler32_sum(file_name):
    adler_sum = 1
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            adler_sum = adler32(chunk, adler_sum)
    return hex(adler_sum)[2:10].lower()
