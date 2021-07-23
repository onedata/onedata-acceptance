"""This module contains gherkin steps to run acceptance tests featuring clusters
management in onezone web GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} clicks on Create automation inventory '
                  'button in automation sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_automation_button_in_panel(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['automation'].create_automation()


@wt(parsers.parse('user of {browser_id} writes "{text}" into inventory name '
                  'text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_name_into_input_box_on_main_automation_page(selenium, browser_id,
                                                      text, oz_page):
    oz_page(selenium[browser_id])['automation'].input_box.value = text


@wt(parsers.parse('user of {browser_id} clicks on confirmation button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_name_input_on_main_automation_page(selenium, browser_id,
                                               oz_page):
    oz_page(selenium[browser_id])['automation'].input_box.confirm()
