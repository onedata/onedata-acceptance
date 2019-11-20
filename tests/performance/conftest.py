"""This module contains definitions of pytest fixtures that are used in
performance tests of onedata.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import inspect

import yaml

from tests import *
from tests.utils.path_utils import get_file_name
from tests.utils.git_utils import get_branch_name, get_commit, get_repository
from tests.utils.performance_utils import *
from tests.utils.utils import get_copyright, get_authors, get_suite_description


@pytest.fixture(scope='session')
def yaml_output(request):
    performance_report = PerformanceReport('performance', get_repository(),
                                           get_commit(), get_branch_name())

    def fin():
        if not os.path.exists(PERFORMANCE_LOGDIR):
            os.makedirs(PERFORMANCE_LOGDIR)
        f = open(PERFORMANCE_OUTPUT, 'w')
        f.write(yaml.safe_dump(performance_report.report))

    request.addfinalizer(fin)
    return performance_report


class AbstractPerformanceTest:
    @pytest.fixture(scope='module')
    def suite_report(self, request, env_report):
        module = inspect.getmodule(self.__class__)
        name = get_file_name(inspect.getfile(self.__class__))
        report = SuiteReport(name, get_suite_description(module),
                             get_copyright(module), get_authors(module))

        def fin():
            env_report.add_to_report('suites', report)

        request.addfinalizer(fin)
        return report

    @pytest.fixture(scope='module')
    def env_report(self, request, yaml_output, env_description_abs_path):
        name = env_description_abs_path.split(os.path.sep)[-1]
        report = EnvironmentReport(name)

        def fin():
            yaml_output.add_to_report('envs', report)

        request.addfinalizer(fin)
        return report
