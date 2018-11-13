"""Utils and fixtures to facilitate operations on group hierarchy menu modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, WebItemsSequence, Label


class Options(PageObject):
    name = id = Label('.one-label')


class GroupHierarchyMenu(Modal):
    add_child = Button('.groups-hierarchy-visualiser-actions '
                       '.add-child-group-action')
    options = WebItemsSequence('.groups-hierarchy-visualiser-actions li',
                               cls=Options)

    def __str__(self):
        return 'Group hierarchy menu'

