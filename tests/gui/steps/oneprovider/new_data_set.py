"""This module contains gherkin steps to run acceptance tests featuring
files add new data set in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} click Dataset write protection toggle'
                  ' on Datasets menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_protection_toggle(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modals(driver).file_datasets.dataset_protection_toggle.check()


@wt(parsers.parse('user of {browser_id} click Metadata write protection toggle'
                  ' on Datasets menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_protection_toggle(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modals(driver).file_datasets.metadata_protection_toggle.check()


@wt(parsers.parse('user of {browser_id} sees {text} label '
                  'in File Metadata menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_editor_disabled_label(browser_id, selenium, modals, text):
    driver = selenium[browser_id]
    item_status = modals(driver).metadata.editor_disabled
    assert item_status == text, f'{item_status} does not match expected {text}'



