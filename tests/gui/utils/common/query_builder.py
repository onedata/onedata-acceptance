"""Utils to facilitate operations on query builder (used e.g. on data
discovery page and QoS modal)"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, WebElementsSequence


class QueryBuilder(PageObject):
    root_block = Button('.root-block')
    another_block_buttons = WebElementsSequence(
        '.query-builder-block-adder.clickable')
    query_button = Button('.submit-query')
