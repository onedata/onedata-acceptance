"""Utils to facilitate operations on clusters page in Onezone gui"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.onezone.generic_page import GenericPage
from tests.gui.utils.core.web_elements import Button, NamedButton, WebItem, \
    Label, WebItemsSequence
from tests.gui.utils.core.base import PageObject


class TokenPage(PageObject):
    copy = NamedButton('button', text='Copy')


class MenuItem(PageObject):
    name = id = Label('.item-name')

    def __call__(self):
        self.click()


class SubmenuItem(PageObject):
    name = id = Label('.one-label')

    def __call__(self):
        self.click()


class ClustersPage(GenericPage):
    add_new_provider_cluster = Button('.add-cluster-btn')

    token_page = WebItem('.main-content', cls=TokenPage)

    menu_button = Button('.with-menu .collapsible-toolbar-toggle')

    menu = WebItemsSequence('.two-level-sidebar.sidebar-clusters '
                            '.one-list-wrapper .one-label',
                            cls=MenuItem)
    submenu = WebItemsSequence('.second-level-items .item-header',
                               cls=SubmenuItem)

    deregistration_checkbox = Button('.text-understand')
    deregistration_button = Button('.btn-danger.btn-deregister')
