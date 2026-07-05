"""This module contains meta steps for operations on automation page concerning
task creation in Onezone using web GUI
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

import yaml

from tests.gui.steps.modals.modal import click_modal_button
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.steps.onezone.automation.workflow_creation import (
    add_another_parallel_box_to_lane,
    add_lambda_revision_to_workflow,
    add_parallel_box_to_lane,
    add_task_to_empty_parallel_box,
    choose_option_in_dropdown_menu_in_task_page,
    confirm_lambda_creation_or_edition,
    write_task_name_in_task_edition_text_field,
    write_text_into_editor_bracket,
)
from tests.gui.utils import OZLoggedIn, Popups
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) creates (?P<which>|another )task "
        "using (?P<ordinal>1st|2nd|3rd|4th) revision of "
        '"(?P<lambda_name>.*)" lambda in "(?P<lane_name>.*)" lane with '
        r"following configuration:\n(?P<config>(.|\s)*)"
    )
)
def create_task_using_previously_created_lambda(
    browser_id: str,
    config: str,
    selenium: SeleniumDrivers,
    lane_name: str,
    lambda_name: str,
    ordinal: str,
    which: str,
) -> None:
    """Create task using lambda according to given config.

    Config format given in yaml is as follows:
    where parallel box: "below"/"above"         ---> optional
    task name: task_name                        ---> optional
    arguments:                                  ---> optional
        task_arguments
    results:                                    ---> optional
        task_results


    Example configuration:

        where parallel box: "below"
        task name: "Second lambda task"
        arguments:
            file:
              value builder: "Iterated item"
            metadata_key:
              value builder: "Constant value"
              value: "sha256_key"
            algorithm:
              value builder: "Constant value"
              value: "sha256"
        results:
            result:
              target store: "output-store"
    """

    _create_task_using_previously_created_lambda(
        browser_id,
        config,
        selenium,
        lane_name,
        lambda_name,
        ordinal,
        which,
    )


def _create_task_using_previously_created_lambda(
    browser_id: str,
    config: str,
    selenium: SeleniumDrivers,
    lane_name: str,
    lambda_name: str,
    ordinal: str,
    which: str,
) -> None:
    arg_type = "argument"
    res_type = "result"
    conf_param_option = "configuration parameters"
    option = "task"
    data = yaml.load(config, yaml.Loader)
    arguments = data.get("arguments", False)
    results = data.get("results", False)
    task_name = data.get("task name", False)
    configuration_parameters = data.get("configuration parameters", False)

    if "another" in which:
        position = data["where parallel box"]
        add_another_parallel_box_to_lane(selenium, browser_id, lane_name, position)
    else:
        add_parallel_box_to_lane(selenium, browser_id, lane_name)

    time.sleep(0.5)
    add_task_to_empty_parallel_box(selenium, browser_id, lane_name)
    time.sleep(0.5)
    add_lambda_revision_to_workflow(selenium, browser_id, lambda_name, ordinal)

    if task_name:
        write_task_name_in_task_edition_text_field(selenium, browser_id, task_name)

    if configuration_parameters:
        for param_name, param in configuration_parameters.items():
            choose_option_in_dropdown_menu_in_task_page(
                selenium,
                browser_id,
                param["value builder"],
                param_name,
                conf_param_option,
            )
            write_text_into_editor_bracket(
                selenium,
                browser_id,
                param["value"],
                param_name,
                conf_param_option,
            )

    if arguments:
        for arg_name, arg in arguments.items():
            choose_option_in_dropdown_menu_in_task_page(
                selenium,
                browser_id,
                arg["value builder"],
                arg_name,
                arg_type,
            )
            if "value" in arg:
                write_text_into_editor_bracket(
                    selenium,
                    browser_id,
                    arg["value"],
                    arg_name,
                    arg_type,
                )

    if results:
        for res_name, res in results.items():
            choose_option_in_dropdown_menu_in_task_page(
                selenium,
                browser_id,
                res["target store"],
                res_name,
                res_type,
            )

    confirm_lambda_creation_or_edition(selenium, browser_id, option)


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) removes "(?P<task>.*)" task'
        ' from (?P<ordinal>.*) parallel box in "(?P<lane>.*)" lane'
    )
)
def remove_task_from_lane(
    selenium: SeleniumDrivers, browser_id: str, lane: str, task: str
) -> None:
    modal = "Remove task"
    option = "Remove"

    driver = selenium[browser_id]
    page = OZLoggedIn(driver).automation
    lane_obj = page.workflows_page.workflow_visualiser.workflow_lanes[lane]
    lane_obj.parallel_box.task_list[task].menu_button()
    Popups(driver).menu_popup_with_label.menu[option]()
    click_modal_button(selenium, browser_id, option, modal)


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) modifies "(?P<task>.*)" task in '
        '(?P<ordinal>.*) parallel box in "(?P<lane>.*)" lane by '
        r"(?P<option>adding|changing) following:\n(?P<config>(.|\s)*)"
    )
)
def modify_task_results(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane: str,
    task: str,
    config: str,
    option: str,
) -> None:
    conf_param_option = "configuration parameters"
    data = yaml.load(config, yaml.Loader)
    results_conf = data.get("results", False)
    lambda_conf = data.get("lambda", False)
    configuration_parameters = data.get(conf_param_option, False)
    button = "Modify"
    task_option = "task"

    driver = selenium[browser_id]
    page = OZLoggedIn(driver).get_page("automation", click=True)
    lane_obj = page.workflows_page.workflow_visualiser.workflow_lanes[lane]
    lane_obj.parallel_box.task_list[task].menu_button()
    Popups(driver).menu_popup_with_label.menu[button]()
    # wait for task form to open
    time.sleep(1)

    if lambda_conf:
        revision = from_ordinal_number_to_int(lambda_conf[0]["revision"])
        page.workflows_page.task_form.lambda_revision.click()
        Popups(driver).power_select.choose_item(str(revision))

    if results_conf:
        for res in results_conf:
            [(res_name, new_res)] = res.items()
            try:
                result = page.workflows_page.task_form.results[res_name]
            except RuntimeError:
                result = page.workflows_page.task_form.results[res_name + ":"]
            if option == "adding":
                result.add_mapping()
            element = result.target_store_dropdown[-1]
            driver.execute_script("arguments[0].scrollIntoView();", element)
            result.target_store_dropdown[-1].click()
            Popups(driver).power_select.choose_item(new_res)

    if configuration_parameters:
        for param_name, param in configuration_parameters.items():
            choose_option_in_dropdown_menu_in_task_page(
                selenium,
                browser_id,
                param["value builder"],
                param_name,
                conf_param_option,
            )
            write_text_into_editor_bracket(
                selenium,
                browser_id,
                param["value"],
                param_name,
                conf_param_option,
            )

    confirm_lambda_creation_or_edition(selenium, browser_id, task_option)
