"""This module contains gherkin steps to run acceptance tests featuring
copy paste operations using local system clipboard.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.utils.bdd_utils import wt, parsers

from tests.gui.utils.generic import parse_seq


@wt(parsers.re('user of (?P<browser_id>.*?) sends copied (?P<item_type>.*?) '
               'to users? of (?P<browser_list>.*)'))
@wt(parsers.re('user of (?P<browser_id>.*?) sends copied (?P<item_type>.*?) '
               'to user named (?P<browser_list>.*)'))
def send_copied_item_to_other_users(browser_id, item_type, browser_list,
                                    tmp_memory, displays, clipboard):
    item = clipboard.paste(display=displays[browser_id])
    for browser in parse_seq(browser_list):
        tmp_memory[browser]['mailbox'][item_type.lower()] = item


@wt(parsers.parse('user of {browser_id} sees that copied token '
                  'matches displayed one'))
def assert_copied_token_match_displayed_one(browser_id, tmp_memory,
                                            displays, clipboard):
    displayed_token = tmp_memory[browser_id]['token']
    copied_token = clipboard.paste(display=displays[browser_id])
    err_msg = 'Displayed token: {} does not match copied one: ' \
              '{}'.format(displayed_token, copied_token)
    assert copied_token == displayed_token, err_msg


@wt(parsers.parse('user of {browser_id} sees that copied token '
                  'does not match displayed one'))
def assert_copied_token_does_not_match_displayed_one(browser_id, tmp_memory,
                                                     displays, clipboard):
    displayed_token = tmp_memory[browser_id]['token']
    copied_token = clipboard.paste(display=displays[browser_id])
    err_msg = 'Displayed token: {} match copied one: {} ' \
              'while it should not be'.format(displayed_token, copied_token)
    assert copied_token != displayed_token, err_msg
