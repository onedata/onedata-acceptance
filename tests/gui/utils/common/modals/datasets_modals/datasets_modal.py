"""Utils and fixtures to facilitate operations on datasets modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItemsSequence,
)
from tests.gui.utils.onezone.generic_page import Element

from ..modal import Modal


class ParentDatasetItem(Element):
    name = id = Label(".file-path")
    metadata_protection_toggle = Toggle(".metadata-flag-toggle")
    data_protection_toggle = Toggle(".data-flag-toggle")


class DatasetsModal(Modal):
    establish_dataset = Button(".one-button.btn-primary")
    x = Button(".close")
    data_protection_toggle = Toggle(".direct-dataset-item .data-flag-toggle")
    metadata_protection_toggle = Toggle(
        ".direct-dataset-item .metadata-flag-toggle"
    )
    ancestor_data_protection = Toggle(
        ".parent-group-dataset-item .metadata-flag-toggle"
    )
    ancestor_metadata_protection = Toggle(
        ".parent-group-dataset-item .data-flag-toggle"
    )
    ancestor_option = WebElement(
        ".parent-group-dataset-item .dataset-label-section"
    )
    ancestors = WebItemsSequence(".parent-dataset-item", cls=ParentDatasetItem)
    data_protected_label = Label(".data-protected-tag")
    metadata_protected_label = Label(".metadata-protected-tag")

    def __str__(self):
        return "Datasets modal"
