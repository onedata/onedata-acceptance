"""Utils and fixtures to facilitate operations on metadata modals."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from decorator import contextmanager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    AceEditor,
    Button,
    Input,
    Label,
    NamedButton,
    WebElement,
    WebElementsSequence,
    WebItem,
    WebItemsSequence,
)


class XattrMetadataEntry(PageObject):
    key = id = Label(".one-label")
    edit_key = Input('.form-control[placeholder="Key"]')
    key_input = Input(".one-inline-editor .form-control")
    value = Input('.form-control[placeholder="Value"]')
    remove = Button(".remove-param")
    edit_existing_key = Button(".edit-icon.clickable")

    def __str__(self):
        return "metadata basic entry"

    def press_backspace_to_delete_selected(self):
        action = ActionChains(self.driver)
        action.key_down(Keys.BACKSPACE).perform()


class XattrMetadataNewEntry(PageObject):
    key = Input('.form-control[placeholder="Key"]')
    value = Input('.form-control[placeholder="Value"]')


class XattrsMetadataPanel(PageObject):
    new_entry = WebItem(".last-record", cls=XattrMetadataNewEntry)
    entries = WebItemsSequence(
        ".form-group-editable:not([class~=last-record])", cls=XattrMetadataEntry
    )
    description = WebElement(".metadata-description")

    def click_on_background_in_xattrs_panel(self):
        ActionChains(self.driver).move_to_element_with_offset(
            self.description, 0, 0
        ).click().perform()


class AceEditorMetadataPanel(PageObject):
    status = WebElement(".tab-pane.active .form-group")
    lines = WebElementsSequence(".ace_line_group")
    area = WebElement(".ace_content")

    @contextmanager
    def select_lines(self):
        action = ActionChains(self.driver)
        action.backspace_down = lambda: action.key_down(Keys.BACKSPACE)
        yield action
        action.perform()

    # TODO VFS-12496 remove metadata_type from clear_editor function
    def clear_editor(self, metadata_type):
        script = (
            f"ace.edit(document.querySelector('.file-metadata-{metadata_type} "
            ".ember-ace > .ace_editor')).setValue('')"
        )
        self.driver.execute_script(script)


class JSONMetadataPanel(AceEditorMetadataPanel):
    text_area = AceEditor(".file-metadata-json")


class RDFMetadataPanel(AceEditorMetadataPanel):
    text_area = AceEditor(".file-metadata-rdf")


class NavigationTab(PageObject):
    name = id = Label(".tab-name")
    status = WebElement(".tab-state")

    def is_empty(self):
        return "inactive" in self.status.get_attribute("class")


class MetadataTab(Modal):
    modal_name = Label(".modal-header")
    navigation = WebItemsSequence(".metadata-type-btn", cls=NavigationTab)
    xattrs = WebItem(".relative", cls=XattrsMetadataPanel)
    json = WebItem(".tab-pane-metadata-json", cls=JSONMetadataPanel)
    rdf = WebItem(".tab-pane-metadata-rdf", cls=RDFMetadataPanel)

    save = NamedButton(".btn-primary", text="Save")
    discard_changes = NamedButton(".btn-warning", text="Discard changes")

    loading_alert = Label(".resource-load-error")
    editor_disabled = Label(".editor-disabled-lock-text")
    question_icon = Button(".oneicon-sign-question-rounded")

    def __str__(self):
        return "Metadata tab"
