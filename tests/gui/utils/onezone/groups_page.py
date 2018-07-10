"""Utils to facilitate operations on groups page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               Label, WebItem, WebItemsSequence)
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from .common import EditBox, InputBox


class GroupOverviewPage(PageObject):
    group_name = Label('.header-row .name-editor')
    rename = Button('.header-row .oneicon-rename')
    leave_group = NamedButton('.header-row button',
                              text='Leave group')
    edit_name_box = WebItem('.header-row .name-editor',
                            cls=EditBox)


class GroupsPage(GenericPage):
    elements_list = WebItemsSequence('.sidebar-groups '
                                     'li.one-list-item.clickable', cls=Element)

    create_group = Button('.oneicon-add-filled')
    join_group = Button('.oneicon-join-plug')

    input_box = WebItem('.content-info-content-container', cls=InputBox)
    overview_page = WebItem('.main-content', cls=GroupOverviewPage)

