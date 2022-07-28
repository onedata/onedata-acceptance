"""Utils and fixtures to facilitate operations on Function pods activity modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import pdb

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label
from tests.gui.utils.onezone.generic_page import Element


class FilterTab(Element):
    name = id = Label('.text')


class PodsRecordStatus(PageObject):
    pod_name = id = Label('.pod-id')
    readiness = Label('.pod-readiness')
    status = Label('.pod-status')


class EventRecord(PageObject):
    type = Label('.event-type')
    reason = id = Label('.event-reason')


class FunctionPodsActivity(Modal):
    tabs = WebItemsSequence('.pods-filter-btn-group .btn-sm', cls=FilterTab)

    pods_list = WebItemsSequence('.pods-table-section '
                                 '.pods-table-pod-row', cls=PodsRecordStatus)

    events_list = WebItemsSequence('.events-table-section '
                                   '.events-table-event-row', cls=EventRecord)

    def __str__(self):
        return 'Function pods activity modal'

    def get_css_selector(self):
        css_selector = self.web_elem.get_attribute('class')
        css_selector = css_selector.replace(' ', '.')
        css_selector = '.' + css_selector
        return css_selector

    def scroll_to_bottom(self):
        self.driver.execute_script('arguments[0].scrollIntoView();',
                                   self.rows[-1].web_elem)

    def scroll_to_event(self, driver, number, length):
        if number == 0:
            tmp_number = number
        else:
            tmp_number = number - 1

        selector = (self.get_css_selector() + ' ' +
                    f'.events-table-event-row:nth-of-type({number}) ')
        scroll_to_css_selector(driver, selector)

        pom = driver.find_elements_by_css_selector(f'.events-table-event-row')[
            tmp_number]
        print(pom.find_elements_by_css_selector('.event-reason')[0].text)
        pdb.set_trace()
        return pom.find_elements_by_css_selector('.event-reason')[0].text
