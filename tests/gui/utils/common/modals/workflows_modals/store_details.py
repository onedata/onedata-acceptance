"""Utils and fixtures to facilitate operations on Store details modal."""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    AceEditor,
    Button,
    Label,
    WebElement,
    WebElementsSequence,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.onezone.generic_page import Element

from ..modal import Modal


class FilterTab(Element):
    name = id = Label(".column-name")


class StoreDetailsObjectRow(PageObject):
    name = id = Label(".column-object-property")


class StoreDetailsListRow(PageObject):
    name = id = Label(".column-name")
    dataset_name = Button(".dataset-name")
    file_name = Button(".file-name")
    range_start = Label(".column-start")
    range_end = Label(".column-end")
    range_step = Label(".column-step")
    objects_sequence = WebElementsSequence(".column-object-property")
    value = Label(".table-body .column-value")
    path = Label(".column-path .value-container")


class ArrayView(PageObject):
    header = Label(".root-presenter-header")
    items = WebElementsSequence(".array-item .single-line-presenter")


class SingleFileContainer(PageObject):
    name = id = Label(".file-name")
    clickable_name = Button(".file-name")


class StoreDetails(Modal):
    close = Button(".modal-header .close")
    copy_button = Button(".copy-link")
    name_header = WebElement(".modal-header .truncated-string")

    tabs = WebItemsSequence(".nav-tabs .ember-view", cls=FilterTab)
    store_content_list = WebItemsSequence(
        ".entries-table .data-row", cls=StoreDetailsListRow
    )
    store_content_object = WebItemsSequence(
        ".entries-table .data-row", cls=StoreDetailsObjectRow
    )
    raw_view = AceEditor(".value-container-presenter")
    array_view = WebItem(".array-visual-presenter", cls=ArrayView)
    single_file_container = WebItem(
        ".content-container", cls=SingleFileContainer
    )
    close_details = Button(".close-details")

    def __str__(self):
        return "Store details modal"
