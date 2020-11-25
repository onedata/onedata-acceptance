"""Utils to facilitate operations on discovery page in Onezone gui"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import (
    Button, NamedButton, WebElement, WebItemsSequence, Label, WebItem, Input)
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.onezone.generic_page import GenericPage, Element
from tests.gui.utils.common.common import DropdownSelector, Toggle
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
    name_input = Input('.name-field .form-control')
    schema_input = Input('.schema-field .form-control')
    create_button = Button('.create-btn')
    indices_list = WebItemsSequence('.content-harvesters-indices .row '
                                    'li.one-collapsible-list-item', cls=Index)
    menu_button = Button('.with-menu .collapsible-toolbar-toggle')


class GeneralTab(PageObject):
    edit_button = NamedButton('.edit-btn', text='Edit')
    save_button = NamedButton('.submit-btn', text='Save')
    copy_public_url = Button('.publicUrl-field .copy-btn')


class GUIPluginIndex(PageObject):
    plugin_index = id = Label('.row-header')
    harvester_index = Label('.index-info')


class GUIPluginTab(PageObject):
    gui_status = Label('.gui-status')

    upload_file_input = WebElement('.upload-gui-input')
    upload_button = Button('.upload-button')

    injected_config = Label('.json-editor-textarea')
    version = Label('.gui-version')
    indices = WebItemsSequence('.indices-table tbody tr', cls=GUIPluginIndex)


class ConfigurationPage(PageObject):
    public = Toggle('.one-way-toggle')

    general_tab = WebItem('.content-harvesters-config', cls=GeneralTab)
    gui_plugin_tab = WebItem('.content-harvesters-config', cls=GUIPluginTab)

    general_button = NamedButton('.nav-link', text='General')
    gui_plugin_button = NamedButton('.nav-link', text='GUI plugin')


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
    configuration = NamedButton('.one-list-level-2 .item-header',
                                text='Configuration')


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

    name = WebElement('.name-field .form-control')
    plugin_selector = DropdownSelector('.type-field')
    endpoint = WebElement('.endpoint-field .form-control')
    create_button = NamedButton('.submit-btn', text='Create')

    rename_input = WebElement('.name-editor input')
    rename_button = Button('.save-icon')

    spaces_list = WebItemsSequence('.content-harvesters-spaces '
                                   '.row .list-header-row',
                                   cls=Space)

    input_box = WebItem('.content-info-content-container', cls=InputBox)

    indices_page = WebItem('.main-content', cls=IndicesPage)
    members_page = WebItem('.main-content', cls=MembersPage)
    configuration_page = WebItem('.main-content', cls=ConfigurationPage)

    forbidden_alert = WebElement('.alert.forbidden')

