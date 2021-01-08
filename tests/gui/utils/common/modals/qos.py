"""Utils and fixtures to facilitate operations on Quality of Service modal.
"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, Input, NamedButton,
                                               WebItemsSequence, Label,
                                               WebElement)


class Requirement(PageObject):
    delete = Button('.oneicon-checkbox-filled-x')
    fulfilled = Label('.qos-status-fulfilled')
    impossible = Label('.qos-status-impossible')
    expression = Label('.query-builder-input')
    replicas_number = Label('.replicas-number')


class QualityOfServiceModal(Modal):
    add_requirement = NamedButton('.btn-primary', text='Add Requirement')
    enter_as_text = Button('.enter-text-link')
    confirm_text = Button('.oneicon-checked')
    expression = Input('.qos-info-row-expression .form-control')
    replicas_number = Input('.replicas-number-input')
    save = NamedButton('.ready', text='Save')
    close = NamedButton('.btn-default', text='Close')
    requirements = WebItemsSequence('.qos-entry', cls=Requirement)
    delete_confirm = NamedButton('.btn-danger', text='Yes, remove')

    def __str__(self):
        return 'Quality of Service modal'
