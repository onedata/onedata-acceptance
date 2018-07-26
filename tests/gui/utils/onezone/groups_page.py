"""Utils to facilitate operations on groups page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               Label, WebItem, WebItemsSequence, Input)
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from .common import EditBox, InputBox

class Group(Element):
    menu = Button('.collapsible-toolbar-toggle')
    members = NamedButton('.one-list-level-2 .item-header', text='Members')
    parents = NamedButton('.one-list-level-2 .item-header', text='Parents')
    edit_box = WebItem('.name-editor', cls=EditBox)

# TODO: Can be removed?
#class GroupOverviewPage(PageObject):
#    group_name = Label('.header-row .name-editor')
#    rename = Button('.header-row .oneicon-rename')
#    leave_group = NamedButton('.header-row button',
#                              text='Leave group')
#    edit_name_box = WebItem('.header-row .name-editor',
#                            cls=EditBox)


class GroupsPage(GenericPage):
    elements_list = WebItemsSequence('.sidebar-groups .one-list .one-list-item.clickable.ember-view', cls=Group)

    create_group = Button('.oneicon-add-filled')
    join_group = Button('.oneicon-join-plug')

    group_menu = WebItemsSequence('div.webui-popover[style*=\'display: block;\'] ul li', cls=Element)

    input_box = WebItem('.content-info-content-container', cls=InputBox) 

    # overview_page = WebItem('.main-content', cls=GroupOverviewPage)

    join_space = Button('.minimized-item.clickable.join-space-action .oneicon-space-join')
    menu_button = Button('.collapsible-toolbar-toggle ')

