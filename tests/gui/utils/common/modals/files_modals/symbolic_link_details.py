"""Utils and fixtures to facilitate operations on symbolic link details modal."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.type_definitions import Clipboard
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Button, Label, NamedButton
from tests.gui.utils.generic import transform


class SymbolicLinkDetailsModal(Modal):
    modal_name = Label(".modal-header h1")
    owner = Label(".file-info-row-owner .property-value")
    close = Button(".close")
    symbolic_link_name = Button(".file-info-row-name .property-value .clipboard-btn")
    symbolic_link_location = Button(
        ".file-info-row-path .property-value .clipboard-btn"
    )
    symbolic_link_target_path = Button(
        ".file-info-row-target-path .property-value .clipboard-btn"
    )

    def __str__(self) -> str:
        return "Symbolic link details modal"

    def get_property(
        self,
        property_name: str,
        clipboard: Clipboard,
        displays: dict[str, str],
        browser_id: str,
    ) -> str:
        getattr(self, transform(property_name)).click()
        return clipboard.paste(display=displays[browser_id])
