"""Utils and fixtures to facilitate operations on Select files, direcotires
 or symlinks modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button
from tests.gui.utils.oneprovider import FileBrowser


class SelectFilesDirectoriesSymlinks(PageObject):
    file_browser = FileBrowser('.items-select-browser-part.upload-drop-zone-container')
    confirm_button = Button('.submit-selection-btn')
