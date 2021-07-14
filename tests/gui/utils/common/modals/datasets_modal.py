"""Utils and fixtures to facilitate operations on datasets modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from .modal import Modal
from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.web_elements import Button


class DatasetsModal(Modal):
    dataset_toggle = Toggle('.toggle-header .one-way-toggle-track')
    dataset_close_button = Button('.close-btn')

    def __str__(self):
        return 'Datasets modal'

