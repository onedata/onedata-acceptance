"""Utils and fixtures to facilitate operations on transfers in Oneprovider GUI
"""

__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from functools import partial

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.oneprovider.data_tab.space_selector import SpaceRecord
from tests.gui.utils.core.web_elements import (Label, WebElement,
                                               Icon, WebItemsSequence,
                                               ButtonWithTextPageObject,
                                               WebItem, Button)

TransferStatusList = ['completed', 'skipped', 'cancelled', 'failed',
                      'replicating', 'evicting', 'scheduled', 'enqueued']
TransferTypeList = ['migration', 'replication', 'eviction']


# before initializing transfer record make sure,
# that columns used in __init__ are enabled
class TransferRecord(PageObject):
    name = Label('td:first-of-type')
    username = Label('td:nth-of-type(2)')
    destination = Label('td:nth-of-type(3)')
    status_icon = Icon('.cell-status')
    menu_button = Button('.cell-actions')
    type_icon = Icon('.cell-type')
    icon = Icon('.transfer-file-icon')

    def __init__(self, driver, web_elem, parent, **kwargs):
        super(TransferRecord, self).__init__(driver, web_elem, parent, **kwargs)
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


class TransferRecordHistory(TransferRecord):
    replicated = Label('.replicated-bytes')
    total_files = Label('.evicted-files')


class TransferRecordActive(TransferRecord):
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


class TabHeader(PageObject):
    name = Label('.tab-label')

    def click(self):
        self.web_elem.click()


class TransferColumnHeader(PageObject):
    name = id = Label('.column-name')


class _TransfersTab(PageObject):
    providers_table = WebElement('.providers-table')
    spaces = WebItemsSequence('ul.spaces-list li', cls=SpaceRecord)
    tabs = WebItemsSequence('.providers-table .nav-tabs li',
                            cls=TabHeader)
    _ended_list = WebItemsSequence('.col-ended-transfers tr.data-row',
                                   cls=TransferRecordHistory)
    _ongoing_list = WebItemsSequence('.col-ongoing-transfers tr.data-row',
                                     cls=TransferRecordActive)
    _waiting_list = WebItemsSequence('.col-waiting-transfers tr.data-row',
                                     cls=TransferRecordHistory)
    _transfers_list_for_certain_file = WebItemsSequence(
        '.transfers-table-container .transfer-row', cls=TransferRecord)
    configure_columns = Button('.columns-configuration-button')
    column_headers = WebItemsSequence(
        '.transfers-table th:not(:last-child, :first-of-type)',
        cls=TransferColumnHeader)

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

    @property
    def certain_file(self):
        return self._transfers_list_for_certain_file

    def __getitem__(self, name):
        for tab in self.tabs:
            if name in tab.name.lower():
                return tab
        else:
            raise RuntimeError('no tab named {} in transfer tab'.format(name))


TransfersTab = partial(WebItem, cls=_TransfersTab)
