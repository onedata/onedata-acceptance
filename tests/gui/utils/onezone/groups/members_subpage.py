"""Utils to facilitate operations on groups members 
subpage page in Onezone gui"""

__author__ = "Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               Label, WebItem, Input,
                                               WebItemsSequence)


class GroupMembersHeaderRow(PageObject):
    checkbox = Button('div.item-checkbox')
    search_bar = Input('input.form-control')


class GroupMembersItemHeader(PageObject):
    checkbox = Button('div.item-checkbox')
    menu_button = Button('.collapsible-toolbar-toggle')
    save_button = NamedButton('.btn-toolbar .btn-sm', text='Save')
    reset_button = NamedButton('.btn-toolbar .btn-danger', text='Reset')


class Privilege(PageObject):
    name = id = Label('label')
    toggle = Button('.one-way-toggle-control')


class PrivilegeGroup(PageObject):
    name = id = Label('div.tree-item-content-container > '
                      'div.one-tree-item-content > label')
    toggle = Button('div.tree-item-content-container > '
                    'div.one-tree-item-content > div > div > '
                    'div.one-way-toggle-control')
    privileges = WebItemsSequence('div > div.one-tree > ul > li', cls=Privilege)
    show_hide_button = Button('.tree-circle')

    def __call__(self):
        self.show_hide_button.click()


class GroupMembersItemRow(PageObject):
    header = WebItem('.list-header-row', cls=GroupMembersItemHeader)
    name = id = Label('.one-label')
    privileges = WebItemsSequence('.one-collapsible-list-item-content '
                                  '.form.ember-view > div > ul > li', 
                                  cls=PrivilegeGroup)


class GroupMembersList(PageObject):
    header = WebItem('li.list-header-row', cls=GroupMembersHeaderRow)
    items = WebItemsSequence('.one-collapsible-list-item', 
                             cls=GroupMembersItemRow)
    generate_token = NamedButton('a', text='generate an invitation token')


class InvitationTokenArea(PageObject):
    token = Input('textarea')
    copy = NamedButton('button', text='Copy')
    generate = Button('.btn-get-token')
    close = Button('.oneicon-close')


class GroupMembersPage(PageObject):
    groups = WebItem('.row:nth-of-type(2) > ul', cls=GroupMembersList)
    users = WebItem('.row:nth-of-type(3) > ul', cls=GroupMembersList)
    token = WebItem('.invitation-token-presenter', cls=InvitationTokenArea)


