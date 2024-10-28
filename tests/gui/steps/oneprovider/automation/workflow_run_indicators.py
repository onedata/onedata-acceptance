"""This module contains gherkin steps to run acceptance tests featuring
workflows run indicators in oneprovider web GUI"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.steps.oneprovider.automation.automation_basic import (
    switch_to_automation_page,
)
from tests.utils.bdd_utils import parsers, wt


def get_run_indicators_for_lane(selenium, browser_id, op_container, lane_name):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    lane = workflow_visualiser.workflow_lanes[lane_name]
    return [elem.number for elem in lane.run_indicators]


@wt(
    parsers.parse(
        "user of {browser_id} sees that run indicator with "
        '"{number}" number has appeared on run bar for '
        '"{lane_name}" lane'
    )
)
def assert_run_indicator_for_lane(
    selenium, browser_id, op_container, lane_name, number
):
    run_indicators = get_run_indicators_for_lane(
        selenium, browser_id, op_container, lane_name
    )
    err_msg = (
        f'Run indicator with "{number}" does not appeared on run bar '
        f"for lane {lane_name}"
    )
    assert number in run_indicators, err_msg


@wt(
    parsers.parse(
        'user of {browser_id} sees that run indicator with "{number}"'
        ' number is the only indicator on run bar for "{lane_name}"'
        " lane"
    )
)
def assert_certain_indicator_is_only_one_in_lane(
    selenium, browser_id, op_container, lane_name, number
):
    assert_run_indicator_for_lane(selenium, browser_id, op_container, lane_name, number)
    run_indicators = get_run_indicators_for_lane(
        selenium, browser_id, op_container, lane_name
    )
    err_msg = (
        f'Run indicator with "{number}" is not the only one indicator '
        f'for "{lane_name}" lane'
    )
    assert len(run_indicators) == 1, err_msg


@wt(
    parsers.parse(
        'user of {browser_id} clicks on run indicator with "{number}"'
        ' number on run bar for "{lane_name}" lane'
    )
)
def click_on_run_indicator_for_lane(
    selenium, browser_id, op_container, lane_name, number
):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    lane = workflow_visualiser.workflow_lanes[lane_name]
    lane.run_indicators[number].click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that origin run number for"
        ' run "{run_number}" of "{lane_name}" lane is '
        '"{expected_origin_number}"'
    )
)
def assert_origin_run_number_for_run_in_lane(
    selenium,
    browser_id,
    op_container,
    lane_name,
    run_number,
    expected_origin_number,
):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    lane = workflow_visualiser.workflow_lanes[lane_name]
    origin_number = lane.run_indicators[run_number].origin_run_number
    err_msg = (
        f'Origin run number for "{run_number}" of "{lane_name}" lane'
        f" is {origin_number} and is different than expected "
        f"{expected_origin_number}"
    )
    assert origin_number == expected_origin_number, err_msg


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) sees that "
        '(?P<option>run|origin run|run type|status) is "(?P<value>.*?)" '
        'for run "(?P<number>.*?)" for "(?P<lane_name>.*?)" lane in'
        " popup that appeared after clicking run indicator"
    )
)
def assert_status_for_run_in_popup(
    selenium, browser_id, popups, option, value, op_container, lane_name, number
):
    click_on_run_indicator_for_lane(
        selenium, browser_id, op_container, lane_name, number
    )
    info = popups(selenium[browser_id]).run_info
    info_dict_list = {
        elem.split(": ")[0].lower(): elem.split(": ")[1] for elem in info.split("\n")
    }
    err_msg = f'{option} is not {value} for "{number}" run for "{lane_name}" lane'
    assert info_dict_list[option] == value.lower(), err_msg
