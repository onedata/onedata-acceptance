"""Utils to facilitate operations on workflows subpage of automation page in
Onezone gui """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Input, Label, \
    Button, WebItem
from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import Element

class WorkflowEditorTab(PageObject):
    add_store_button = Button('.create-store-action-trigger')


class NewWorkflowPage(PageObject):
    workflow_name = WebItem('.name-field .text-like-field', cls=InputBox)
    create_button = Button('.btn-primary')


class Workflow(Element):
    name = id = Label('.text-like-field')
    menu_button = Button('.one-menu-toggle')


class WorkflowsPage(PageObject):
    elements_list = WebItemsSequence('.atm-workflow-schemas-list' 
                                     ' .atm-workflow-schemas-list-entry',
                                     cls=Workflow)

    new_workflow_page = WebItemsSequence('.content-atm-inventories-workflows-creator-view ', cls=NewWorkflowPage)

    workflow_editor_tab=WebItemsSequence('.editor-tab-active ')

    workflow_details_tab=WebItemsSequence('.details-tab-active ')

