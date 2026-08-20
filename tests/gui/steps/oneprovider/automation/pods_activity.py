"""Steps for the Function pods activity modal in Oneprovider GUI."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.modals.modal import get_modal
from tests.gui.utils import Modals
from tests.gui.utils.common.modals.workflows_modals.function_pods_activity import (
    FunctionPodsActivity,
)
from tests.utils.utils import repeat_failed


def change_tab_in_function_pods_activity_modal(
    modal: FunctionPodsActivity, tab_name: str
) -> None:
    tab_number = 0 if tab_name == "Current" else 1

    time.sleep(0.25)
    modal.tabs[tab_number].click()
    time.sleep(0.25)


@repeat_failed(
    interval=1,
    timeout=180,
    exceptions=(AssertionError, StaleElementReferenceException),
)
def wait_until_all_pods_are_terminated_in_function_pods_activity_modal(
    driver: WebDriver,
) -> None:
    modal = Modals(driver).function_pods_activity
    change_tab_in_function_pods_activity_modal(modal, "Current")
    assert len(modal.pods_list) == 0, "Pods has not been terminated"


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_first_pod_in_function_pods_activity_modal(driver: WebDriver) -> None:
    modal = get_modal(driver, "Function pods activity", FunctionPodsActivity)
    modal.pods_list[0].click()


def gather_events_list(
    modal: FunctionPodsActivity, driver: WebDriver, option: str
) -> list[str]:
    number = int(modal.get_number_of_data_rows(driver))
    get_event = lambda i: modal.get_elem_by_data_row_id(  # pylint: disable=unnecessary-lambda-assignment
        i, driver, option
    )
    return [get_event(i) for i in range(number, -1, -1)]


@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_events_in_function_pods_activity_modal(
    driver: WebDriver,
    events: list[str],
    option: str,
    lambda_name: str | None = None,
) -> None:
    modal = get_modal(driver, "Function pods activity", FunctionPodsActivity)
    gathered_list = gather_events_list(modal, driver, option)

    for event in events:
        if lambda_name:
            assert any(
                event in gathered_event and lambda_name in gathered_event
                for gathered_event in gathered_list
            ), f"{option}: {event} that contains {lambda_name} has not been found"
        else:
            assert (
                event in gathered_list
            ), f"{option}: {event} has not been found. Events found: {gathered_list}"
