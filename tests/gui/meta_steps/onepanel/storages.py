"""This module contains meta steps for operations on storages in Onepanel
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.utils.acceptance_utils import wt
from tests.gui.steps.onepanel.storages import (
    wt_expands_toolbar_icon_for_storage_in_onepanel,
    wt_clicks_on_btn_in_storage_toolbar_in_panel,
    assert_storage_disappeared_from_list)
from tests.gui.steps.modal import click_modal_button


@wt(parsers.parse('user of {browser_id} removes "{name}" storage '
                  'in Onepanel page'))
def remove_storage_in_op_panel_using_gui(selenium, browser_id, name,
                                         onepanel, popups):
    option = 'Remove storage'
    button = 'Remove'
    modal = 'REMOVE STORAGE'

    wt_expands_toolbar_icon_for_storage_in_onepanel(selenium, browser_id,
                                                    name, onepanel)
    wt_clicks_on_btn_in_storage_toolbar_in_panel(selenium, browser_id,
                                                 option, popups)
    click_modal_button(selenium, browser_id, button, modal)
    assert_storage_disappeared_from_list(selenium, browser_id, name,
                                         onepanel)

