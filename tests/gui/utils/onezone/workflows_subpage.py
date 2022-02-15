"""Utils to facilitate operations on workflows subpage of automation page in
Onezone gui """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Input, Label, \
    Button, WebItem, NamedButton
from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import Element


class Store(Element):
    name = id = Label('.store-name')


class WorkflowLane(Element):
    add_paraller_box_button = Button('.create-parallel-box-action-trigger')
    # paraller_box_list = WebItemsSequence('.lane-elements')


class WorkflowVisualiser(PageObject):

    create_lane_button = Button('.create-lane-action-trigger')
    workflow_lanes = WebItemsSequence('.visualiser-elements '
                                      '.workflow-visualiser-lane', cls = WorkflowLane)

    add_store_button = Button('.create-store-action-trigger')
    stores_list = WebItemsSequence('.workflow-visualiser-stores-list '
                                   '.tag-item', cls = Store)


class Workflow(Element):
    name = id = Label('.text-like-field')
    menu_button = Button('.one-menu-toggle')


class WorkflowsPage(PageObject):
    elements_list = WebItemsSequence('.atm-workflow-schemas-list' 
                                     ' .atm-workflow-schemas-list-entry',
                                     cls=Workflow)

    workflow_visualiser = WebItem('.workflow-visualiser ', cls = WorkflowVisualiser)

    workflow_name = WebItem('.name-field .text-like-field', cls=InputBox)

    create_button = NamedButton('.btn', text='Create')

