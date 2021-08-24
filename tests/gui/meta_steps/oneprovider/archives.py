""""Meta steps for operations for datasets"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu)
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser,
    click_menu_for_elem_in_browser)
from tests.gui.steps.oneprovider.archives import (
    check_toggle_in_create_archive_modal,
    write_description_in_create_archive_modal)
from tests.gui.steps.modal import click_modal_button


@wt(parsers.parse('user of {browser_id} creates archive for item '
                  '"{item_name}" in "{space_name}" with following '
                  'configuration:\n{config}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_archive(browser_id, selenium, config, item_name, space_name,
                   oz_page, op_container, tmp_memory, modals):
    """Create archive according to given config.

    Config format given in yaml is as follow:

            description: archive_description        ---> optional
            layout: plain/BagIt
            create nested archives: True/False      ---> optional,
            incremental: True/False                 ---> optional
            include DIP: True/False                 ---> optional


    Example configuration:

          layout: plain
          incremental: True
    """
    _create_archive(browser_id, selenium, config, item_name, space_name,
                    oz_page, op_container, tmp_memory, modals)


@repeat_failed(timeout=WAIT_FRONTEND)
def _create_archive(browser_id, selenium, config, item_name, space_name,
                    oz_page, op_container, tmp_memory, modals):
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    option_in_data_row_menu = 'Create archive'
    button_name = 'Create'
    # options = parse_seq(options)
    try:
        op_container(selenium[browser_id]).dataset_browser.breadcrumbs
    except RuntimeError:
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      space_name,
                                                      option_in_space, oz_page)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, item_browser)
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   item_browser)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)

    data = yaml.load(config)

    description = data.get('description', False)
    layout = data['layout']
    create_nested_archives = data.get('create nested archives', False)
    incremental = data.get('incremental', False)
    include_dip = data.get('include DIP', False)

    if description:
        write_description_in_create_archive_modal(selenium, browser_id, modals,
                                                  description)
    if layout == 'BagIt':
        click_modal_button(selenium, browser_id, layout,
                           option_in_data_row_menu, modals)
    if create_nested_archives:
        option = 'create_nested_archives'
        check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                             option)
    if incremental:
        option = 'incremental'
        check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                             option)
    if include_dip:
        option = 'include_dip'
        check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                             option)

    click_modal_button(selenium, browser_id, button_name,
                       option_in_data_row_menu, modals)

