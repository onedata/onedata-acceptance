"""Utils and fixtures to facilitate operations on upload presenter."""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, WebElement


class UploadPresenter(PageObject):
    upload_state = WebElement(".header-text")
    _summary_state = WebElement(".summary-state .one-icon")

    minimize_summary_button = Button(".upload-summary-header-toggle-minimize")
    cancel_button = Button(".cancel-action.upload-summary-header-cancel")

    def is_failed(self):
        return "upload-object-error-icon" in self._summary_state.get_attribute(
            "class"
        )

    def __str__(self):
        return "Upload presenter"
