"""Utils to facilitate operations on spaces page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               WebItemsSequence, Label,
                                               WebItem)
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from .common import EditBox, InputBox


class Space(Element):
    name = id = Label('.one-label')
    support_size = Label('.status-toolbar-icon:first-of-type')
    supporting_providers_number = Label('.status-toolbar-icon:last-of-type')

    overview = NamedButton('.one-list-level-2 .item-header',
                           text='Overview')
    providers = NamedButton('.one-list-level-2 .item-header',
                            text='Providers')
    members = NamedButton('.one-list-level-2 .item-header',
                          text='Members')


class Provider(Element):
    support = Label('.outer-text')


class SpaceOverviewPage(PageObject):
    space_name = Label('.header-row .name-editor')
    rename = Button('.header-row .oneicon-rename')
    set_default_space = NamedButton('.header-row button',
                                    text='Toggle default space')
    leave_space = NamedButton('.header-row button', text='Leave space')
    edit_name_box = WebItem('.header-row .name-editor', cls=EditBox)


class WelcomePage(PageObject):
    create_a_space = NamedButton('.info .ember-view', text='Create a space')
    join_existing_space = NamedButton('.info .ember-view', text='join an existing space')
    join_group = NamedButton('.info .ember-view', text='join a group')


class GetSupportPage(PageObject):
    request_support_modal = NamedButton('.nav-link', text='Request support')
    deploy_provider_modal = NamedButton('.nav-link', text='Deploy your own provider')
    expose_existing_data_modal = NamedButton('.nav-link', text='Expose existing data collection')

    token_textarea = Label('.active textarea')
    copy_button = NamedButton('.tab-pane.active .copy-btn', text='Copy')
    generate_another_token = NamedButton('.active .btn-get-token', text='Generate another token')


class SpaceProvidersPage(PageObject):
    providers_list = WebItemsSequence('.space-providers-list '
                                      'li.one-collapsible-list-item',
                                      cls=Provider)
    get_support = NamedButton('button', text='Get support')
    get_support_page = WebItem('.ember-view', cls=GetSupportPage)


class SpaceMembersPage(PageObject):
    menu_button = Button('.collapsible-toolbar-toggle')
    input_box = WebItem('.invitation-token-presenter', cls=InputBox)


class SpacesPage(GenericPage):
    create_space_button = Button('.oneicon-add-filled')
    join_space_button = Button('.oneicon-join-plug')

    elements_list = WebItemsSequence('.sidebar-spaces '
                                     'li.one-list-item.clickable', cls=Space)

    input_box = WebItem('.content-info-content-container', cls=InputBox)

    overview_page = WebItem('.main-content', cls=SpaceOverviewPage)
    providers_page = WebItem('.main-content', cls=SpaceProvidersPage)
    members_page = WebItem('.main-content', cls=SpaceMembersPage)
    welcome_page = WebItem('.main-content', cls=WelcomePage)

    invite_user = Button('.minimized-item.clickable.invite-user .oneicon-user-add')
    invite_group = Button('.minimized-item.clickable.invite-group .oneicon-group-invite')
    get_started = Button('.btn.btn-default.hide-sm-active.ember-view')
