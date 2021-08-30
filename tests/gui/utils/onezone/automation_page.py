"""Utils to facilitate operations on automation page in Onezone gui"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.generic import rm_css_cls
from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import GenericPage
from tests.gui.utils.core.web_elements import (Button, NamedButton, WebItem,
                                               Label, WebItemsSequence,
                                               WebElement)
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.onezone.common import EditBox, InputBox
from tests.gui.utils.onezone.members_subpage import MembersPage


class Inventory(Element):
    menu = Button('.atm-inventory-menu-trigger')
    workflows = NamedButton('.one-list-level-2 .item-header', text='Workflows')
    lambdas = NamedButton('.one-list-level-2 .item-header', text='Lambdas')
    members = NamedButton('.one-list-level-2 .item-header', text='Members')
    edit_box = WebItem('.name-editor.atm-inventory-name', cls=EditBox)


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

    members_page = WebItem('.main-content', cls=MembersPage)

    privileges_err_msg = Label('.alert-promise-error')

    # upload_input = WebItem('input#upload-atm-workflow-schema-action-input')
    upload_input = WebElement('.upload-atm-workflow-schema-action-input')

    def upload_workflow(self, files):
        """This interaction is very hacky, because uploading files with Selenium
        needs to use input element, but we do not use it directly in frontend.
        So we unhide an input element for a while and pass a local file path to it.
        """
        with rm_css_cls(self.driver, self._upload_input, 'hidden') as elem:
            elem.send_keys(files)
