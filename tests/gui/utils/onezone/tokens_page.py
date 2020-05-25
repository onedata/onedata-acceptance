"""Utils to facilitate operations on tokens page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button, NamedButton, WebItemsSequence, Label, Input, WebElement, WebItem)
from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import Element, GenericPage


class TokenRow(PageObject):
    id = name = Label('.item-name')
    menu_button = Button('.token-menu-trigger')
    icon = WebElement('.one-icon')

    def is_type_of(self, exp_type):
        return exp_type in self.icon.get_attribute('class')

    def is_revoked(self):
        return 'inactive' in self.web_elem.get_attribute('class')

    def __str__(self):
        return 'Tokens row'


class TokenFilter(PageObject):
    all = Button('.btn-all')
    access = Button('.btn-access')
    identity = Button('.btn-identity')
    invite = Button('.btn-invite')


class TokensSidebar(PageObject):
    create_new_token = Button('.one-sidebar-toolbar-button .oneicon-add-filled')
    tokens = WebItemsSequence('.token-item', cls=TokenRow)
    consume_token = Button('.oneicon-consume-token')
    filter = WebItem('.filter-control', cls=TokenFilter)

    name_input = Input('.one-list-wrapper .form-control')
    confirm = Button('.save-icon')
    discard = Button('.cancel-icon')

    def __str__(self):
        return 'Tokens sidebar'


class InviteType(PageObject):
    name = id = Label('.text')


class CreateNewTokenPage(PageObject):
    create_token = NamedButton('.submit-token', text='Create token')
    access_option = WebElement('.option-access .one-way-radio-control')
    identity_option = WebElement('.option-identity .one-way-radio-control')
    invite_option = WebElement('.option-invite .one-way-radio-control')

    token_name_input = WebItem('.name-field .field-component', cls=InputBox)

    invite_types = WebItemsSequence('.ember-power-select-option', cls=InviteType)
    invite_type = WebElement('.inviteType-field .dropdown-field-trigger')

    def __str__(self):
        return 'Create new token page'

    def expand_invite_type_dropdown(self):
        self.invite_type.click()


class TokensPage(GenericPage):
    sidebar = WebItem('.sidebar-tokens', cls=TokensSidebar)
    create_token_page = WebItem('.col-content', cls=CreateNewTokenPage)

    copy_token = Button('.copy-btn')
    token = Label('.clipboard-input.form-control ')
    menu = Button('.with-menu .collapsible-toolbar-toggle')
    revoke_toggle = Toggle('.one-way-toggle')
    save_button = NamedButton('.submit-token', text='Save')

    input_name = Input('.token-consumer .token-container input')
    _toggle = WebElement('.token-consumer '
                         '.ember-basic-dropdown-trigger[role="button"]')
    join_button = NamedButton('button', text='Join')

    def expand_dropdown(self):
        self._toggle.click()

    def __str__(self):
        return 'Tokens page'
