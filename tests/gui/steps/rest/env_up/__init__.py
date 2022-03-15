"""This package contains python modules with steps to set up test environment
using REST API
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

# Values of variables depend on settings in gui/backend and
# should be synchronized with them.
# Upload_chunk size is given in MB and UPLOAD_INACTIVITY is given in seconds

GUI_UPLOAD_CHUNK_SIZE = 1
UPLOAD_INACTIVITY_PERIOD_SEC = 60
