"""Utils to facilitate operations on uploads page in Onezone gui"""

__author__ = "Emilia Kwolek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               WebItemsSequence, Label,
                                               WebItem, WebElement)
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from .common import EditBox, InputBox


class Provider(Element):
    id = name = Label('.item-name')


class UploadedObject(Element):
    id = name = Label('.upload-object-link')


class UploadedContentPage(PageObject):
    uploaded_items_list = WebItemsSequence('.up-upload-object-info', cls=UploadedObject)


class UploadsPage(GenericPage):
    elements_list = WebItemsSequence('.sidebar-uploads'
                                     ' li.one-list-item.clickable', cls=Provider)
    uploaded_content_page = WebItem('.main-content', cls=UploadedContentPage)
