"""Steps used for details modal handling in various GUI testing scenarios
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from datetime import datetime

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.modals.modal import check_modal_name
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees that {which_title} is "{title}" '
                  'in modal "{modal}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_chart_title_in_details_modal(selenium, browser_id, modals, title,
                                        which_title, modal):
    modal = check_modal_name(modal)
    modal = getattr(modals(selenium[browser_id]), modal).size_statistics
    if which_title == 'charts title':
        charts_title = modal.charts_title
    elif which_title == 'count chart title':
        charts_title = modal.chart[0].title
    else:
        charts_title = modal.chart[1].title
    assert charts_title == title, (f'Charts title is {charts_title} not '
                                   f'{title} as expected')


@wt(parsers.parse('user of {browser_id} clicks on chart in modal "{modal}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_chart_in_modal(browser_id, modals, selenium, modal):
    modal = check_modal_name(modal)
    getattr(modals(selenium[browser_id]),
            modal).size_statistics.click_on_chart()


@wt(parsers.parse('user of {browser_id} sees that "{element}" item displayed '
                  'in "{modal}" modal is not active'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_button_in_modal_not_active(browser_id, modal, element, modals,
                                      selenium):
    driver = selenium[browser_id]
    modal = getattr(modals(driver), check_modal_name(modal))
    err_msg = f'"{element}" button is in active state'
    assert not modal.is_element_active(transform(element)), err_msg


@wt(parsers.parse('user of {browser_id} sees that tooltip with size statistics'
                  ' header has date format in modal "{modal}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tooltip_on_chart_in_modal(browser_id, selenium, popups):
    driver = selenium[browser_id]
    header = popups(driver).chart_statistics.header
    try:
        datetime.strptime(header, '%H:%M %d/%m/%Y')
    except ValueError:
        raise Exception('Header: {header} of tooltip does not have date format')

