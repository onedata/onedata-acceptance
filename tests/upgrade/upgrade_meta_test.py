"""This module contains meta test of upgrade procedure"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.upgrade.tests import oneclient_crud, rest_comprehensive, rest_views


def test_upgrade(tests_controller):
    """
    All those tests are interpreted as a one test
    Number of tests depends on a config file
    Procedure of running a test:
    Run all setups -> Upgrade services -> Run all verifies
    """

    tests_controller.add_tests(oneclient_crud.get_tests(tests_controller))
    tests_controller.add_tests(rest_comprehensive.get_tests(tests_controller))
    tests_controller.add_tests(rest_views.get_tests(tests_controller))
    tests_controller.run_tests()
