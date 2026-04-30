"""Utils to facilitate operations on endpoints in API reference page of Onedata.org website"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


class EndpointInfo:
    def __init__(self, method, name):
        self.method = method
        self.name = name
        self.label = f"{self.method} {self.name}"
