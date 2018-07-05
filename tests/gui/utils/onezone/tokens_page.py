"""Utils to facilitate operations on tokens page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               WebItemsSequence, WebItem)
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from .common import InputBox


class TokensPage(GenericPage):
    create_token = Button('.oneicon-add-filled')
    remove_token = NamedButton('.header-row button', text='Remove')
    copy_token = Button('.copy-btn')
    elements_list = WebItemsSequence('.sidebar-tokens '
                                     'li.one-list-item.clickable', cls=Element)
    input_box = WebItem('.content-info-content-container', cls=InputBox)
