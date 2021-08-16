""""Meta steps for operations for datasets"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu,
    click_on_option_in_the_sidebar)
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.gui.steps.oneprovider.file_browser import (
    click_menu_for_elem_in_file_browser)
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser)
from tests.gui.steps.modal import click_modal_button


@wt(parsers.parse('user of {browser_id} clicks Mark this file as dataset toggle'
                  ' in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_mark_file_as_dataset_toggle(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modals(driver).datasets.dataset_toggle.check()


@wt(parsers.parse('user of {browser_id} creates dataset for item '
                  '"{item_name}" in "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_dataset(browser_id, tmp_memory, item_name, space_name,
                   selenium, oz_page, op_container, modals):

    try:
        op_container(selenium[browser_id]).file_browser.breadcrumbs
    except RuntimeError:
        click_on_option_in_the_sidebar(selenium, browser_id, 'Data', oz_page)
        click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                    'spaces', space_name,
                                                    oz_page)
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      space_name, 'Files',
                                                      oz_page)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory)
    click_menu_for_elem_in_file_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, 'Datasets',
                                             modals)
    click_mark_file_as_dataset_toggle(browser_id, selenium, modals)
    click_modal_button(selenium, browser_id, 'Close', 'Datasets', modals)
