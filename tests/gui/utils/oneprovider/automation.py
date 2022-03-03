"""Utils and fixtures to facilitate operations on transfers in Oneprovider GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label
from tests.gui.utils.onezone.generic_page import Element


class ExecutionsRecordHistory(TransferRecord):
    transferred = Label('td:nth-of-type(6)')
    total_files = Label('td:nth-of-type(7)')


class ExecutionsRecordActive(TransferRecord):
    transferred = Label('td:nth-of-type(5)')
    total_files = Label('td:nth-of-type(6)')



class NavigationTab(Element):
    name = id = Label('nav-link')


class _AutomationTab(PageObject):
    navigation_tab = WebItemsSequence('.nav-tabs li', cls=NavigationTab)

    _ended_list = WebItemsSequence('.atm-workflow-executions-table tr.data-row',
                                   cls=ExecutionsRecordHistory)
    _ongoing_list = WebItemsSequence('.atm-workflow-executions-table tr.data-row',
                                     cls=ExecutionsRecordActive)
    _waiting_list = WebItemsSequence('.atm-workflow-executions-table tr.data-row',
                                     cls=ExecutionsRecordHistory)
