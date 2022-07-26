"""Utils and fixtures to facilitate operation on public share view"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import (
    Label, Button, Input, WebItem, WebElementsSequence)
from ..breadcrumbs import Breadcrumbs
from ..file_browser import FileBrowser
from ...core import scroll_to_css_selector_bottom
from ...core.base import PageObject


class URLTypeSelector(PageObject):
    public_share_link = Button('.option-share-link')
    public_rest_endpoint = Button('.option-rest-link')


class DublinCoreMetadata(PageObject):

    def write_to_last_input(self, val, which):
        if which == 'title':
            css_sel = '.form-control[data-dc-element-type="title"]'
        elif which == 'creator':
            css_sel = '.form-control[data-dc-element-type="creator"]'
        elif which == 'description':
            css_sel = '.form-control[data-dc-element-type="description"]'
        inputs = self.driver.find_elements_by_css_selector(css_sel)
        inputs[-1].clear()
        inputs[-1].send_keys(val)

    def click_add_button(self, button_name):
        buttons = self.driver.find_elements_by_css_selector('.btn-add-entry'
                                                            ' .text')
        for button in buttons:
            if button.text == button_name:
                css_sel = '.metadata-text .one-icon'
                scroll_to_css_selector_bottom(self.driver, css_sel)
                button.click()
                break
        else:
            raise Exception(f'{button_name} was not found in '
                            f'"Dublin Core Metadata" form')


class Description(PageObject):
    create_description = Button('.btn-content-info')
    description_field = Input('.textarea-source-editor')
    save = Button('.btn-primary')


class PublicShareView(object):
    name = Label('.fb-breadcrumbs-dir')
    share_name = Label('.share-name')
    link_type_selector = Button('.url-type-selector-trigger')
    url_type_popup = WebItem('.compact-url-type-selector-actions',
                             cls=URLTypeSelector)
    url = Input('.clipboard-input.form-control')
    copy_icon = Button('.oneicon-browser-copy')
    breadcrumbs = Breadcrumbs('.file-browser-head-container')
    file_browser = FileBrowser('.content-file-browser')
    error_msg = Label('.error-details.active')
    description_tab = Button('.nav-link-description')
    publish_as_open_data_tab = Button('.nav-link-opendata')
    files_tab = Button('.nav-link-files')
    description = Label('.markdown-view')
    no_files_message_header = Label('.content-info-content-container h1')
    share_not_found = Label('.text-center .col-xs-12')
    choose_a_handle_service = Button('.select-handle-service')
    proceed = Button('.btn-content-info')
    dublin_core_metadata_form = WebItem('.opendata-one-carousel',
                                        cls=DublinCoreMetadata)
    dublin_core_metadata_data = WebElementsSequence('.open-data-value')
    publish_as_open_data = Button('.btn-submit')
    link_name = Label('.ember-power-select-selected-item')
    copy_link = Button('.clipboard-btn-input[data-clipboard-target~='
                       '".clipboard-line-public-url-input"]')
    description_form = WebItem('.content-space-shares', cls=Description)
    xml = Button('.btn-xml-editor')
    xml_data = Label('.open-data-xml-textarea')

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return 'Public Share View'

