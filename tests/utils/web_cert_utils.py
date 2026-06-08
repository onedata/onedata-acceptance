"""This module contains utility functions for web certificates."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from pathlib import Path
from typing import Any

from tests import PROJECT_DIR
from tests.utils.bdd_utils import parsers, wt
from tests.utils.environment_utils import run_kubectl_command

CERT_PATH_OP = Path("/etc/op_panel/certs")
CERT_PATH_TESTS = Path("tests/utils/web_certs")
WEB_CERT = "web_cert.pem"
WEB_KEY = "web_key.pem"


def replace_cert_in_op(
    hosts: Any, prov: str, cert_name_in_op: str, cert_path_in_tests: str
) -> None:
    cmd_args = [
        os.path.join(PROJECT_DIR, CERT_PATH_TESTS, cert_path_in_tests),
        f"{hosts[prov]["pod-name"]}:{os.path.join(CERT_PATH_OP, cert_name_in_op)}",
    ]
    run_kubectl_command("cp", cmd_args)


def replace_cert_for_one_not_including_s3_in_op(hosts: Any, prov: str) -> None:
    replace_cert_in_op(hosts, prov, WEB_CERT, os.path.join("certs_no_s3", WEB_CERT))
    replace_cert_in_op(hosts, prov, WEB_KEY, os.path.join("certs_no_s3", WEB_KEY))


@wt(
    parsers.parse(
        '{user} replaces web cert for one not including OneS3 domain in "{provider}"'
        " provider"
    )
)
def wt_replace_cert_for_one_not_including_s3_in_op(hosts: Any, provider: str) -> None:
    replace_cert_for_one_not_including_s3_in_op(hosts, provider)
