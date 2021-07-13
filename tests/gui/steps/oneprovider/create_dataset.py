"""This module contains gherkin steps to run acceptance tests featuring
files create dataset in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} clicks Mark this directory as Dataset'
                  ' toggle on Datasets menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_mark_directory_as_dataset_toggle(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modals(driver).file_datasets.dataset_toggle.check()


@wt(parsers.parse('user of {browser_id} clicks Close button on Datasets'
                  ' menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_close_dataset_menu_button(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modals(driver).file_datasets.dataset_close_button()




