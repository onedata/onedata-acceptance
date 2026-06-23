"""This package contains source code for onedata_fs unit tests.
"""
__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os

ROOT_USER = 'root'
TEST_FILE = 'test_onedatafs.py'
TEST_MODULE = 'unit_tests.test_onedatafs'

LOCAL_UNIT_TESTS_DIR = 'tests/onedata_fs/unit_tests'

CONTAINER_ONEDATA_FS_DIR = '/tmp/onedata_fs'
CONTAINER_UNIT_TESTS_DIR = os.path.join(CONTAINER_ONEDATA_FS_DIR, 'unit_tests')
CONTAINER_TEST_CFG_FILE = os.path.join(CONTAINER_UNIT_TESTS_DIR,
                                       'test_cfg.yaml')
CONTAINER_REPORTS_XML_DIR = os.path.join(CONTAINER_UNIT_TESTS_DIR,
                                         'reports/xml')
CONTAINER_TESTS_FILE_PATH = os.path.join(CONTAINER_UNIT_TESTS_DIR, TEST_FILE)


# constants for test_config file keys
SPACE_NAME = 'space-name'
PROVIDER_IP = 'provider-ip'
ACCESS_TOKEN = 'access-token'
