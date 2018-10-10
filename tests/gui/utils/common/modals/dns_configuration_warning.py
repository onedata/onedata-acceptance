"""Utils and fixtures to facilitate operations on modal shown after proceed DNS
configuration with warning.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton
from .modal import Modal


class DNSConfigurationWarningModal(Modal):
    yes = NamedButton('button', text='Yes, proceed')
    no = NamedButton('button', text='No, review setup')

    def __str__(self):
        return 'DNS configuration warning modal'
