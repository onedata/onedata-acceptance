"""Utils and fixtures to facilitate operations on modals."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from abc import abstractmethod

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Label, WebElement


class Modal(PageObject):
    title = Label(".modal-title")
    question_icon = Button(".oneicon-sign-question-rounded")
    documentation_link = WebElement(".documentation-link")

    @abstractmethod
    def __str__(self):
        pass
