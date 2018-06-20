"""Utils and fixtures to facilitate operations on tokens page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Input, Button, NamedButton, WebItemsSequence, Label, WebItem
from .common import EditBox, InputBox


class Token(PageObject):
    name = Label('.one-label')
    support_size = Label('.status-toolbar .oneicon-null') #!!!!!!
    support_providers_number = Label('.status-toolbal .oneicon-provider') #!!!!!!!

    overview_button = NamedButton('.one-list-level-2 .item-header', text='Overview')
    providers_button = NamedButton('.one-list-level-2 .item-header', text='Providers')


class TokensPage(PageObject):
    name = id = Label('.row-heading .col-title')
    get_started_button = NamedButton('.btn-default', text='Get started')

    create_token_button = Button('.oneicon-add-filled')

    tokens_list = WebItemsSequence('.sidebar-tokens li.one-list-item.clickable', cls=Token)

    input_box = WebItem('.content-info-content-container', cls=InputBox)
    remove_token_button = NamedButton('.header-row button', text='Remove')
    
    #copy token button

    def __getitem__(self, item):
        item = item.lower()
        for token in self.tokens_list:
            if token.name == item:
                return token
        raise RuntimeError('No token named "{}" found in Tokens Page'.format(item))
