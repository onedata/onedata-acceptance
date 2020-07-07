"""Utils and fixtures to facilitate operations on Quality of Service popover
modal.
"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, Input, NamedButton,
                                               WebItemsSequence)


class Requirement(PageObject):
    delete = Button('.oneicon-checkbox-filled-x')


class QualityOfServicePopover(Modal):
    add_requirement = NamedButton('.btn-primary', text='Add Requirement')
    input_name = Input('.code-textarea')
    save = NamedButton('.ready', text='Save')
    close = NamedButton('.btn-default', text='Close')
    requirements = WebItemsSequence('.qos-entry', cls=Requirement)
    delete_confirm = NamedButton('.spin-button-label', text='Yes, remove')

    def __str__(self):
        return 'Quality of Service modal'
