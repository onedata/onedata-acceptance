"""Utils and fixtures to facilitate operation on public and private share
view"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import Button, Label, WebElementsSequence


class ShareView(object):
    xml = Button('.btn-xml-editor')
    xml_data = Label('.open-data-xml-textarea')
    description_tab = Button('.nav-link-description')
    publish_as_open_data_tab = Button('.nav-link-opendata')
    files_tab = Button('.nav-link-files')
    dublin_core_metadata_data = WebElementsSequence('.open-data-value')
    copy_link = Button('.clipboard-btn-input[data-clipboard-target~='
                       '".clipboard-line-public-url-input"]')

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return 'Share View'
