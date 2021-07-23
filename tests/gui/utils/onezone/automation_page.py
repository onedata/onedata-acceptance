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
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.onezone.common import EditBox, InputBox


class Inventory(Element):
    menu = Button('.collapsible-toolbar-toggle')
    workflows = NamedButton('.one-list-level-2 .item-header', text='Workflows')
    lambdas = NamedButton('.one-list-level-2 .item-header', text='Lambdas')
    members = NamedButton('.one-list-level-2 .item-header', text='Members')
    edit_box = WebItem('.name-editor', cls=EditBox)


class AutomationDetailsPage(PageObject):
    upload_json = NamedButton('.upload-atm-workflow-schema-action-trigger',
                              text='Upload (json)')
    add_new_workflow = NamedButton('.open-add-atm-workflow-schema-trigger',
                                   text='Add new workflow')


class AutomationPage(GenericPage):
    elements_list = WebItemsSequence('.sidebar-atm-inventories '
                                     '.one-list>.one-list-item.clickable',
                                     cls=Inventory)

    create_automation = Button('.create-atm-inventory-link-trigger')

    input_box = WebItem('.content-info-content-container', cls=InputBox)

    main_page = WebItem('.col-content', cls=AutomationDetailsPage)
