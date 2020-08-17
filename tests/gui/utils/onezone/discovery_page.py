"""Utils to facilitate operations on discovery page in Onezone gui"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import (Button, NamedButton, WebElement,
                                               WebItemsSequence, Label, WebItem)
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.onezone.generic_page import GenericPage, Element
from tests.gui.utils.common.common import DropdownSelector
from tests.gui.utils.onezone.members_subpage import MembersPage
from tests.gui.utils.onezone.common import InputBox


class WelcomePage(PageObject):
    create_harvester = NamedButton('.info .ember-view',
                                   text='Create a harvester')
    join_existing_harvester = NamedButton('.info .ember-view',
                                          text='join an existing harvester')
    join_group = NamedButton('.info .ember-view', text='join a group')


class Index(PageObject):
    name = id = Label('.one-label')
    progress_value = Label('.progress-table-cell text')


class IndicesPage(PageObject):
    name_input = WebElement('form .row input')
    schema_input = WebElement('form .row textarea')
    create_button = NamedButton('.form-group button .spin-button-label',
                                text='Create')
    indices_list = WebItemsSequence('.content-harvesters-indices .row '
                                    'li.one-collapsible-list-item', cls=Index)
    menu_button = Button('.with-menu .collapsible-toolbar-toggle')


class Harvester(Element):
    menu_button = Button('.collapsible-toolbar-toggle')

    spaces = NamedButton('.one-list-level-2 .item-header',
                         text='Spaces')
    indices = NamedButton('.one-list-level-2 .item-header',
                          text='Indices')
    members = NamedButton('.one-list-level-2 .item-header',
                          text='Members')
    data_discovery = NamedButton('.one-list-level-2 .item-header',
                                 text='Data discovery')


class MenuItem(PageObject):
    name = id = Label('a.clickable')

    def __call__(self):
        self.click()


class Space(PageObject):
    name = id = Label('.one-label')

    menu_button = Button('.collapsible-toolbar-toggle')

    def click_menu(self):
        self.click()
        self.menu_button.click()


class DiscoveryPage(GenericPage):
    add_one_of_your_spaces_button = NamedButton('button',
                                                text='Add one of your spaces')
    invite_space_using_token_button = NamedButton('button',
                                                  text='Invite space using token')

    elements_list = WebItemsSequence('.sidebar-harvesters '
                                     'li.one-list-item.clickable',
                                     cls=Harvester)

    menu = WebItemsSequence('.webui-popover-content '
                            '.one-collapsible-toolbar-popover '
                            '.dropdown-menu .one-collapsible-toolbar-item',
                            cls=MenuItem)

    menu_button = Button('.with-menu .collapsible-toolbar-toggle')

    get_started = Button('.btn.btn-default.hide-sm-active.ember-view')
    create_new_harvester_button = Button('.one-sidebar-toolbar-button'
                                         '.create-harvester-btn')

    name = WebElement('.field-create-name')
    plugin_selector = DropdownSelector('.ember-basic-dropdown')
    endpoint = WebElement('.field-create-endpoint')
    create_button = NamedButton('button', text='Create')

    rename_input = WebElement('.name-editor input')
    rename_button = Button('.save-icon')

    spaces_list = WebItemsSequence('.content-harvesters-spaces '
                                   '.row .list-header-row',
                                   cls=Space)

    input_box = WebItem('.content-info-content-container', cls=InputBox)

    indices_page = WebItem('.main-content', cls=IndicesPage)
    members_page = WebItem('.main-content', cls=MembersPage)

    forbidden_alert = WebElement('.alert.forbidden')

