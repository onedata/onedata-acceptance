"""Utils and fixtures to facilitate operations on spaces page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Input, Button, NamedButton, WebItemsSequence, Label, WebItem
from .common import EditBox, InputBox


class Space(PageObject):
    name = Label('.one-label')
    support_size = Label('.status-toolbar .oneicon-null') #!!!!!!
    support_providers_number = Label('.status-toolbal .oneicon-provider') #!!!!!!!

    overview_button = NamedButton('.one-list-level-2 .item-header', text='Overview') 
    providers_button = NamedButton('.one-list-level-2 .item-header', text='Providers')


class SpaceOverviewPage(PageObject):
    space_name = Label('.header-row .name-editor')
    rename_button = Button('.header-row .oneicon-rename')
    default_space_button = NamedButton('.header-row button', text='Toggle default space')
    leave_space_button = NamedButton('.header-row button', text='Leave space')
    edit_name_box = WebItem('.header-row .name-editor', cls=EditBox)


class SpacesPage(PageObject):
    name = id = Label('.row-heading .col-title')
    get_started_button = NamedButton('.btn-default', text='Get started')

    create_space_button = Button('.oneicon-add-filled')
    join_space_button = Button('.oneicon-join-plug')

    spaces_list = WebItemsSequence('.sidebar-spaces li.one-list-item.clickable', cls=Space)

    input_box = WebItem('.content-info-content-container', cls=InputBox)
    space_overview_page = WebItem('.main-content', cls=SpaceOverviewPage)
    
    #get support button
    #leave_space_modal

    def __getitem__(self, item):
        item = item.lower()
        for space in self.spaces_list:
            if space.name == item:
                return space
        raise RuntimeError('No space named "{}" found in Spaces Page'.format(item))
