"""Utils and fixtures to facilitate operations on Task audit log modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (WebItemsSequence, Label, Button)


class LogsEntry(PageObject):
    description = Label('.description-cell')
    severity = Label('.severity-name')


class TaskAuditLog(Modal):
    logs_entry = WebItemsSequence('.audit-log-table-entry', cls=LogsEntry)
    x = Button('.close')

    copy_json = Button('.copy-link')
    close_details = Button('.close-details')

    def __str__(self):
        return 'Task audit log modal'


