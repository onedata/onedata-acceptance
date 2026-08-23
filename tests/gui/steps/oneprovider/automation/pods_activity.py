"""Steps for the Function pods activity modal in Oneprovider GUI."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_FRONTEND, WAIT_PODS_TERMINATION
from tests.gui.steps.modals.modal import get_modal
from tests.gui.utils import Modals
from tests.gui.utils.common.modals.workflows_modals.pods_activity import (
    PodsActivity,
)
from tests.utils.utils import repeat_failed


def change_tab_in_pods_activity_modal(modal: PodsActivity, tab_name: str) -> None:
    tab_number = 0 if tab_name == "Current" else 1
    modal.tabs[tab_number].click()


@repeat_failed(
    interval=1,
    timeout=WAIT_PODS_TERMINATION,
    exceptions=(AssertionError, StaleElementReferenceException),
)
def assert_all_pods_are_terminated(modal: PodsActivity) -> None:
    assert len(modal.pods_list) == 0, "Pods has not been terminated"


def wait_until_all_pods_are_terminated_in_pods_activity_modal(
    driver: WebDriver,
) -> None:
    modal = Modals(driver).pods_activity
    change_tab_in_pods_activity_modal(modal, "Current")
    assert_all_pods_are_terminated(modal)


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_first_pod_in_pods_activity_modal(modal: PodsActivity) -> None:
    modal.pods_list[0].click()


def gather_events_list(
    modal: PodsActivity, driver: WebDriver, option: str
) -> list[str]:
    number = int(modal.get_number_of_data_rows(driver))
    get_event = lambda i: modal.get_elem_by_data_row_id(  # pylint: disable=unnecessary-lambda-assignment
        i, driver, option
    )
    return [get_event(i) for i in range(number, -1, -1)]


def assert_each_event_is_gathered(
    events: list[str],
    gathered_events: list[str],
    option: str,
) -> None:
    for event in events:
        assert event in gathered_events, (
            f'No gathered event with {option} "{event}" was found. '
            f"Gathered {option}s: {gathered_events}"
        )


def is_event_gathered_with_lambda(
    event: str, lambda_name: str, gathered_events: list[str]
) -> bool:
    for gathered_event in gathered_events:
        if event in gathered_event and lambda_name in gathered_event:
            return True
    return False


def assert_each_event_is_gathered_with_lambda(
    events: list[str],
    lambda_name: str,
    gathered_events: list[str],
    option: str,
) -> None:
    for event in events:
        is_event_gathered = is_event_gathered_with_lambda(
            event, lambda_name, gathered_events
        )

        assert is_event_gathered, (
            f'No gathered event with {option} containing "{event}" '
            f'and lambda name "{lambda_name}" was found. '
            f"Gathered {option}s: {gathered_events}"
        )


@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_events_in_pods_activity_modal(
    driver: WebDriver,
    events: list[str],
    option: str,
    lambda_name: str | None = None,
) -> None:
    modal = get_modal(driver, "Function pods activity", PodsActivity)
    gathered_events = gather_events_list(modal, driver, option)

    if lambda_name:
        assert_each_event_is_gathered_with_lambda(
            events, lambda_name, gathered_events, option
        )
    else:
        assert_each_event_is_gathered(events, gathered_events, option)
