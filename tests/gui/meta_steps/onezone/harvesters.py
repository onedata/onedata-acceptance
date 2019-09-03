"""This module contains meta steps for operations on harvesters in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.onezone.members import *
from tests.gui.steps.onezone.discovery import (
    click_on_option_in_harvester_menu,
    click_button_on_discovery_on_left_sidebar_menu,
    type_text_to_input_field_in_discovery_page,
    type_endpoint_to_input_field_in_discovery_page,
    click_remove_space_option_in_menu_in_discover_spaces_page,
    click_create_button_in_discovery_page,
    click_on_option_of_harvester_on_left_sidebar_menu,
    type_index_name_to_input_field_in_indices_page,
    click_create_button_in_indices_page, click_button_in_harvester_spaces_page,
    choose_space_from_dropdown_in_add_space_modal)
from tests.gui.steps.onezone.spaces import (
    click_on_option_in_the_sidebar,
    click_element_on_lists_on_left_sidebar_menu)
from tests.gui.steps.modal import click_modal_button


@wt(parsers.parse('user of {browser_id} removes "{space_name}" space '
                  'from harvester'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_space_from_harvester(selenium, browser_id, oz_page, space_name):
    button = 'Remove'
    modal = 'Remove space from harvester'

    click_remove_space_option_in_menu_in_discover_spaces_page(selenium, browser_id,
                                                              space_name, oz_page)
    click_modal_button(selenium, browser_id, button, modal, oz_page)


@wt(parsers.parse('user of {browser_id} removes "{harvester_name}" '
                  'harvester in Onezone page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_harvester(selenium, browser_id, oz_page, harvester_name):
    where = 'Discovery'
    list_type = 'harvesters'
    option = 'Remove'
    modal = 'Remove harvester'

    click_on_option_in_the_sidebar(selenium, browser_id, where, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, list_type,
                                                harvester_name, oz_page)
    click_on_option_in_harvester_menu(selenium, browser_id, option,
                                      harvester_name, oz_page)
    click_modal_button(selenium, browser_id, option, modal)


@wt(parsers.parse('user of {browser_id} creates "{harvester_name}" harvester '
                  'in Onezone page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_harvester(selenium, browser_id, oz_page, harvester_name, hosts):
    where = 'Discovery'
    input_name = 'name'
    endpoint_input = 'endpoint'
    button_name = 'create new harvester'

    click_on_option_in_the_sidebar(selenium, browser_id, where, oz_page)
    click_button_on_discovery_on_left_sidebar_menu(selenium, browser_id,
                                                   button_name, oz_page)
    type_text_to_input_field_in_discovery_page(selenium, browser_id, oz_page,
                                               harvester_name, input_name)
    type_endpoint_to_input_field_in_discovery_page(selenium, browser_id,
                                                   oz_page, endpoint_input,
                                                   hosts)
    click_create_button_in_discovery_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} adds "{space_name}" space to '
                  '"{harvester_name}" harvester using available spaces dropdown'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_space_to_harvester(selenium, browser_id, oz_page, space_name,
                            harvester_name):
    option = 'Spaces'
    button_name = 'add one of your spaces'
    button_in_modal = 'Add'
    modal = 'Choose Space'

    click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                      harvester_name, option,
                                                      oz_page)
    click_button_in_harvester_spaces_page(selenium, browser_id, oz_page,
                                          button_name)
    choose_space_from_dropdown_in_add_space_modal(selenium, browser_id,
                                                  space_name, modals)
    click_modal_button(selenium, browser_id, button_in_modal, modal)


@wt(parsers.parse('user of {browser_id} creates "{index_name}" index '
                  'in "{harvester_name}" harvester in Discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_index_in_harvester(selenium, browser_id, oz_page, index_name,
                              harvester_name):
    option = 'Indices'

    click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                      harvester_name, option,
                                                      oz_page)
    type_index_name_to_input_field_in_indices_page(selenium, browser_id,
                                                   oz_page, index_name)
    click_create_button_in_indices_page(selenium, browser_id, oz_page)

