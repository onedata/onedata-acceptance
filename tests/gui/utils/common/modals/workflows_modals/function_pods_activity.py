"""Utils and fixtures to facilitate operations on Function pods activity modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label, \
    WebElement
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


class FunctionPodsActivity(Modal):
    tabs = WebItemsSequence('.pods-filter-btn-group .btn-sm', cls=FilterTab)

    pods_list = WebItemsSequence('.pods-table-section '
                                 '.pods-table-pod-row', cls=PodsRecordStatus)

    events_list = WebItemsSequence('.events-table-section '
                                   '.events-table-event-row', cls=EventRecord)

    events_list_scrollbar = WebElement('.events-table-section '
                                       '.perfect-scrollbar-element')

    def __str__(self):
        return 'Function pods activity modal'

    def get_css_selector(self):
        css_selector = self.web_elem.get_attribute('class')
        css_selector = css_selector.replace(' ', '.')
        css_selector = '.' + css_selector
        return css_selector

    def scroll_to_last_element_of_list(self):
        self.driver.execute_script("arguments[0].scrollBy(0,150)",
                                   self.events_list_scrollbar)

    def scroll_to_event(self, driver, number):
        selector = f'{self.get_css_selector()} ' \
                   f'.events-table-event-row:nth-of-type({number}) '
        scroll_to_css_selector(driver, selector)

    def get_event_reason(self, driver, number, length):
        # This interaction is hacky because scroll in Function pods activity
        # modal scrolls to the event above the wanted one. This is why
        # we are skipping the first iteration of loop (first reason would
        # be doubled) and adding one more scroll and assertion for the last one.
        if number == length:
            self.scroll_to_last_element_of_list()
        else:
            self.scroll_to_event(driver, number)

        element = driver.find_elements_by_css_selector(f'.events-table-event-'
                                                       f'row')[number - 1]
        return element.find_elements_by_css_selector('.event-reason')[0].text
