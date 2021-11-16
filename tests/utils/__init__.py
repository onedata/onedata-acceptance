"""This package contains modules with utility functions for oneclient tests.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os

CLIENT_POD_LOGS_DIR = '/tmp/logs'
RPYC_LOGS_DIR = os.path.join(CLIENT_POD_LOGS_DIR, 'rpyc_logs')
ONECLIENT_LOGS_DIR = os.path.join(CLIENT_POD_LOGS_DIR, 'oc_logs')
ONECLIENT_MOUNT_DIR = '/tmp/onedata/mnt'
