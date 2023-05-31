"""This module contains meta steps for operations on automation page concerning
 store creation in Onezone using web GUI
"""
__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import yaml


from tests.gui.steps.modals.modal import (click_modal_button,
                                          write_name_into_text_field_in_modal, check_checkbox_in_modal,
                                          choose_option_in_dropdown_menu_in_modal)
from tests.gui.steps.onezone.automation.workflow_creation import (
    click_add_store_button)
from tests.utils.bdd_utils import wt, parsers


@wt(parsers.re('user of (?P<browser_id>.*) creates (input|output) store for '
               'workflow "(?P<workflow>.*)" with following configuration:'
               r'\n(?P<config>(.|\s)*)'))
def create_store_for_workflow(browser_id, config, selenium, oz_page, modals,
                              popups):
    """Create store according to given config.

        Config format given in yaml is as follows:
            name: store_name
            type dropdown: type                     ---> optional
            data type dropdown: data_type
            user input: True/False                  ---> optional

        Example configuration:

            name: "output"
            type dropdown: List
            data type dropdown: Object
    """
    _create_store_for_workflow(browser_id, config, selenium, oz_page, modals,
                               popups)


def _create_store_for_workflow(browser_id, config, selenium, oz_page, modals,
                               popups):
    data = yaml.load(config)
    name = data['name']

    type_dropdown = data['type dropdown']
    data_type_dropdown = data['data type dropdown']
    user_input = data.get('user input', False)

    name_textfield = 'store name'
    modal_name = 'Create new store'
    type_dropdown_menu = 'type dropdown menu'
    data_type_dropdown_menu = 'data type dropdown menu'
    toggle_name = 'User input'
    option = 'checks' if user_input else 'unchecks'
    button = 'Create'

    click_add_store_button(selenium, browser_id, oz_page)
    write_name_into_text_field_in_modal(selenium, browser_id, name, modal_name,
                                        modals, name_textfield)
    choose_option_in_dropdown_menu_in_modal(selenium, browser_id, modals,
                                            type_dropdown_menu, popups,
                                            type_dropdown, modal_name)
    choose_option_in_dropdown_menu_in_modal(selenium, browser_id, modals,
                                            data_type_dropdown_menu, popups,
                                            data_type_dropdown, modal_name)
    check_checkbox_in_modal(selenium, browser_id, modals, toggle_name,
                            option, modal_name)
    click_modal_button(selenium, browser_id, button, modal_name, modals)
