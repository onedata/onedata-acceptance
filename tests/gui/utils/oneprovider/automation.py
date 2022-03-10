"""Utils and fixtures to facilitate operations on workflows in Oneprovider GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label, Icon, \
    Button, WebElement, NamedButton, WebItem
from tests.gui.utils.core.web_objects import ButtonWithTextPageObject
from tests.gui.utils.onezone.generic_page import Element

WorkflowStatusList = ['scheduled', 'preparing', 'enqueued', 'active',
                      'aborting', 'interrupted', 'cancelled', 'skipped',
                      'finished', 'failed', 'unknown']


class ExecutionRecord(PageObject):
    name = Label('cell-name')
    inventory = Label('cell-inventory')
    status_icon = Icon('.cell-status')
    menu_button = Button('.cell-actions')

    def __init__(self, driver, web_elem, parent, **kwargs):
        super(ExecutionRecord, self).__init__(driver, web_elem, parent,
                                              **kwargs)
        status_class = self.status_icon.get_attribute('class').split()
        self.status = [x for x in status_class if x in WorkflowStatusList][0]

    def is_expanded(self):
        return 'expanded-row' in self.web_elem.get_attribute('class')

    def expand(self):
        self.web_elem.click()

    def collapse(self):
        if self.is_expanded():
            self.web_elem.click()

    def __str__(self):
        return 'Workflow row {} in {}'.format(self.name, self.parent)


class Revision(Element):
    name = id = Label('.description')


class Workflow(Element):
    name = id = Label('.workflow-schema-name')

    show_revisions_button = Button('.expand-button')
    revision_list = WebItemsSequence('.revisions-table '
                                     '.revisions-table-revision-entry',
                                     cls=Revision)


class NavigationTab(Element):
    name = id = Label('.tab-name')


class Task(Element):
    pods_activity = Button('.view-task-pods-activity-action-trigger')


class ParallelBox(Element):
    task_list = WebItemsSequence('.box-elements .draggable-task', cls=Task)


class WorkflowLane(Element):
    name = id = Label('.lane-name')
    parallel_box = WebItem('.workflow-visualiser-parallel-box ',
                           cls=ParallelBox)


class Store(Element):
    name = id = Label('.store-name')


class WorkflowVisualiser(PageObject):
    status_bar = Label('.workflow-status-text .workflow-status')
    workflow_lanes = WebItemsSequence('.visualiser-elements '
                                      '.workflow-visualiser-lane',
                                      cls=WorkflowLane)

    add_store_button = Button('.create-store-action-trigger')
    stores_list = WebItemsSequence('.workflow-visualiser-stores-list '
                                   '.tag-item', cls=Store)


class WorkflowExecutionPage(PageObject):
    navigation_tab = WebItemsSequence('.nav-tabs .tab-label', cls=NavigationTab)

    workflow_list = WebItemsSequence('.atm-workflow-schemas-list'
                                     ' .list-entry', cls=Workflow)
    input_icon = Button('.tag-creator-trigger')
    run_workflow_button = NamedButton('.btn-submit', text='Run Workflow')

    _ended_list = WebItemsSequence('.atm-workflow-executions-table tr.data-row',
                                   cls=ExecutionRecord)
    _ongoing_list = WebItemsSequence(
        '.atm-workflow-executions-table tr.data-row',
        cls=ExecutionRecord)
    _waiting_list = WebItemsSequence(
        '.atm-workflow-executions-table tr.data-row',
        cls=ExecutionRecord)

    workflow_visualiser = WebItem('.workflow-visualiser',
                                  cls=WorkflowVisualiser)

    @property
    def ongoing(self):
        self['ongoing'].click()
        return self._ongoing_list

    @property
    def ended(self):
        self['ended'].click()
        return self._ended_list

    @property
    def waiting(self):
        self['waiting'].click()
        return self._waiting_list

    def __getitem__(self, name):
        for tab in self.navigation_tab:
            if name in tab.name.lower():
                return tab
        else:
            raise RuntimeError('no tab named {} in automation tab'.format(name))
