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

    join_cluster = Button('.join-cluster-btn')

    token_page = WebItem('.main-content', cls=TokenPage)

    menu_button = Button('.with-menu .collapsible-toolbar-toggle')

    menu = WebItemsSequence('.two-level-sidebar.sidebar-clusters '
                            '.one-list-wrapper .one-label',
                            cls=MenuItem)
    submenu = WebItemsSequence('.second-level-items .item-header',
                               cls=SubmenuItem)

    deregister_provider = Button('.btn-danger.btn-deregister-provider')
    modify_provider_details = Button('.collapsible-toolbar-buttons '
                                     '.btn-modify-provider')
    confirm_modify_provider_details = NamedButton('button span',
                                                  text='Modify provider details')

    deregistration_checkbox = Button('.text-understand')
    confirm_deregistration = Button('.btn-danger.btn-deregister')

    join_cluster_token_input = WebElement('.join-cluster-token')
    join_the_cluster = NamedButton('button .spin-button-label',
                                   text='Join the cluster')

