"""This module contains meta steps for operations on automation page concerning
 lambda creation in Onezone using web GUI
"""
__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import yaml

from tests.gui.steps.onezone.automation.automation_basic import *
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.onezone.automation.workflow_creation import (
    click_add_new_button_in_menu_bar, write_text_into_lambda_form,
    switch_toggle_in_lambda_form, confirm_lambda_creation_or_edition)
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} creates lambda with following '
                  'configuration:\n{config}'))
def create_lambda_manually(browser_id, config, selenium, oz_page, popups):

    """Create lambda according to given config.

        Config format given in yaml is as follows:
            name: lambda_name
            docker image: docker image
            mount space: True/False                 ---> optional
            read-only: True/False                   ---> optional
            arguments:
              - name: argument_name
                type: argument_type
              - name: 2nd_argument_name             ---> optional
                type: 2nd_argument_type
            results:                                ---> optional
              - name: result_name
                type: result_type


        Example configuration:

            name: "checksum-counting-oneclient"
            docker image: "docker.onedata.org/checksum-counting-oneclient:v8"
            read-only: False
            arguments:
              - name: "file"
                type: File
              - name: "metadata_key"
                type: String
              - name: "algorithm"
                type: String
            results:
              - name: "result"
                type: Object
    """
    _create_lambda_manually(browser_id, config, selenium, oz_page, popups)


def _create_lambda_manually(browser_id, config, selenium, oz_page, popups):

    button = 'Add new lambda'
    name_field = 'lambda name'
    docker_field = 'docker image'
    read_only_toggle = 'Read only'
    mount_space_toggle = 'Mount space'
    argument_option = 'argument'
    conf_param_option = 'configuration parameters'
    result_option = 'result'
    option = 'lambda'

    data = yaml.load(config)
    name = data['name']
    docker_image = data['docker image']
    read_only = data.get('read-only', True)
    mount_space = data.get('mount space', True)
    arguments = data.get('arguments', False)
    results = data.get('results', False)
    configuration_parameters = data.get('configuration parameters', False)

    read_only_option = 'checks' if read_only else 'unchecks'
    mount_space_option = 'checks' if mount_space else 'unchecks'

    click_add_new_button_in_menu_bar(selenium, browser_id, oz_page, button)
    write_text_into_lambda_form(selenium, browser_id, oz_page, name, name_field)
    write_text_into_lambda_form(selenium, browser_id, oz_page, docker_image,
                                docker_field)
    switch_toggle_in_lambda_form(selenium, browser_id, oz_page,
                                 read_only_option, read_only_toggle)
    switch_toggle_in_lambda_form(selenium, browser_id, oz_page,
                                 mount_space_option, mount_space_toggle)

    def ordinal(n):
        return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n
                                       % 10::4])

    if configuration_parameters:
        for i, config_param in enumerate(configuration_parameters):
            add_parameter_into_lambda_form(
                selenium, browser_id, oz_page, popups, conf_param_option,
                config_param['name'], config_param['type'], ordinal(i + 1))

    if arguments:
        for i, args in enumerate(arguments):
            add_parameter_into_lambda_form(
                selenium, browser_id, oz_page, popups, argument_option,
                args['name'], args['type'], ordinal(i+1))

    if results:
        for i, res in enumerate(results):
            add_parameter_into_lambda_form(
                selenium, browser_id, oz_page, popups, result_option,
                res['name'], res['type'], ordinal(i+1))

    confirm_lambda_creation_or_edition(selenium, browser_id, oz_page, option)


@wt(parsers.parse('user of {browser_id} creates "{lambda_name}" lambda from '
                  '"{docker_image}" docker image in "{inventory}" inventory'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_lambda_using_gui(selenium, browser_id, oz_page, lambda_name,
                            docker_image, inventory):
    click_on_option_in_the_sidebar(selenium, browser_id, 'Automation', oz_page)
    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'lambdas', oz_page)
    click_add_new_button_in_menu_bar(selenium, browser_id, oz_page,
                                     'Add new lambda')
    write_text_into_lambda_form(selenium, browser_id, oz_page,
                                lambda_name, 'lambda name')
    write_text_into_lambda_form(selenium, browser_id, oz_page,
                                docker_image, 'docker image')

    confirm_lambda_creation_or_edition(selenium, browser_id, oz_page, 'lambda')

    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'lambdas', oz_page)

    assert_lambda_exists(selenium, browser_id, oz_page, lambda_name)


@wt(parsers.re('user of (?P<browser_id>.*) changes (?P<ordinal>|1st |2nd |3rd '
               '|4th )(?P<option>argument|result|configuration parameters) '
               'named "(?P<name>.*)" to be "(?P<type>.*)" type'))
def change_parameter_type_in_lambda_form(selenium, browser_id, oz_page,
                                         popups, option, type, ordinal):
    driver = selenium[browser_id]
    page = oz_page(driver)['automation'].lambdas_page.form
    subpage = getattr(page, transform(option))

    ordinal = '1st' if not ordinal else ordinal
    bracket_name = 'bracket_' + ordinal.strip()
    object_bracket = getattr(subpage, bracket_name)
    css_sel = '#' + object_bracket.name.web_elem.get_attribute('id')
    scroll_to_css_selector(driver, css_sel)

    split_type = type.replace(')', '').split(' (')
    new_type = split_type[0] if 'Array' in type else type

    object_bracket.remove_element()
    object_bracket.type_dropdown.click()
    popups(driver).power_select.choose_item(new_type)

    if 'Array' in type:
        object_bracket.type_dropdown.click()
        popups(driver).power_select.choose_item(split_type[1])


@wt(parsers.re('user of (?P<browser_id>.*) adds '
               '(?P<ordinal>|1st |2nd |3rd |4th )(?P<option>argument|result'
               '|configuration parameters) named "(?P<name>.*)" '
               'of "(?P<type>.*)" type'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_parameter_into_lambda_form(selenium, browser_id, oz_page, popups,
                                   option, name, type, ordinal):
    driver = selenium[browser_id]
    page = oz_page(driver)['automation'].lambdas_page.form

    subpage = getattr(page, transform(option))
    subpage.add_button()
    ordinal = '1st' if not ordinal else ordinal
    bracket_name = 'bracket_' + ordinal.strip()
    object_bracket = getattr(subpage, bracket_name)

    name_input = object_bracket.name
    css_sel = '#' + name_input.web_elem.get_attribute('id')
    scroll_to_css_selector(driver, css_sel)
    name_input.value = name

    object_bracket.type_dropdown.click()
    popups(driver).power_select.choose_item(type)
