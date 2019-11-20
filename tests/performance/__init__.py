"""Package with performance tests of onedata.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from collections import namedtuple

CLIENT_CONF = namedtuple('ClientConf', ['user', 'mount_path', 'client_host',
                                        'client_instance', 'token'])
