"""Utils and fixtures to facilitate operations on groups page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Input, Button, NamedButton, WebItemsSequence, Label, WebItem
from .common import EditBox, InputBox


class Group(PageObject):
    name = Label('.one-label')
    support_size = Label('.status-toolbar .oneicon-null') #!!!!!!
    support_providers_number = Label('.status-toolbal .oneicon-provider') #!!!!!!!


class GroupOverviewPage(PageObject):
    group_name = Label('.header-row .name-editor')
    rename_button = Button('.header-row .oneicon-rename')
    leave_group_button = NamedButton('.header-row button', text='Leave group')
    edit_name_box = WebItem('.header-row .name-editor', cls=EditBox)


class GroupsPage(PageObject):
    name = id = Label('.row-heading .col-title')
    get_started_button = NamedButton('.btn-default', text='Get started')

    create_group_button = Button('.oneicon-add-filled')
    join_group_button = Button('.oneicon-join-plug')

    groups_list = WebItemsSequence('.sidebar-groups li.one-list-item.clickable', cls=Group)

    input_box = WebItem('.content-info-content-container', cls=InputBox)
    group_overview_page = WebItem('.main-content', cls=GroupOverviewPage)

    def __getitem__(self, item):
        item = item.lower()
        for group in self.groups_list:
            if group.name == item:
                return group
        raise RuntimeError('No group named "{}" found in Groups Page'.format(item))
