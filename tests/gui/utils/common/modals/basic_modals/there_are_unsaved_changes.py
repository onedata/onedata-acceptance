"""Utils and fixtures to facilitate operations on there are unsaved changes
modal.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import Button
from ..modal import Modal


class ThereAreUnsavedChanges(Modal):
    dont_save = Button('.question-dont-save')
    cancel = Button('.question-cancel')
    save = Button('.question-save')

    def __str__(self):
        return 'There are unsaved changes modal'
