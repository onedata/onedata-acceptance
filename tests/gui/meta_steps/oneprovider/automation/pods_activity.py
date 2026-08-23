"""This module contains meta steps for operations on automation page checking
pods activity in Oneprovider using web GUI
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import yaml

from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.steps.modals.modal import click_modal_button, get_modal
from tests.gui.steps.oneprovider.automation.automation_basic import (
    click_on_link_in_task_box,
    click_on_task_in_lane,
)
from tests.gui.steps.oneprovider.automation.pods_activity import (
    change_tab_in_pods_activity_modal,
    click_on_first_pod_in_pods_activity_modal,
    wait_for_events_in_pods_activity_modal,
    wait_until_all_pods_are_terminated_in_pods_activity_modal,
)
from tests.gui.utils.common.modals.workflows_modals.pods_activity import (
    PodsActivity,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.parse(
        "user of {browser_id} waits for all pods to "
        'finish execution in modal "Function pods activity"'
    )
)
def wait_for_ongoing_pods_to_be_terminated(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    wait_until_all_pods_are_terminated_in_pods_activity_modal(driver)


@wt(
    parsers.parse(
        "user of {browser_id} sees that name of first pod in tab "
        '"{tab}" in modal "Function pods activity" contains lambda name "{lambda_name}"'
    )
)
def assert_lambda_name_in_tab_name(
    selenium: SeleniumDrivers, browser_id: str, tab: str, lambda_name: str
) -> None:
    switch_to_iframe(selenium, browser_id)
    modal = get_modal(selenium[browser_id], "Function pods activity", PodsActivity)
    change_tab_in_pods_activity_modal(modal, tab)
    pod_name = modal.pods_list[0].pod_name
    error_message = (
        f'Pod name: "{pod_name}" does not contain lambda name: "{lambda_name}"'
    )
    assert lambda_name in pod_name, error_message


@wt(
    parsers.parse(
        'user of {browser_id} clicks on first pod in tab "{tab}" '
        'in modal "Function pods activity"'
    )
)
def click_on_first_pod(selenium: SeleniumDrivers, browser_id: str, tab: str) -> None:
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    modal = get_modal(driver, "Function pods activity", PodsActivity)
    change_tab_in_pods_activity_modal(modal, tab)
    click_on_first_pod_in_pods_activity_modal(driver)


@wt(
    parsers.parse(
        "user of {browser_id} clicks on first terminated pod in "
        'modal "Function pods activity"'
    )
)
def click_on_first_terminated_pod(selenium: SeleniumDrivers, browser_id: str) -> None:
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    modal = get_modal(driver, "Function pods activity", PodsActivity)
    change_tab_in_pods_activity_modal(modal, "All")
    click_on_first_pod_in_pods_activity_modal(driver)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees events in modal "
        r'"Function pods activity" with following '
        r"(?P<option>reason|message)s:\n(?P<events>(.|\s)*)"
    )
)
def assert_events_in_pods_monitor(
    selenium: SeleniumDrivers, browser_id: str, events: str, option: str
) -> None:

    driver = selenium[browser_id]
    switch_to_iframe(selenium, browser_id)
    events_list = [
        event for event in yaml.load(events, yaml.Loader) if "+" not in event
    ]
    wait_for_events_in_pods_activity_modal(driver, events_list, option)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees events in modal "
        r'"Function pods activity" that contains lambda name '
        r'"(?P<lambda_name>.*)" and following '
        r"(?P<option>reason|message)s:\n(?P<events>(.|\s)*)"
    )
)
def assert_events_containing_lambda_name(
    selenium: SeleniumDrivers,
    browser_id: str,
    events: str,
    option: str,
    lambda_name: str,
) -> None:
    driver = selenium[browser_id]
    switch_to_iframe(selenium, browser_id)
    events_list = [
        event.replace('"', "").split(" + ")[1]
        for event in yaml.load(events, yaml.Loader)
        if "+" in event
    ]
    if not events_list:
        events_list = yaml.load(events, yaml.Loader)
    wait_for_events_in_pods_activity_modal(driver, events_list, option, lambda_name)


def get_lambda_name(events: str) -> str:
    events_list = yaml.load(events, yaml.Loader)
    for event in events_list:
        if "+" in event:
            lambda_name = (
                event.replace("message that contains: ", "")
                .replace('"', "")
                .split(" + ")[0]
            )
            return lambda_name
    raise ValueError("lambda name not found")


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees following "(?P<link>.*)" '
        r'(?P<option>reason|message)s for task "(?P<task>.*)" in '
        r'(?P<ordinal>.*) parallel box in "(?P<lane>.*)" lane '
        r"(?P<if_finished>after workflow execution is finished|during "
        r"workflow execution):\n(?P<events>(.|\s)*)"
    )
)
def checks_events_for_task(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane: str,
    task: str,
    ordinal: str,
    link: str,
    if_finished: str,
    option: str,
    events: str,
) -> None:
    click = "clicks on"
    close = "closes"
    button = "X"
    modal = "Function pods activity"

    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, lane, task, link, ordinal)
    if "finished" in if_finished:
        wait_for_ongoing_pods_to_be_terminated(selenium, browser_id)
        click_on_first_terminated_pod(selenium, browser_id)

    assert_events_in_pods_monitor(selenium, browser_id, events, option)
    lambda_name = get_lambda_name(events)

    assert_events_containing_lambda_name(
        selenium, browser_id, events, option, lambda_name
    )
    click_modal_button(selenium, browser_id, button, modal)
    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, close)


@wt(
    parsers.parse(
        "user of {browser_id} sees that name of first pod in tab"
        ' "{tab}" for task "{task}" in {ordinal} parallel box in '
        '"{lane}" lane contains lambda name "{lambda_name}"'
    )
)
def assert_pod_name_for_task(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane: str,
    task: str,
    ordinal: str,
    tab: str,
    lambda_name: str,
) -> None:
    click = "clicks on"
    close = "closes"
    link = "Pods activity"
    button = "X"
    modal = "Function pods activity"

    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, lane, task, link, ordinal)
    assert_lambda_name_in_tab_name(selenium, browser_id, tab, lambda_name)
    click_modal_button(selenium, browser_id, button, modal)
    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, close)


def check_number_of_events(
    selenium: SeleniumDrivers, browser_id: str, exp_num: str, task: str
) -> None:
    driver = selenium[browser_id]
    actual_num = int(
        get_modal(
            driver, "Function pods activity", PodsActivity
        ).get_number_of_data_rows(driver)
    )
    expected_num = int(exp_num)
    error_message = (
        f'numer of events on "Pods activity" ({actual_num}) for task '
        f'"{task}" is not about {expected_num}'
    )
    assert abs(actual_num - expected_num) <= 3, error_message


@wt(
    parsers.parse(
        "user of {browser_id} sees that numer of events on "
        '"Pods activity" list for task "{task}" in {ordinal}'
        ' parallel box in "{lane}" lane is about {exp_num}'
    )
)
def assert_number_of_events_in_task(
    browser_id: str,
    task: str,
    lane: str,
    exp_num: str,
    ordinal: str,
    selenium: SeleniumDrivers,
) -> None:
    click = "clicks on"
    close = "closes"
    link = "Pods activity"
    button = "X"
    modal = "Function pods activity"

    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, lane, task, link, ordinal)
    wait_for_ongoing_pods_to_be_terminated(selenium, browser_id)
    click_on_first_terminated_pod(selenium, browser_id)
    check_number_of_events(selenium, browser_id, exp_num, task)
    click_modal_button(selenium, browser_id, button, modal)
    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, close)
