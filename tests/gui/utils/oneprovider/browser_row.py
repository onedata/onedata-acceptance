"""Utils and fixtures to facilitate operation on file row in file, dataset
and archive browsers in oneprovider web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time


class BrowserRow(object):

    def is_selected(self):
        return 'file-selected' in self.web_elem.get_attribute('class')

    def wait_for_selected(self):
        for i in range(30):
            time.sleep(0.1)
            if self.is_selected():
                return

        raise RuntimeError('Waited too long for being selected')
