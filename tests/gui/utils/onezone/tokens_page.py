"""Utils to facilitate operations on tokens page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               WebItemsSequence, Label, Input,
                                               WebElement)
from tests.gui.utils.onezone.generic_page import Element, GenericPage


class TokensPage(GenericPage):
    create_token = Button('.create-token-btn .oneicon-add-filled')
    remove_token = NamedButton('button.delete-token', text='Remove')
    consume_token = Button('.oneicon-consume-token')
    copy_token = Button('.copy-btn')
    elements_list = WebItemsSequence('.sidebar-tokens '
                                     'li.one-list-item.clickable', cls=Element)
    token = Label('.content-info-content-container '
                  '.token-textarea.form-control')

    input_name = Input('.token-consumer .token-container input')
    _toggle = WebElement('.token-consumer '
                         '.ember-basic-dropdown-trigger[role="button"]')
    join_button = NamedButton('button', text='Join')

    def expand_dropdown(self):
        self._toggle.click()
