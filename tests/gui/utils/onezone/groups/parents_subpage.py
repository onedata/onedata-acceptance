"""Utils to facilitate operations on groups parents 
subpage page in Onezone gui"""

__author__ = "Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               Label, WebItem, Input,
                                               WebItemsSequence)
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from tests.gui.utils.onezone.common import EditBox, InputBox


class GroupParentsListHeader(PageObject):
    search_bar = Input('input.form-control')
    menu = Button('.collapsible-toolbar-toggle')


class GroupParentsItemRow(PageObject):
    name = id = Label('.one-label')
    menu = Button('.collapsible-toolbar-toggle')


class GroupParentsPage(PageObject):
    header = WebItem('.main-content .sticky-element-container',
                     cls=GroupParentsListHeader)
    items = WebItemsSequence('.main-content > div > ul > li', 
                             cls=GroupParentsItemRow)
