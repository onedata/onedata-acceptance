"""Utils and fixtures to facilitate operations on create archive modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Input, Label, NamedButton, WebElement, WebItem
from tests.utils.utils import element_has_class, repeat_failed

from ..modal import Modal


class ToggleContainer(PageObject):
    toggle_area = WebElement(".one-checkbox-base.one-way-toggle")
    toggle_track = Toggle(".one-way-toggle-control")

    def is_checked(self) -> bool:
        return element_has_class(self.toggle_area, "checked")

    @repeat_failed(timeout=0.5)
    def check(self) -> None:
        if not self.is_checked():
            self.toggle_track.web_elem.click()
        assert self.is_checked(), "Toggle failed to check"


class CreateArchive(Modal):
    header = WebElement(".archive-create-modal-header")
    base_archive = Label(".field-component.static-text-field")

    create = NamedButton(".btn-primary", text="Create")
    description = Input(".textarea-field .form-control")
    bagit = Button(".option-bagit .one-way-radio-control")

    create_nested_archives = WebItem(
        ".field-renderer .form-group .createNestedArchives-field", cls=ToggleContainer
    )
    incremental = WebItem(".field-renderer .form-group .incremental-field", cls=ToggleContainer)
    include_dip = WebItem(".field-renderer .form-group .includeDip-field", cls=ToggleContainer)
    follow_symbolic_links = WebItem(
        ".field-renderer .form-group .followSymlinks-field", cls=ToggleContainer
    )

    def __str__(self) -> str:
        return "Create archive"
