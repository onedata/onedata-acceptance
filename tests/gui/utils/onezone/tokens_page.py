"""Utils to facilitate operations on tokens page in Onezone gui"""

__author__ = "Michal Stanisz, Natalia Organek"
__copyright__ = "Copyright (C) 2018-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.common.privilege_tree import PrivilegeTree
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button, NamedButton, WebItemsSequence, Label, Input, WebElement, WebItem,
    WebElementsSequence)
from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import GenericPage
from tests.gui.utils.onezone.token_caveats import CaveatField


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


class TokenInviteTargetOptions(PageObject):
    name = id = Label('.text')


class TokenInviteTargetNameOptions(PageObject):
    name = id = Label('.truncated-string')


class TokenInviteFilter(PageObject):
    dropdown_menus = WebElementsSequence('.ember-basic-dropdown-trigger')
    options = WebItemsSequence('.ember-power-select-option',
                               cls=TokenInviteTargetOptions)
    name_options = WebItemsSequence('.ember-power-select-option',
                                    cls=TokenInviteTargetNameOptions)


class TokensSidebar(PageObject):
    create_new_token = Button('.one-sidebar-toolbar-button .oneicon-add-filled')
    tokens = WebItemsSequence('.token-item', cls=TokenRow)
    consume_token = Button('.oneicon-consume-token')
    clean_up_obsolete_tokens = Button('.oneicon-clean-filled')
    filter = WebItem('.filter-control', cls=TokenFilter)
    invite_filter = WebItem('.filter-control.target-filter',
                            cls=TokenInviteFilter)

    name_input = Input('.name-editor .form-control')
    confirm = Button('.save-icon')
    discard = Button('.cancel-icon')

    def click_create_new_token(self, driver):
        driver.execute_script("arguments[0].click();",
                              self.web_elem.find_element_by_css_selector(
                                  '.create-token-link-trigger'))

    def __str__(self):
        return 'Tokens sidebar'


class UsageLimitBar(PageObject):
    infinity_option = WebElement('.option-infinity .one-way-radio-control')
    number_option = WebElement('.option-number')
    number_input = Input('.text-like-field .form-control')


class CreateNewTokenPage(PageObject):
    create_custom_token = Button('.template-custom')

    create_token = NamedButton('.submit-token', text='Create token')
    access_option = WebElement('.option-access .one-way-radio-control')
    identity_option = WebElement('.option-identity .one-way-radio-control')
    invite_option = WebElement('.option-invite .one-way-radio-control')

    token_name_input = WebItem('.name-field .field-component', cls=InputBox)

    invite_type = WebElement('.inviteType-field .dropdown-field-trigger')
    invite_target = WebElement('.target-field .dropdown-field-trigger')
    usage_limit = WebItem('.usageLimit-collapse', cls=UsageLimitBar)

    show_inactive_caveats = Button('.caveats-expand')
    expiration_caveat = WebItem('.expireCaveat-field', cls=CaveatField)
    region_caveat = WebItem('.regionCaveat-field', cls=CaveatField)
    country_caveat = WebItem('.countryCaveat-field', cls=CaveatField)
    asn_caveat = WebItem('.asnCaveat-field', cls=CaveatField)
    ip_caveat = WebItem('.ipCaveat-field', cls=CaveatField)
    consumer_caveat = WebItem('.consumerCaveat-field', cls=CaveatField)
    service_caveat = WebItem('.serviceCaveat-field', cls=CaveatField)
    interface_caveat = WebItem('.interfaceCaveat-field', cls=CaveatField)
    readonly_caveat = WebItem('.readonlyCaveat-field', cls=CaveatField)
    path_caveat = WebItem('.pathCaveat-field', cls=CaveatField)
    object_id_caveat = WebItem('.objectIdCaveat-field', cls=CaveatField)

    footer = WebElement('.footer-buttons')

    def __str__(self):
        return 'Create new token page'

    def expand_invite_type_dropdown(self):
        self.invite_type.click()

    def expand_invite_target_dropdown(self):
        self.invite_target.click()

    def expand_caveats(self):
        if 'show' in self.show_inactive_caveats.web_elem.text.lower():
            self.show_inactive_caveats()

    def hide_caveats(self):
        if 'hide' in self.show_inactive_caveats.web_elem.text.lower():
            self.show_inactive_caveats()

    def scroll_to_bottom(self):
        self.driver.execute_script('arguments[0].scrollTo(arguments[1]);',
                                   self.web_elem, self.footer)

    def get_caveat(self, name):
        self.scroll_to_bottom()
        return getattr(self, f'{name}_caveat')


class TokensPage(GenericPage):
    sidebar = WebItem('.sidebar-tokens', cls=TokensSidebar)
    create_token_page = WebItem('.col-content', cls=CreateNewTokenPage)

    copy_token = Button('.copy-btn')
    token = Label('.clipboard-input.form-control ')
    menu = Button('.with-menu .collapsible-toolbar-toggle')
    revoke_toggle = Toggle('.one-way-toggle')
    save_button = NamedButton('.submit-token', text='Save')

    privilege_tree = WebItem('.invitePrivilegesDetails-field',
                             cls=PrivilegeTree)

    token_name = Label('.name-field .text-like-field')
    token_type = Label('.type-field .radio-field')
    invite_type = Label('.inviteType-field .field-component')
    invite_target = Label('.target-field .field-component')
    usage_count = Label('.usageCount-field .static-text-field')

    input_name = Input('.token-consumer .token-container input')
    _toggle = WebElement('.token-consumer '
                         '.ember-basic-dropdown-trigger[role="button"]')
    join_button = NamedButton('button', text='Join')

    onezone_rest_access_template = WebElement('.template-onezoneRest')

    def expand_dropdown(self):
        self._toggle.click()

    def is_token_revoked(self):
        return self.revoke_toggle.is_checked()

    def __str__(self):
        return 'Tokens page'
