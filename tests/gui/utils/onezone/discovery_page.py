"""Utils to facilitate operations on discovery page in Onezone gui"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.web_elements import (Button, NamedButton, WebElement,
                                               WebItemsSequence, Label)
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.onezone.generic_page import GenericPage, Element
from tests.gui.utils.common.common import DropdownSelector


class WelcomePage(PageObject):
    create_harvester = NamedButton('.info .ember-view',
                                   text='Create a harvester')
    join_existing_harvester = NamedButton('.info .ember-view',
                                          text='join an existing harvester')
    join_group = NamedButton('.info .ember-view', text='join a group')


class JoinToHarvester(PageObject):
    join_harvester_button = NamedButton('button', text='Join the harvester')


class Harvester(Element):
    name = id = Label('.one-label')
    menu_button = Button('.collapsible-toolbar-toggle')

    spaces = NamedButton('.one-list-level-2 .item-header',
                         text='Spaces')
    members = NamedButton('.one-list-level-2 .item-header',
                          text='Members')


class MenuItem(PageObject):
    name = id = Label('a.clickable')

    def __call__(self):
        self.click()


class Space(PageObject):
    name = id = Label('.one-label')


class DiscoveryPage(GenericPage):
    create_new_harvester_button = Button('.one-sidebar-toolbar-button'
                                         '.create-harvester-btn')
    join_harvester_button = Button('.join-harvester-btn'
                                   '.one-sidebar-toolbar-button '
                                   '.oneicon-join-plug')

    menu = WebItemsSequence('.webui-popover-content '
                            '.one-collapsible-toolbar-popover '
                            '.dropdown-menu .one-collapsible-toolbar-item',
                            cls=MenuItem)

    get_started = Button('.btn.btn-default.hide-sm-active.ember-view')

    elements_list = WebItemsSequence('.sidebar-harvesters '
                                     'li.one-list-item.clickable',
                                     cls=Harvester)

    name = WebElement('.field-create-name')
    plugin_selector = DropdownSelector('.ember-basic-dropdown')
    endpoint = WebElement('.field-create-endpoint')

    create_button = NamedButton('button', text='Create')

    rename_input = WebElement('.name-editor input')
    rename_button = Button('.save-icon')

    add_space_button = NamedButton('button', text='Add one of your spaces')
    spaces_list = WebItemsSequence('.content-harvesters-spaces '
                                   '.row .header-content-container',
                                   cls=Space)

