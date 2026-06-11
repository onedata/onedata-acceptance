"""This module contains gherkin steps to run acceptance tests featuring
common operations in onepanel web GUI.
"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.conftest import SeleniumDrivers
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.utils import Onepanel
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{button}" button on cluster members page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_btn_on_members_panel(
    selenium: SeleniumDrivers, browser_id: str, button: str
) -> None:
    driver = selenium[browser_id]
    interface = Onepanel(driver).content.members_emergency_interface
    getattr(interface, transform(button)).click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that number of direct users is "
        "equal {number} on cluster members page"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_equal_direct_user_number(
    selenium: SeleniumDrivers, browser_id: str, number: int
) -> None:
    driver = selenium[browser_id]
    interface = Onepanel(driver).content.members_emergency_interface
    user_number = interface.direct_users_number
    message_error = f"found {user_number} direct users instead of {number}"
    assert user_number == number, message_error
