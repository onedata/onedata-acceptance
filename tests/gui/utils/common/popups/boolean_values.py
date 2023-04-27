"""Utils and fixtures to facilitate operations on choose boolean values popup.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label


class Options(PageObject):
    name = id = Label('.text')


class BooleanValues(PageObject):
    options = WebItemsSequence('.option-container', cls=Options)

    def __str__(self):
        return 'Boolean values'
