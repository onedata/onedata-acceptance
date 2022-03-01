"""Utils to facilitate operations on workflows subpage of automation page in
Onezone gui """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Input, Label, \
    Button, WebItem, NamedButton
from tests.gui.utils.onezone.common import InputBox, EditBox
from tests.gui.utils.onezone.generic_page import Element


class Task(Element):
    menu_button = Button('.task-actions-trigger')


class ParallelBox(Element):
    add_task_button = Button('.create-task-action-trigger')
    task_list = WebItemsSequence('.box-elements .draggable-task', cls=Task)


class WorkflowLane(Element):
    name = id = Label('.lane-name')
    add_parallel_box_button = Button('.create-parallel-box-action-trigger')
    parallel_box = WebItem('.workflow-visualiser-parallel-box ',
                           cls=ParallelBox)


class Store(Element):
    name = id = Label('.store-name')


class WorkflowVisualiser(PageObject):
    create_lane_button = Button('.create-lane-action-trigger')
    workflow_lanes = WebItemsSequence('.visualiser-elements '
                                      '.workflow-visualiser-lane',
                                      cls=WorkflowLane)

    add_store_button = Button('.create-store-action-trigger')
    stores_list = WebItemsSequence('.workflow-visualiser-stores-list '
                                   '.tag-item', cls=Store)


class RevisionDetails(PageObject):
    description = Input('.textarea-field .form-control')


class NavigationTab(Element):
    name = id = Label('.nav-link')


class TaskAddForm(PageObject):
    task_name = WebItem('.name-field .text-like-field', cls=EditBox)
    create_button = Button('.btn-primary')


class Revision(Element):
    name = id = Label('.description')
    menu_button = Button('.one-menu-toggle')


class Workflow(Element):
    name = id = Label('.name-field .text-like-field')

    menu_button = Button('.workflow-actions-trigger')
    create_new_revision = Button('. create-atm-workflow-schema-revision-action-trigger')
    show_revisions_button = Button('.expand-button')
    revision_list = WebItemsSequence('.revisions-table '
                                     '.revisions-table-revision-entry',
                                     cls=Revision)


class WorkflowsPage(PageObject):
    elements_list = WebItemsSequence('.atm-workflow-schemas-list'
                                     ' .atm-workflow-schemas-list-entry',
                                     cls=Workflow)

    navigation_tab = WebItemsSequence('.nav-tabs li', cls=NavigationTab)

    workflow_visualiser = WebItem('.workflow-visualiser',
                                  cls=WorkflowVisualiser)

    revision_details = WebItem('.revision-details-form', cls=RevisionDetails)

    workflow_name = WebItem('.name-field .text-like-field', cls=InputBox)

    create_button = NamedButton('.btn', text='Create')

    task_form = WebItem('.task-form-container', cls=TaskAddForm)

    workflow_name_input = WebItem('.name-field .text-like-field', cls=EditBox)

    workflow_save_button = Button('.btn-save')



