"""Utils and fixtures to facilitate operations on Function pods activity modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label
from tests.gui.utils.onezone.generic_page import Element


class PodsRecordStatus(PageObject):
    pod_name = id = Label('.pod-id')
    readiness = Label('.pod-readiness')
    status = Label('.pod-status')


class FilterTab(Element):
    name = id = Label('.text')


class FunctionPodsActivity(PageObject):
    tabs = WebItemsSequence('.pods-filter-btn-group .btn-sm', cls=FilterTab)

    pods_list = WebItemsSequence('.scrollable-table-content tr.data-row',
                                  cls=PodsRecordStatus)

    def __str__(self):
        return 'Function pods activity modal'
