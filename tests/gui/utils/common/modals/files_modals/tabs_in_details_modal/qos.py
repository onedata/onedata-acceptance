"""Utils and fixtures to facilitate operations on Quality of Service modal."""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.common.exceptions import JavascriptException

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.common.query_builder import QueryBuilder
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    NamedButton,
    WebElement,
    WebItem,
    WebItemsSequence,
)


class Requirement(PageObject):
    delete = Button(".remove-qos-trigger")
    fulfilled = Label(".qos-status-fulfilled")
    impossible = Label(".qos-status-impossible")
    expression = Label(".query-builder-input")
    replicas_number = Label(".replicas-number")


class Entry(PageObject):
    time = WebElement(".timestamp-cell")
    file = WebElement(".cell-file")
    event = WebElement(".cell-content-message")
    link = WebElement(".cell-file .navy")


class AuditLogBrowser(PageObject):

    entries = WebItemsSequence(".table-entry.data-row.audit-log-table-entry", cls=Entry)

    def is_empty(self):
        return len(self.entries) == 0

    empty_info = WebElement(".table-is-empty-cell")


class QoSTab(Modal):
    add_requirement = NamedButton(".btn-primary", text="Add Requirement")
    enter_as_text = Button(".enter-text-link")
    confirm_text = Button(".oneicon-checked")
    expression = Input(".qos-info-row-expression .form-control")
    replicas_number = Input(".replicas-number-input")
    save = NamedButton(".btn-primary", text="Save")
    requirements = WebItemsSequence(".qos-entry", cls=Requirement)
    delete_confirm = NamedButton(".btn-danger", text="Yes, remove")

    audit_log_list = WebItem(".audit-log-browser", cls=AuditLogBrowser)

    show_details_audit_log = Button(".qos-details-type-logs")
    show_details_transfer_statistics = Button(".qos-details-type-charts")

    query_builder = WebItem(".query-builder", cls=QueryBuilder)
    storage_matching = Label(".storages-matching-number")
    no_storage_matching = Label(".storages-matching-text")
    show_matching_storages = Button(".storages-matching-info-icon")
    privileges_message = Label(".world-map .text-center")
    question_icon = Button(".oneicon-sign-question-rounded")

    def __str__(self):
        return "QoS tab"

    def scroll_to_top(self):
        try:
            self.driver.execute_script(
                "document.querySelector('.perfect-scrollbar-element"
                ".ps--active-y').scrollTo(0, 0)"
            )
        except JavascriptException as e:
            raise Exception("Error executing script, failed to scroll to top of QoSTab Modal") from e
