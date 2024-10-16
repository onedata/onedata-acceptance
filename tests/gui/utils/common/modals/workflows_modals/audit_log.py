"""Utils and fixtures to facilitate operations on Task audit log modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItemsSequence,
)


class LogsEntry(PageObject):
    severity = id = Label(".severity-name")
    description = Label(".description-cell")


class AuditLog(Modal):
    logs_entry = WebItemsSequence(".audit-log-table-entry", cls=LogsEntry)
    user_log = WebElement(".user-log-content-cell")
    x = Button(".close")

    copy_json = Button(".copy-link")
    close_details = Button(".close-details")
    download_as_json = Button(".download-audit-log-action-trigger")

    def __str__(self):
        return "Audit log modal"
