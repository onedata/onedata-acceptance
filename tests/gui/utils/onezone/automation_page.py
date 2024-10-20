"""Utils to facilitate operations on automation page in Onezone gui"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    NamedButton,
    WebElement,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.generic import rm_css_cls
from tests.gui.utils.onezone.common import EditBox, InputBox
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from tests.gui.utils.onezone.lambdas_subpage import LambdasPage
from tests.gui.utils.onezone.members_subpage import MembersPage
from tests.gui.utils.onezone.workflows_subpage import WorkflowsPage


class Inventory(Element):
    name = id = Label(".item-name")
    menu = Button(".atm-inventory-menu-trigger")
    workflows = NamedButton(".one-list-level-2 .item-header", text="Workflows")
    lambdas = NamedButton(".one-list-level-2 .item-header", text="Lambdas")
    members = NamedButton(".one-list-level-2 .item-header", text="Members")
    edit_box = WebItem(".name-editor.atm-inventory-name", cls=EditBox)


class AutomationDetailsPage(PageObject):
    upload_json = NamedButton(
        ".upload-atm-workflow-schema-action-trigger", text="Upload (json)"
    )
    add_new_workflow = NamedButton(".btn", text="Add new workflow")

    add_new_lambda = NamedButton(".btn", text="Add new lambda")


class AutomationPage(GenericPage):
    elements_list = WebItemsSequence(
        ".sidebar-atm-inventories .one-list>.one-list-item.clickable",
        cls=Inventory,
    )

    create_automation = Button(".create-atm-inventory-link-trigger")

    input_box = WebItem(".content-info-content-container", cls=InputBox)

    main_page = WebItem(".main-content", cls=AutomationDetailsPage)

    members_page = WebItem(".main-content", cls=MembersPage)

    workflows_page = WebItem(".main-content", cls=WorkflowsPage)

    lambdas_page = WebItem(".main-content", cls=LambdasPage)

    privileges_err_msg = Label(".alert-promise-error")

    _upload_input_workflow = WebElement(".upload-atm-workflow-schema-action-input")

    _upload_input_lambda = WebElement(".upload-atm-lambda-action-input")

    def upload_workflow(self, files):
        """This interaction is very hacky, because uploading files with Selenium
        needs to use input element, but we do not use it directly in frontend.
        So we unhide an input element for a while and pass a local file path to it.
        """
        with rm_css_cls(self.driver, self._upload_input_workflow, "hidden") as elem:
            elem.send_keys(files)

    def upload_lambda(self, files):
        with rm_css_cls(self.driver, self._upload_input_lambda, "hidden") as elem:
            elem.send_keys(files)
