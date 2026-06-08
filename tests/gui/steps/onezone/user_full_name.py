"""This module contains gherkin steps to run acceptance tests featuring
user full name management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2017-2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils import OZLoggedIn
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) clicks on "
        r"(?P<btn>confirm|cancel) button displayed next to user "
        r"full name edit box in Profile page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_btn_for_user_full_name_edit_box_in_oz(
    selenium: Any, browser_id: Any, btn: Any
) -> Any:
    getattr(OZLoggedIn(selenium[browser_id])["profile"].edit_box, btn).click()


@wt(
    parsers.parse(
        'user of {browser_id} types "{text}" to user full name edit box in Profile page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_into_user_full_name_edit_box_in_oz(
    selenium: Any, browser_id: Any, text: Any
) -> Any:
    OZLoggedIn(selenium[browser_id])["profile"].edit_box.value = text


@wt(
    parsers.parse(
        "user of {browser_id} activates edit box by clicking on "
        "the user full name in Profile page"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def activate_user_full_name_edit_box_in_oz(selenium: Any, browser_id: Any) -> Any:
    OZLoggedIn(selenium[browser_id])["profile"].rename_full_name()


@wt(
    parsers.parse(
        "user of {browser_id} sees that the user full name displayed "
        'in Profile page is "{expected_full_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_correct_usr_full_name_in_oz(
    selenium: Any, browser_id: Any, expected_full_name: Any
) -> Any:
    displayed_full_name = OZLoggedIn(selenium[browser_id])["profile"].full_name
    err_msg = (
        f'expected "{expected_full_name}" as user full name, but instead'
        f' displayed is "{displayed_full_name}" in USER FULL NAME oz panel'
    )

    assert displayed_full_name == expected_full_name, err_msg
