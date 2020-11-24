"""This module contains gherkin steps to run acceptance tests featuring
emergency passphrase management in onepanel web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import _enter_text
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} clicks on {button} button on '
                  'emergency passphrase page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_emergency_passphrase_page(selenium, browser_id,
                                              onepanel, button):
    driver = selenium[browser_id]
    button = transform(button) + '_button'
    getattr(onepanel(driver).content.emergency_passphrase, button).click()


@wt(parsers.parse('user of {browser_id} types "{text}" to {input_field} input '
                  'field on emergency passphrase page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_input_on_emergency_passphrase_page(selenium, browser_id,
                                                    onepanel, text, input_field):
    driver = selenium[browser_id]
    input_field = transform(input_field) + '_input'
    field = getattr(onepanel(driver).content.emergency_passphrase, input_field)
    _enter_text(field, text)

