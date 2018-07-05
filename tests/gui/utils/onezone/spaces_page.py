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
    support_size = Label('.status-toolbar-icon:first-of-type')
    supporting_providers_number = Label('.status-toolbar-icon:last-of-type')

    overview = NamedButton('.one-list-level-2 .item-header',
                           text='Overview')
    providers = NamedButton('.one-list-level-2 .item-header',
                            text='Providers')


class Provider(Element):
    support = Label('.outer-text')


class SpaceOverviewPage(PageObject):
    space_name = Label('.header-row .name-editor')
    rename = Button('.header-row .oneicon-rename')
    set_default_space = NamedButton('.header-row button',
                                    text='Toggle default space')
    leave_space = NamedButton('.header-row button', text='Leave space')
    edit_name_box = WebItem('.header-row .name-editor', cls=EditBox)


class SpaceProvidersPage(PageObject):
    providers_list = WebItemsSequence('.space-providers-list '
                                      'li.one-collapsible-list-item',
                                      cls=Provider)
    get_support = NamedButton('.open-add-storage', text='Get support')


class SpacesPage(GenericPage):
    create_space_button = Button('.oneicon-add-filled')
    join_space_button = Button('.oneicon-join-plug')

    elements_list = WebItemsSequence('.sidebar-spaces '
                                     'li.one-list-item.clickable', cls=Space)

    input_box = WebItem('.content-info-content-container', cls=InputBox)
    overview_page = WebItem('.main-content', cls=SpaceOverviewPage)
