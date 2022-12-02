"""Utils to facilitate operations on groups members 
subpage page in Onezone gui"""

__author__ = "Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from selenium.webdriver import ActionChains

from tests.gui.utils.common.privilege_tree import PrivilegeTree
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               Label, WebItem, Input,
                                               WebItemsSequence, WebElement,
                                               WebElementsSequence)


class MembersHeaderRow(PageObject):
    checkbox = Button('div.item-checkbox')
    search_bar = Input('input.form-control')
    menu_button = Button('li.list-header-row '
                         '.collapsible-toolbar-toggle.btn-menu-toggle')


class MembersItemHeader(PageObject):
    checkbox = Button('div.item-checkbox')
    user = WebElement('.header-content-container')
    menu_button = Button('.collapsible-toolbar-toggle')
    save_button = NamedButton('.save-btn', text='Save')
    discard_button = NamedButton('.discard-btn', text='Discard changes')

    def click_menu(self, driver):
        ActionChains(driver).move_to_element(self.user).perform()
        self.menu_button.click()


class MembersItemRow(PageObject):
    header = WebItem('.list-header-row', cls=MembersItemHeader)
    name = id = Label('.record-name-general')
    privilege_tree = WebItem('.one-tree', cls=PrivilegeTree)
    forbidden_alert = WebElement('.alert.forbidden')
    status_labels = WebElementsSequence('.label')
    ownership_warning = WebElement('.privileges-of-owner-warning')

    member = WebElement('.list-header-row')
    member_menu_button = WebElement('.collapsible-toolbar-toggle')

    def click_member_menu_button(self, driver):
        ActionChains(driver).move_to_element(self.member).perform()
        self.member_menu_button.click()

    def are_privileges_visible(self):
        try:
            return self.privilege_tree
        except RuntimeError:
            return False

    def has_status_label(self, name):
        return any(x.text == name for x in self.status_labels)

    def is_opened(self):
        return 'active' in self.web_elem.get_attribute('class')


class MembersItemRowUsers(MembersItemRow):
    name = id = Label('.user-info-with-icon .user-fullname')


class MembersList(PageObject):
    header = WebItem('li.list-header-row', cls=MembersHeaderRow)
    items = WebItemsSequence('.one-collapsible-list-item',
                             cls=MembersItemRow)
    generate_token = NamedButton('a', text='generate an invitation token')


class MembersUserList(MembersList):
    items = WebItemsSequence('.one-collapsible-list-item',
                             cls=MembersItemRowUsers)


class MembershipElement(PageObject):
    name = id = Label('.record-name')


class MembershipRelation(PageObject):
    line = id = WebElement('.line')
    relation_menu_button = Button('.actions-trigger')

    def click_relation_menu_button(self, driver):
        ActionChains(driver).move_to_element(self.line).perform()
        self.relation_menu_button()


class MembershipRow(PageObject):
    name = id = Label('div')
    elements = WebItemsSequence('.membership-row-element.membership-block',
                                cls=MembershipElement)
    relations = WebItemsSequence('.membership-row-element.membership-relation',
                                 cls=MembershipRelation)


class InvitationTokenArea(PageObject):
    token = Input('textarea')
    copy = NamedButton('button', text='Copy')
    generate = Button('.btn-get-token')
    close = Button('.oneicon-close')


class MembersPage(PageObject):
    groups = WebItem('.group-list', cls=MembersList)
    users = WebItem('.user-list', cls=MembersUserList)
    token = WebItem('.invitation-token-presenter', cls=InvitationTokenArea)
    show_view_option = Button('.view-tools-toggle')
    effective_button = NamedButton('.direct-selector button', text='Effective')
    memberships_button = NamedButton('.mode-selector button', text='Memberships')
    memberships = WebItemsSequence('.membership-visualiser .membership-row',
                                   cls=MembershipRow)

    forbidden_alert = WebElement('.alert.forbidden')
    bulk_edit_button = NamedButton('.btn', text='Bulk edit')

    def close_member(self, driver):
        driver.execute_script("window.scrollBy(0,0)")
        driver.find_element_by_css_selector('.member-item '
                                            '.one-collapsible-list-item-header'
                                            '.opened').click()

