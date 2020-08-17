"""Utils to facilitate operations on spaces page in Onezone gui"""

__author__ = "Michal Stanisz, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from selenium.webdriver import ActionChains
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               WebItemsSequence, Label,
                                               WebItem, WebElement)
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from .common import EditBox, InputBox
from .members_subpage import MembersPage


class Space(Element):
    name = id = Label('.one-label')
    support_size = Label('.status-toolbar-icon:first-of-type')
    supporting_providers_number = Label('.status-toolbar-icon:last-of-type')
    home_icon = WebElement('.status-toolbar-icon:first-of-type span')

    overview = NamedButton('.one-list-level-2 .item-header',
                           text='Overview')
    data = NamedButton('.one-list-level-2 .item-header',
                       text='Data')
    shares = NamedButton('.one-list-level-2 .item-header',
                         text='Shares')
    transfers = NamedButton('.one-list-level-2 .item-header',
                            text='Transfers')
    providers = NamedButton('.one-list-level-2 .item-header',
                            text='Providers')
    members = NamedButton('.one-list-level-2 .item-header',
                          text='Members')
    harvesters = NamedButton('.one-list-level-2 .item-header',
                             text='Harvesters')
    menu_button = Button('.collapsible-toolbar-toggle')

    def click_menu(self):
        self.click()
        self.menu_button.click()

    def is_home_icon(self):
        return 'oneicon-home' in self.home_icon.get_attribute("class")

    def is_active(self):
        return 'active' in self.web_elem.get_attribute('class')


class Provider(Element):
    id = name = Label('.one-label')
    support = Label('.outer-text')
    menu_button = Button('.provider-menu-toggle')


class SpaceInfoTile(PageObject):
    rename = Button('.edit-icon')
    edit_name_box = WebItem('.editor', cls=EditBox)
    shares_count = Label('.shares-count')


class SpaceOverviewPage(PageObject):
    space_name = Label('.with-menu .one-label')
    info_tile = WebItem('.resource-info-tile', cls=SpaceInfoTile)


class WelcomePage(PageObject):
    create_a_space = NamedButton('.info .ember-view', text='Create a space')
    join_an_existing_space = NamedButton('.info .ember-view',
                                         text='join an existing space')
    join_group = NamedButton('.info .ember-view', text='join a group')


class HarvesterRow(Element):
    name = id = Label('.item-name')
    harvester = WebElement('.item-name')
    harvester_menu_button = WebElement('.collapsible-toolbar-toggle')

    def click_harvester_menu_button(self, driver):
        ActionChains(driver).move_to_element(self.harvester).perform()
        self.harvester_menu_button.click()


class HarvestersPage(PageObject):
    harvesters_list = WebItemsSequence(
        '.main-content .one-collapsible-list-item', cls=HarvesterRow)
    add_one_of_harvesters = NamedButton(
        '.add-harvester-to-space-trigger.btn',
        text='Add one of your harvesters')
    invite_harvester_using_token = NamedButton(
        '.generate-invite-token-action.btn',
        text='Invite harvester using token')


class GetSupportPage(PageObject):
    request_support_modal = NamedButton('.nav-link', text='Request support')
    deploy_provider_modal = NamedButton('.nav-link',
                                        text='Deploy your own Oneprovider')
    expose_existing_data_modal = NamedButton('.nav-link',
                                             text='Expose existing data set')

    token_textarea = Label('.active textarea')
    copy = Button('.request-support-tab .copy-btn')
    forbidden_alert = WebElement('.error')


class SpaceProvidersPage(PageObject):
    providers_list = WebItemsSequence('.space-providers-list '
                                      'li.one-collapsible-list-item',
                                      cls=Provider)
    add_support = NamedButton('button', text='Add support')
    get_support_page = WebItem('.ember-view', cls=GetSupportPage)


class _Provider(PageObject):
    name = id = Label('a .tab-name')


class DataPage(GenericPage):
    create_space_button = Button('.one-sidebar-toolbar-button '
                                 '.oneicon-add-filled')

    spaces_header_list = WebItemsSequence('.sidebar-spaces '
                                          'li.one-list-item.clickable '
                                          '.item-header', cls=Space)

    elements_list = WebItemsSequence('.sidebar-spaces '
                                     'li.one-list-item.clickable', cls=Space)

    input_box = WebItem('.content-info-content-container', cls=InputBox)

    overview_page = WebItem('.main-content', cls=SpaceOverviewPage)
    providers_page = WebItem('.main-content', cls=SpaceProvidersPage)
    members_page = WebItem('.main-content', cls=MembersPage)
    welcome_page = WebItem('.main-content', cls=WelcomePage)
    harvesters_page = WebItem('.main-content', cls=HarvestersPage)

    # button in top right corner on all subpages
    menu_button = Button('.with-menu .collapsible-toolbar-toggle')

    get_started = Button('.btn.btn-default.hide-sm-active.ember-view')

    tab_name = Label('.header-row')

    current_provider = Label('.current-oneprovider-name')
    providers = WebItemsSequence('.provider-online', cls=_Provider)
    choose_other_provider = Button('.choose-oneprovider-link')
