"""Utils and fixtures to facilitate operations on workflows in Oneprovider GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from selenium.webdriver import ActionChains

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    WebItemsSequence, Label, Icon, Button, NamedButton, WebItem, WebElement)
from tests.gui.utils.onezone.generic_page import Element


class ExecutionRecord(PageObject):
    name = id = Label('.cell-name')
    inventory = Label('.cell-inventory')
    status_icon = Icon('.cell-status')
    menu_button = Button('.cell-actions')

    def expand(self):
        self.web_elem.click()

    def __str__(self):
        return f'Workflow row {self.name} in {self.parent}'


class Revision(Element):
    number = id = Label('.revision-number')
    name = Label('.description')


class Workflow(Element):
    name = id = Label('.workflow-schema-name')

    show_revisions_button = Button('.expand-button')
    revision_list = WebItemsSequence('.revisions-table '
                                     '.revisions-table-revision-entry',
                                     cls=Revision)


class NavigationTab(Element):
    name = id = Label('.tab-name')


class Task(Element):
    name = id = Label('.task-name')
    drag_handle = WebElement('.task-drag-handle')
    pods_activity = Button('.view-task-pods-activity-action-trigger')
    instance_id = Label('.instance-id-detail .truncated-string')
    status = Label('.status-detail .detail-value')
    time_series = Button('.view-task-time-series-action-trigger')
    audit_log = Button('.view-task-audit-log-action-trigger')

    def get_elem_id(self):
        elem_id = self.web_elem.get_attribute('id')
        return elem_id


class ParallelBox(Element):
    task_list = WebItemsSequence('.box-elements .workflow-visualiser-task',
                                 cls=Task)


class RunIndicator(Element):
    number = id = Label('.run-number')
    origin_run_number = Label('.origin-run-number')


class WorkflowLane(Element):
    name = id = Label('.lane-name')
    status = Label('.visible-run-status-label')
    parallel_boxes = WebItemsSequence('.workflow-visualiser-parallel-box ',
                                      cls=ParallelBox)
    latest_run_menu = Button('.lane-run-actions-trigger .menu-toggle-frame')
    run_indicators = WebItemsSequence('.run-indicators-item', cls=RunIndicator)

    def scroll_to_first_task_in_parallel_box(self, number):
        from tests.gui.utils.core import scroll_to_css_selector_bottom
        elem_id = self.parallel_boxes[number].task_list[0].get_elem_id()
        box_sel = f'[id={elem_id}] .items-failed-detail'
        scroll_to_css_selector_bottom(self.driver, box_sel)


class Store(Element):
    name = id = Label('.store-name')


class WorkflowVisualiser(PageObject):
    status = Label('.workflow-status-text .workflow-status')
    workflow_lanes = WebItemsSequence('.visualiser-elements '
                                      '.workflow-visualiser-lane',
                                      cls=WorkflowLane)

    add_store_button = Button('.create-store-action-trigger')
    stores_list = WebItemsSequence('.workflow-visualiser-stores-list '
                                   '.tag-item', cls=Store)
    pause = NamedButton('.pause-resume-atm-workflow-execution-action-trigger',
                        text="Pause")
    resume = NamedButton('.pause-resume-atm-workflow-execution-action-trigger',
                         text="Resume")
    cancel = Button('.cancel-atm-workflow-execution-action-trigger')


class WorkflowExecutionPage(PageObject):
    navigation_tab = WebItemsSequence('.nav-tabs .tab-label', cls=NavigationTab)

    available_workflow_list = WebItemsSequence('.atm-workflow-schemas-list'
                                               ' .list-entry', cls=Workflow)
    input_link = Button('.add-item-trigger')
    run_workflow_button = NamedButton('.btn-submit', text='Run Workflow')

    workflow_executions_list = WebItemsSequence(
        '.atm-workflow-executions-table tr.data-row', cls=ExecutionRecord)

    workflow_visualiser = WebItem('.workflow-visualiser',
                                  cls=WorkflowVisualiser)
    workflow_header = WebElement('.workflow-visualiser')

    def click_on_background_in_workflow_visualiser(self):
        ActionChains(self.driver).move_to_element_with_offset(
            self.workflow_header, 0, 0).click().perform()
