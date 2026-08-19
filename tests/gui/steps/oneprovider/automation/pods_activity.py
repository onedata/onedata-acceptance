"""Steps for the Function pods activity modal in Oneprovider GUI."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.modals.modal import get_modal
from tests.gui.utils.common.modals.workflows_modals.function_pods_activity import (
    FunctionPodsActivity,
)
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_BACKEND)
def assert_no_pods_in_function_pods_activity_modal(driver: WebDriver) -> None:
    modal = get_modal(driver, "Function pods activity", FunctionPodsActivity)
    assert len(modal.pods_list) == 0, "Pods has not been terminated"


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_first_pod_in_function_pods_activity_modal(driver: WebDriver) -> None:
    modal = get_modal(driver, "Function pods activity", FunctionPodsActivity)
    modal.pods_list[0].click()
