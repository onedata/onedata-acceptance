"""Utils and fixtures to facilitate operations on datasets modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from .modal import Modal
from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.web_elements import (Button, WebElement,
                                               WebItemsSequence, Label)
from tests.gui.utils.onezone.generic_page import Element


class ParentDatasetItem(Element):
    name = id = Label('.azure')
    metadata_protection_toggle = Toggle('.metadata-flag-toggle')
    data_protection_toggle = Toggle('.data-flag-toggle')


class DatasetsModal(Modal):
    dataset_toggle = Toggle('.toggle-header .one-way-toggle-track')
    close = Button('.close-btn')
    data_protection_toggle = Toggle('.direct-dataset-item .data-flag-toggle'
                                    ' .one-way-toggle-track')
    metadata_protection_toggle = Toggle('.direct-dataset-item '
                                        '.metadata-flag-toggle '
                                        '.one-way-toggle-track')
    ancestor_data_protection = Toggle('.parent-group-dataset-item '
                                      '.metadata-flag-toggle')
    ancestor_metadata_protection = Toggle('.parent-group-dataset-item'
                                          ' .data-flag-toggle')
    ancestor_option = WebElement('.parent-group-dataset-item '
                                 '.dataset-label-section')
    ancestors = WebItemsSequence('.parent-dataset-item', cls=ParentDatasetItem)

    def __str__(self):
        return 'Datasets modal'

