"""Utils and fixtures to facilitate operations on data row menu modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label


class Options(PageObject):
    name = id = Label('.one-label')


class DataRowMenu(Modal):
    options = WebItemsSequence('.file-actions.dropdown-menu a.clickable',
                               cls=Options)

    def __str__(self):
        return 'Data row menu'

