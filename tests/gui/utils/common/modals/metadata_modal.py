"""Utils and fixtures to facilitate operations on metadata modals.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from decorator import contextmanager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.gui.utils.core.web_elements import (
    NamedButton, Input, Button, Label, WebItemsSequence, WebItem, WebElement,
    WebElementsSequence, AceEditor)
from .modal import Modal
from ...core.base import PageObject


class BasicMetadataEntry(PageObject):
    key = id = Label('.one-label')
    edit_key = Input('.form-control[placeholder="Key"]')
    key_input = Input('.one-inline-editor .form-control')
    value = Input('.form-control[placeholder="Value"]')
    remove = Button('.remove-param')

    def __str__(self):
        return 'metadata basic entry'


class BasicMetadataNewEntry(PageObject):
    key = Input('.form-control[placeholder="Key"]')
    value = Input('.form-control[placeholder="Value"]')


class BasicMetadataPanel(PageObject):
    new_entry = WebItem('.last-record', cls=BasicMetadataNewEntry)
    entries = WebItemsSequence('.form-group-editable:not([class~=last-record])',
                               cls=BasicMetadataEntry)


class AceEditorMetadataPanel(PageObject):
    status = WebElement('.tab-pane.active .form-group')
    lines = WebElementsSequence('.ace_line_group')
    area = WebElement('.ace_content')

    @contextmanager
    def select_lines(self):
        action = ActionChains(self.driver)
        action.backspace_down = lambda: action.key_down(Keys.BACKSPACE)
        yield action
        action.perform()


class JSONMetadataPanel(AceEditorMetadataPanel):
    text_area = AceEditor('.fb-metadata-json')


class RDFMetadataPanel(AceEditorMetadataPanel):
    text_area = AceEditor('.fb-metadata-rdf')


class NavigationTab(PageObject):
    name = id = Label('.tab-name')
    status = WebElement('.tab-state')

    def is_empty(self):
        return 'inactive' in self.status.get_attribute('class')


class MetadataModal(Modal):
    modal_name = Label('.modal-header')
    navigation = WebItemsSequence('.nav-link', cls=NavigationTab)
    basic = WebItem('.relative', cls=BasicMetadataPanel)
    json = WebItem('#json.tab-pane', cls=JSONMetadataPanel)
    rdf = WebItem('#rdf.tab-pane', cls=RDFMetadataPanel)

    close = NamedButton('.btn-default', text='Close')
    save_all = NamedButton('.btn-primary', text='Save all')
    discard_changes = NamedButton('.btn-warning', text='Discard changes')

    loading_alert = Label('.resource-load-error')

    def __str__(self):
        return 'Metadata modal'



