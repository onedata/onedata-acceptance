"""Utils and fixtures to facilitate operations on Function pods activity modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from selenium.webdriver.common.by import By

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (WebItemsSequence, Label,
                                               WebElement, Button)
from tests.gui.utils.onezone.generic_page import Element


class FilterTab(Element):
    name = id = Label('.text')


class PodsRecordStatus(PageObject):
    pod_name = id = Label('.pod-id')
    readiness = Label('.pod-readiness')
    status = Label('.pod-status')


class EventRecord(PageObject):
    reason = id = Label('.event-reason')
    type = Label('.event-type')
    message = Label('.event-message')


class FunctionPodsActivity(Modal):
    tabs = WebItemsSequence('.pods-filter-btn-group .btn-sm', cls=FilterTab)

    pods_list = WebItemsSequence('.pods-table-section '
                                 '.pods-table-pod-row', cls=PodsRecordStatus)

    events_list = WebItemsSequence('.events-table-section '
                                   '.audit-log-table-entry', cls=EventRecord)

    events_list_scrollbar = WebElement('.events-table-section '
                                       '.perfect-scrollbar-element')
    x = Button('.close')

    def __str__(self):
        return 'Function pods activity modal'

    def get_css_selector(self):
        css_selector = self.web_elem.get_attribute('class')
        css_selector = css_selector.replace(' ', '.')
        css_selector = '.' + css_selector
        return css_selector

    def get_elem_by_data_row_id(self, number, driver, option):
        selector =  f'{self.get_css_selector()} [data-row-id="{number}"]'
        elem_sel = f'.event-{option}'
        scroll_to_css_selector(driver, selector)
        row = driver.find_elements(By.CSS_SELECTOR, selector)[0]
        elem_in_row = row.find_elements(By.CSS_SELECTOR, elem_sel)[0].text
        return elem_in_row

    def get_number_of_data_rows(self, driver):
        element = driver.find_elements(By.CSS_SELECTOR,
            f'.audit-log-table-entry')[0]
        return element.get_attribute('data-row-id')
