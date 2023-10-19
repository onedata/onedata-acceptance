"""This module contains gherkin steps to run acceptance tests featuring
spaces management in onezone web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.common.miscellaneous import (press_enter_on_active_element,
                                                  switch_to_iframe)
from tests.gui.steps.modals.modal import wt_wait_for_modal_to_appear
from tests.gui.utils.generic import transform, parse_seq
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


# @wt(parsers.parse('user of {browser_id} sees {tags} tags '
#                   'in space details in space overview page'))
# @repeat_failed(timeout=WAIT_FRONTEND)
# def assert_tags_in_space_details(selenium, browser_id, tags, oz_page):
#     driver = selenium[browser_id]
#     tags = parse_seq(tags)
#     details_tile = oz_page(driver)['data'].overview_page.spaces_details_tile
#     visible_tags = details_tile.space_tags
#     visible_tags = [t.text.split('\n')[0] for t in visible_tags]
#     #import pdb
#     #pdb.set_trace()
#     err_msg = f'user sees tags: {visible_tags} instead of {tags}'
#     assert len(tags) == len(visible_tags), err_msg
#     for tag in tags:
#         assert tag in visible_tags, err_msg


@wt(parsers.parse('user of {browser_id} sees {field}: {mes} '
                  'in space details in space overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_mes_at_field_in_space_details(selenium, browser_id, mes, field,
                                         oz_page):
    print(mes)
    print(field)
    driver = selenium[browser_id]
    field = transform(field)
    details_tile = oz_page(driver)['data'].overview_page.spaces_details_tile
    visible_mes = getattr(details_tile, field)
    if field == 'tags':
        tags = parse_seq(mes)
        visible_tags = [t.text.split('\n')[0] for t in visible_mes]
        err_msg = f'user sees tags: {visible_tags} instead of {tags}'
        assert len(tags) == len(visible_tags), err_msg
        for tag in tags:
            assert tag in visible_tags, err_msg
    else:
        err_msg = f'user sees {visible_mes} instead of {mes} at {field}'
        assert mes[1:-1] == visible_mes, err_msg
