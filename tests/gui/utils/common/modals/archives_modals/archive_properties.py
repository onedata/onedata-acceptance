"""Utils and fixtures to facilitate operations on archive properties modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Input, Label, Button


class ArchiveProperties(Modal):
    archive_id = Input('.archiveId-field .clipboard-input')
    description = Input('.description-field .form-control')
    layout = Label('.layout-field .field-component')
    create_nested_archives = Toggle('.createNestedArchives-field .form-control')
    incremental = Toggle('.incremental-field .form-control')
    include_dip = Toggle('.includeDip-field .form-control')
    follow_symbolic_link = Toggle('.followSymlinks-field .form-control')
    base_archive = Label('.baseArchiveInfo-field .field-component')
    preserved_callback_url = Input('.preservedCallback-field .clipboard-input')
    purged_callback_url = Input('.purgedCallback-field .clipboard-input')
    close = Button('.close-btn')

    def __str__(self):
        return 'Archive properties'
