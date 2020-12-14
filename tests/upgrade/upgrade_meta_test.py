""" This module contains meta test of upgrade procedure
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os
import tests.upgrade.tests.oneclient_CRUD as oneclient_CRUD


def test_upgrade(tests_controller):
    tests_controller.add_test("oneclient CRUD test",
                              oneclient_CRUD.setup("space1"), oneclient_CRUD.verify("space1"))
    tests_controller.add_test("oneclient CRUD test",
                              oneclient_CRUD.setup("space3"), oneclient_CRUD.verify("space3"))
    tests_controller.run_tests()
