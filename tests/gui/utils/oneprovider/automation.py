"""Utils and fixtures to facilitate operations on transfers in Oneprovider GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label, Icon, \
    Button, WebElement
from tests.gui.utils.onezone.generic_page import Element


TransferStatusList = ['completed', 'skipped', 'cancelled', 'failed', 'active',
                      'evicting', 'scheduled', 'enqueued']
TransferTypeList = ['migration', 'replication', 'eviction']


class ExecutionRecord(PageObject):
    name = Label('td:first-of-type')
    username = Label('td:nth-of-type(2)')
    destination = Label('td:nth-of-type(3)')
    status_icon = Icon('.cell-status')
    menu_button = Button('.cell-actions')
    type_icon = Icon('.cell-type')
    icon = Icon('.transfer-file-icon')

    def __init__(self, driver, web_elem, parent, **kwargs):
        super(ExecutionRecord, self).__init__(driver, web_elem, parent, **kwargs)
        status_class = self.status_icon.get_attribute('class').split()
        type_class = self.type_icon.get_attribute('class').split()
        self.status = [x for x in status_class if x in TransferStatusList][0]
        self.type = [x for x in type_class if x in TransferTypeList][0]

    def get_chart(self):
        return TransferChart(self.driver, self.web_elem.find_element_by_xpath(
            ' .//following-sibling::tr'), self.web_elem)

    def is_expanded(self):
        return 'expanded-row' in self.web_elem.get_attribute('class')

    def expand(self):
        self.web_elem.click()

    def collapse(self):
        if self.is_expanded():
            self.web_elem.click()

    def is_file(self):
        return 'oneicon-browser-file' in self.icon.get_attribute('class')

    def is_directory(self):
        return 'oneicon-browser-directory' in self.icon.get_attribute('class')

    def __str__(self):
        return 'Transfer row {} in {}'.format(self.name, self.parent)


class ExecutionsRecordHistory(ExecutionRecord):
    transferred = Label('td:nth-of-type(6)')
    total_files = Label('td:nth-of-type(7)')


class ExecutionsRecordActive(ExecutionRecord):
    transferred = Label('td:nth-of-type(5)')
    total_files = Label('td:nth-of-type(6)')


class TransferChart(PageObject):
    minute = WebItemsSequence('button.btn-default',
                              cls=ButtonWithTextPageObject)
    hour = WebItemsSequence('button.btn-default',
                              cls=ButtonWithTextPageObject)
    active = Label('button.btn-default.active')
    # We take only last point in the chart
    _speed = WebElement(
        '.transfers-transfer-chart .ct-series line:last-of-type')

    def get_speed(self):
        return self._speed.get_attribute('ct:value').split(',')[1]



class NavigationTab(Element):
    name = id = Label('nav-link')


class _AutomationTab(PageObject):
    navigation_tab = WebItemsSequence('.nav-tabs li', cls=NavigationTab)

    _ended_list = WebItemsSequence('.atm-workflow-executions-table tr.data-row',
                                   cls=ExecutionsRecordHistory)
    _ongoing_list = WebItemsSequence(
        '.atm-workflow-executions-table tr.data-row',
        cls=ExecutionsRecordActive)
    _waiting_list = WebItemsSequence(
        '.atm-workflow-executions-table tr.data-row',
        cls=ExecutionsRecordHistory)
