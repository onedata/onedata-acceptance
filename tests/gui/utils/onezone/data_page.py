"""Utils to facilitate operations on spaces page in Onezone gui"""

__author__ = "Michal Stanisz, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

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
    menu_button = Button('.collapsible-toolbar-toggle')

    def click_menu(self):
        self.click()
        self.menu_button.click()

    def is_home_icon(self):
        return 'oneicon-home' in self.home_icon.get_attribute("class")


class Provider(Element):
    support = Label('.outer-text')


class SpaceOverviewPage(PageObject):
    space_name = Label('.with-menu .one-label')
    rename = Button('.edit-icon')
    edit_name_box = WebItem('.editor', cls=EditBox)


class WelcomePage(PageObject):
    create_a_space = NamedButton('.info .ember-view', text='Create a space')
    join_an_existing_space = NamedButton('.info .ember-view',
                                         text='join an existing space')
    join_group = NamedButton('.info .ember-view', text='join a group')


class GetSupportPage(PageObject):
    request_support_modal = NamedButton('.nav-link', text='Request support')
    deploy_provider_modal = NamedButton('.nav-link',
                                        text='Deploy your own Oneprovider')
    expose_existing_data_modal = NamedButton('.nav-link',
                                             text='Expose existing data set')

    token_textarea = Label('.active textarea')
    copy = NamedButton('.copy-btn', text='Copy')
    generate_another_token = NamedButton('.active .btn-get-token',
                                         text='Generate another token')
    forbidden_alert = WebElement('.alert.forbidden')


class SpaceProvidersPage(PageObject):
    providers_list = WebItemsSequence('.space-providers-list '
                                      'li.one-collapsible-list-item',
                                      cls=Provider)
    add_support = NamedButton('button', text='Add support')
    get_support_page = WebItem('.ember-view', cls=GetSupportPage)


class MenuItem(PageObject):
    name = id = Label('a.clickable .text')

    def __call__(self):
        self.click()


class _Provider(PageObject):
    name = id = Label('a .tab-name')


class DataPage(GenericPage):
    create_space_button = Button('.one-sidebar-toolbar-button '
                                 '.oneicon-add-filled')
    join_space_button = Button('.oneicon-join-plug')
    join_harvester_button = NamedButton('button span.spin-button-label',
                                        text='Join the harvester')

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

    menu_button = Button('.with-menu .collapsible-toolbar-toggle')

    get_started = Button('.btn.btn-default.hide-sm-active.ember-view')

    left_menu = WebItemsSequence('.webui-popover-content '
                                 '.one-collapsible-toolbar-popover '
                                 '.dropdown-menu .one-collapsible-toolbar-item',
                                 cls=MenuItem)

    tab_name = Label('.header-row')

    current_provider = Label('.current-oneprovider-name')
    providers = WebItemsSequence('.provider-online', cls=_Provider)
    choose_other_provider = Button('.choose-oneprovider-link')

