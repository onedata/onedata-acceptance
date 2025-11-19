"""This module contains utility functions for web certificates."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from pathlib import Path

from tests import PROJECT_DIR
from tests.utils.bdd_utils import parsers, wt
from tests.utils.environment_utils import run_kubectl_command

CERT_PATH_OP = Path("/etc/op_panel/certs")
CERT_PATH_TESTS = Path("tests/utils/web_certs")
WEB_CERT = "web_cert.pem"
WEB_KEY = "web_key.pem"


def replace_cert_in_op(hosts, prov, cert_name_in_op, cert_path_in_tests):
    cmd_args = [
        os.path.join(PROJECT_DIR, CERT_PATH_TESTS, cert_path_in_tests),
        f"{hosts[prov]["pod-name"]}:{os.path.join(CERT_PATH_OP, cert_name_in_op)}",
    ]
    run_kubectl_command("cp", cmd_args)


def replace_certs_for_ones_not_including_s3_in_op(hosts, prov):
    replace_cert_in_op(hosts, prov, WEB_CERT, os.path.join("certs_no_s3", WEB_CERT))
    replace_cert_in_op(hosts, prov, WEB_KEY, os.path.join("certs_no_s3", WEB_KEY))


@wt(
    parsers.parse(
        '{user} replaces web certs for ones not including oneS3 domain in "{provider}"'
        " provider"
    )
)
def wt_replace_certs_for_ones_not_including_s3_in_op(hosts, provider):
    replace_certs_for_ones_not_including_s3_in_op(hosts, provider)
