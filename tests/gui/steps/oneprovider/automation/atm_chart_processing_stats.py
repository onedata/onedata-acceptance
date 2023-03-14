"""This module contains gherkin steps to run acceptance tests featuring
wokrflows charts with processing stats in oneprovider web GUI """

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from datetime import datetime

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees that chart with processing '
                  'stats exist'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_processing_chart(browser_id, selenium, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    assert modal.chart, 'chart with processing stats is not visible'


@wt(parsers.parse('user of {browser_id} sees that time in right corner of chart'
                  ' with processing stats is around actual time'))
def assert_time_on_lower_right_corner_of_chart_is_around_actual_time(
        browser_id, selenium, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    chart_time_in_right_corner = modal.get_time_from_chart()[-1]
    now = datetime.now()
    ts = datetime.timestamp(now)
    assert abs(chart_time_in_right_corner - ts) < 120, (
        'Difference between actual time and time on chart is bigger than 120s')


@wt(parsers.parse('user of {browser_id} sees that value of last column on chart'
                  ' with processing stats is bigger than zero'))
def assert_value_of_last_column_is_bigger_than_zero(browser_id, selenium,
                                                    modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    values = modal.get_last_column_value()
    err_msg = (f'Last column {values[0][1]} is {values[0][0]} and'
               f' {values[1][1]} is {values[1][0]} when one of them should be '
               f'bigger than zero')
    assert (values[0][0] > 0 or values[1][0] > 0), err_msg


@wt(parsers.parse('user of {browser_id} chooses "{resolution}" resolution from'
                  ' time resolution list in modal "{modal}"'))
def choose_time_resolution(selenium, browser_id, popups, resolution, modal):
    driver = selenium[browser_id]
    for option in popups(driver).time_resolutions_list:
        if option.text == resolution:
            option.click()
            break
    else:
        raise Exception(f'There is no {resolution} in time resolution'
                        f' list in modal "{modal}".')


@wt(parsers.parse('user of {browser_id} sees that {option} processing speed'
                  ' is not bigger than {number} per second on chart with'
                  ' processing stats'))
def assert_number_of_proceeded_files(browser_id, selenium, modals, option,
                                     number):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    values = modal.get_last_column_value()
    for value in values:
        if option in value[1].lower():
            err_msg = (f'Processing speed is {value[0]} {option} per second '
                       f'and is bigger than expected {number} per second.')
            assert value[0] <= int(number), err_msg
            break
    else:
        raise Exception(f'There is no {option} processing speed on chart with'
                        f' processing stat.')

