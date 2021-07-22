"""Utils to facilitate operations on clusters page in Onezone gui"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import GenericPage
from tests.gui.utils.core.web_elements import (Button, NamedButton, WebItem,
                                               Label, WebItemsSequence,
                                               WebElement)
from tests.gui.utils.core.base import PageObject


class AutomationPage(GenericPage):
    create_automation = Button('.create-atm-inventory-link-trigger')

    input_box = WebItem('.content-info-content-container', cls=InputBox)


