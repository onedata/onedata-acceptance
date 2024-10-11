"""This module contains gherkin steps to check if all workflows are used
in acc tests.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

import os

from tests.utils.bdd_utils import parsers, wt

WORKFLOW_DIR = "automation-examples/workflows"
TESTS_DIR = "tests/gui/features"
WORKFLOWS_NAMES = []


@wt(parsers.parse("workflows from automation-examples are gathered"))
def gather_workflows_names():
    global WORKFLOWS_NAMES
    workflows_names = []
    for _, _, files in os.walk(WORKFLOW_DIR):
        workflows_names.extend(filter(lambda x: x.endswith(".json"), files))
    WORKFLOWS_NAMES = workflows_names


@wt(parsers.parse("all gathered workflows are used in acceptance tests"))
def check_using_all_workflows():
    workflows_names = WORKFLOWS_NAMES
    # remove extension
    workflows_names = set(map(lambda x: x.split(".")[0], workflows_names))
    used_workflows = set()
    for dir_path, _, files in os.walk(TESTS_DIR):
        for file in files:
            used_workflows.update(
                check_names_in_file(
                    os.path.join(dir_path, file), workflows_names
                )
            )
    err_msg = (
        "there are workflows not included in tests: "
        f"{workflows_names.difference(used_workflows)}"
    )
    assert workflows_names == used_workflows, err_msg


def check_names_in_file(path, names):
    detected_names = set()
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            words = line.split(" ")
            words = set(map(lambda x: x.replace('"', ""), words))
            detected_names.update(words.intersection(names))
    return detected_names
