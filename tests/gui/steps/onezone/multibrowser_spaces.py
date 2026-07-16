"""This module contains gherkin steps to run acceptance tests featuring
joining spaces in onezone web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils import OZLoggedIn
from tests.gui.utils.generic import parse_elements_sequence
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} sends invitation {item_type} to "{browser_list}"'
    ),
    converters={
        "browser_list": parse_elements_sequence,
    },
)
@repeat_failed(timeout=WAIT_FRONTEND)
def send_invitation_token_to_browser(
    browser_id: str,
    item_type: str,
    displays: dict[str, str],
    clipboard: Clipboard,
    browser_list: list[str],
    tmp_memory: TmpMemory,
) -> None:
    item = clipboard.paste(display=displays[browser_id])
    for browser in browser_list:
        tmp_memory[browser]["mailbox"][item_type.lower()] = item


@wt(
    parsers.parse(
        'user of {browser_id} clicks "{group_name}" on the groups list in the sidebar'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_group_on_groups_on_left_sidebar_menu(
    selenium: SeleniumDrivers, browser_id: str, group_name: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).groups.groups_list[group_name].click()
