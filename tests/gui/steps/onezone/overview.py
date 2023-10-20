"""This module contains gherkin steps to run acceptance tests featuring
spaces management in space overview page in onezone web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import transform, parse_seq
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.re('user of (?P<browser_id>.*?) sees (?P<text>.*?) '
               '(?P<field>Tags|Description|Organization name) in space details'
               ' in space overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_mes_at_field_in_space_details_in_overview(
        selenium, browser_id, text, field, oz_page):
    driver = selenium[browser_id]
    field = transform(field)
    details_tile = oz_page(driver)['data'].overview_page.space_details_tile
    visible_mes = getattr(details_tile, field)
    if field == 'tags':
        tags = parse_seq(text)
        visible_tags = [t.text.split('\n')[0] for t in visible_mes]
        err_msg = f'user sees tags: {visible_tags} instead of {tags}'
        assert len(tags) == len(visible_tags), err_msg
        for tag in tags:
            assert tag in visible_tags, err_msg
    else:
        # get rid of "" characters
        text = text[1:-1]
        err_msg = f'user sees {visible_mes} instead of {text} at {field}'
        assert text == visible_mes, err_msg


@wt(parsers.parse('user of {browser_id} sees that Space {option} advertised '
                  'in marketplace in space overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_space_advertised_in_space_marketplace_in_overview(
        browser_id, option, selenium, oz_page):
    driver = selenium[browser_id]
    marketplace_tile = oz_page(driver)['data'].overview_page.marketplace_tile
    advertise_info = marketplace_tile.advertise_info
    if option == 'is':
        err_msg = (f'space should be advertised but visible info is '
                   f'{advertise_info}')
        assert advertise_info == 'Space advertised', err_msg
    elif option == 'is not':
        err_msg = (f'space should not be advertised but visible info is '
                   f'{advertise_info}')
        assert advertise_info == 'Not advertised', err_msg


@wt(parsers.parse('user of {browser_id} clicks "{link}" link '
                  'in marketplace in space overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_advertised_in_space_marketplace_in_overview(
        browser_id, link, selenium, oz_page):
    driver = selenium[browser_id]
    marketplace_tile = oz_page(driver)['data'].overview_page.marketplace_tile
    link = getattr(marketplace_tile, transform(link))
    link.click()
