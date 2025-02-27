"""This module contains meta test of upgrade procedure"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import tests.upgrade.tests.oneclient_CRUD as oneclient_CRUD
import tests.upgrade.tests.rest_shares as rest_shares
import tests.upgrade.tests.rest_views as rest_views


def test_upgrade(tests_controller):
    """
    All that tests are interpreted as one test
    Number of tests depends on config file
    Procedure of running test:
    Run all setups -> Upgrade services -> Run all verifies
    """

    tests_controller.add_tests(oneclient_CRUD.get_tests(tests_controller))
    tests_controller.add_tests(rest_shares.get_tests(tests_controller))
    tests_controller.add_tests(rest_views.get_tests(tests_controller))
    tests_controller.run_tests()
