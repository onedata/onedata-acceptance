"""This module contains gherkin steps to run acceptance tests featuring
shares management using sidebar in onezone web GUI.
"""

__author__ = "Jakub Pilch"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees space name "{space_name}" of '
                  '"{share_name}" share in shares list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_space_name_for_share_matches_expected(selenium, browser_id, oz_page,
                                                 share_name, space_name):
    shares_list = oz_page(selenium[browser_id])['shares'].shares_list
    share_names_list = {share.name for share in shares_list}

    if share_name not in share_names_list:
        raise RuntimeError(f'Share {share_name} not in shares sidebar')

    found_space_name = shares_list[share_name].space_name
    assert space_name == found_space_name, (f'Space name for share '
                                            f'"{share_name}": '
                                            f'"{found_space_name} does not '
                                            f'match expected: "{space_name}')


@wt(parsers.parse('user of {browser_id} sees share name "{share_name}" in the '
                  'shares list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_share_name_in_shares_sidebar(selenium, browser_id, oz_page,
                                        share_name):
    shares_list = oz_page(selenium[browser_id])['shares'].shares_list
    share_names_list = {share.name for share in shares_list}

    assert share_name in share_names_list, (f'Share {share_name} not in '
                                            f'shares sidebar')