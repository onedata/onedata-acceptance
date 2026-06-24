"""This module contains definitions of pytest fixtures that are used in
performance tests of onedata.
"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import inspect
import os
from collections.abc import Mapping
from typing import cast

import pytest
import yaml

from tests import LOGDIRS, PERFORMANCE_LOGDIR
from tests.conftest import export_logs, get_test_type, make_logdir
from tests.types import (
    EnvDesc,
    Hosts,
    Users,
)
from tests.utils.client_utils import Client
from tests.utils.git_utils import get_branch_name, get_commit, get_repository
from tests.utils.path_utils import get_file_name
from tests.utils.performance_utils import (
    EnvironmentReport,
    PerformanceReport,
    SuiteReport,
)
from tests.utils.user_utils import CORRECT_TOKEN
from tests.utils.utils import get_authors, get_copyright, get_suite_description


@pytest.fixture(scope="session")
def yaml_output(request: pytest.FixtureRequest) -> PerformanceReport:
    performance_report = PerformanceReport(
        "performance",
        get_repository().decode(),
        get_commit().decode(),
        get_branch_name().decode(),
    )

    def fin() -> None:
        if not os.path.exists(PERFORMANCE_LOGDIR):
            os.makedirs(PERFORMANCE_LOGDIR)
        logdir = make_logdir(LOGDIRS.get(get_test_type(request)), "report")
        with open(os.path.join(logdir, "performance.yaml"), "w") as report_file:
            report_file.write(yaml.safe_dump(performance_report.report))
        export_logs(request)

    request.addfinalizer(fin)
    return performance_report


class AbstractPerformanceTest:
    @pytest.fixture(scope="module")
    def suite_report(
        self, request: pytest.FixtureRequest, env_report: EnvironmentReport
    ) -> SuiteReport:
        module = inspect.getmodule(self.__class__)
        if module is None:
            raise ValueError(f"Cannot determine module for {self.__class__.__name__}")
        name = get_file_name(inspect.getfile(self.__class__))
        report = SuiteReport(
            name,
            get_suite_description(module) or "",
            get_copyright(module),
            get_authors(module),
        )

        def fin() -> None:
            env_report.add_to_report("suites", report)

        request.addfinalizer(fin)
        return report

    @pytest.fixture(scope="module")
    def env_report(
        self,
        request: pytest.FixtureRequest,
        yaml_output: PerformanceReport,
        env_description_abs_path: str,
    ) -> EnvironmentReport:
        name = env_description_abs_path.split(os.path.sep)[-1]
        report = EnvironmentReport(name)

        def fin() -> None:
            yaml_output.add_to_report("envs", report)

        request.addfinalizer(fin)
        return report


def mount_performance_client(
    users: Users,
    hosts: Hosts,
    env_desc: EnvDesc,
    username: str,
    client_host: str,
    client_id: str,
) -> Client:
    client = users[username].mount_client(
        client_host,
        client_id,
        cast(Mapping[str, Mapping[str, str]], hosts),
        env_desc,
        CORRECT_TOKEN,
    )
    if client is None:
        raise RuntimeError(f"Failed to mount {client_id} for {username}")
    return client
