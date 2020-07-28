"""Steps implementation for quality of service GUI tests.
"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from pytest_bdd import parsers
from selenium.common.exceptions import NoSuchElementException

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.modal import click_modal_button
from tests.utils.bdd_utils import wt
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} deletes all QoS requirements'))
@repeat_failed(timeout=WAIT_FRONTEND)
def delete_all_qualities_of_service(selenium, browser_id, modals, popups):
    driver = selenium[browser_id]
    modal = modals(driver).quality_of_service
    while len(modal.requirements):
        modal.requirements[0].delete.click()
        popups(driver).delete_qos_popup.confirm.click()


@wt(parsers.parse('user of {browser_id} sees that all QoS requirements are '
                  '{state}'))
@repeat_failed(interval=1, timeout=90,
               exceptions=(NoSuchElementException, RuntimeError))
def assert_all_qualities_of_service_are_fulfilled(selenium, browser_id,
                                                  modals, state):
    driver = selenium[browser_id]
    modal = modals(driver).quality_of_service
    for requirement in modal.requirements:
        assert hasattr(requirement, state), f'no such attribute'
