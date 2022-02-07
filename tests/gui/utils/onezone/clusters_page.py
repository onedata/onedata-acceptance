"""Utils to facilitate operations on clusters page in Onezone gui"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.onezone.generic_page import GenericPage
from tests.gui.utils.core.web_elements import (Button, NamedButton, WebItem,
                                               Label, WebItemsSequence,
                                               WebElement)
from tests.gui.utils.core.base import PageObject


class TokenPage(PageObject):
    copy = Button('.copy-btn')


class MenuItem(PageObject):
    name = id = Label('.item-name')
    status_icon = WebElement('.sidebar-item-icon')
    menu_button = Button('.btn-toolbar')

    # conflicted clusters have 4-letter cluster id hash added to label
    id_hash = Label('.conflict-label')

    def __call__(self):
        self.click()

    def is_not_working(self):
        return 'error' in self.status_icon.get_attribute('class')

    def is_working(self):
        return not self.is_not_working()


class SubmenuItem(PageObject):
    name = id = Label('.one-label')

    def __call__(self):
        self.click()


class ClustersPage(GenericPage):
    add_new_provider_cluster = Button('.add-cluster-btn')

    token_page = WebItem('.main-content', cls=TokenPage)

    menu_button = Button('.with-menu .collapsible-toolbar-toggle')
    menu = WebItemsSequence('.sidebar-clusters .two-level-sidebar '
                            '.one-list-item.resource-item', cls=MenuItem)
    submenu = WebItemsSequence('.second-level-items .item-header',
                               cls=SubmenuItem)

    deregister_label = Button('.text-danger')
    deregister_provider = Button('.btn-danger.btn-deregister-provider')
    deregistration_checkbox = Button('.text-understand')
    confirm_deregistration = Button('.btn-danger.btn-deregister')

    modify_provider_details = Button('.collapsible-toolbar-buttons '
                                     '.btn-modify-provider')
    confirm_modify_provider_details = NamedButton('button',
                                                  text='Modify provider details')

