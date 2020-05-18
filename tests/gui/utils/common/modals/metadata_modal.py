"""Utils and fixtures to facilitate operations on metadata modals.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import (
    NamedButton, Input, Button, Label, WebItemsSequence, WebItem, WebElement)
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


class JSONMetadataPanel(PageObject):
    text_area = Input('.json-textarea')
    status = WebElement('.tab-pane.active .form-group')


class RDFMetadataPanel(PageObject):
    text_area = Input('.rdf-textarea')


class NavigationTab(PageObject):
    name = id = Label('.tab-name')
    status = WebElement('.tab-state')

    def is_empty(self):
        return 'inactive' in self.status.get_attribute('class')


class MetadataModal(Modal):
    modal_name = Label('.modal-header')
    navigation = WebItemsSequence('.nav-link', cls=NavigationTab)
    basic = WebItem('.relative', cls=BasicMetadataPanel)
    json = WebItem('.relative', cls=JSONMetadataPanel)
    rdf = WebItem('.relative', cls=RDFMetadataPanel)

    close = NamedButton('.btn-default', text='Close')
    save_all = NamedButton('.btn-primary', text='Save all')
    discard_changes = NamedButton('.btn-warning', text='Discard changes')

    loading_alert = Label('.resource-load-error')

    def __str__(self):
        return 'Metadata modal'



