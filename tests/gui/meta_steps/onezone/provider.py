"""Utils and fixtures to facilitate operations on providers in Onezone
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.onezone.providers import (
    assert_provider_hostname_matches_given_domain,
    assert_provider_popup_has_appeared_on_map,
    wt_click_on_provider_in_go_to_your_files_oz_panel)


def assert_provider_has_name_and_hostname_in_oz_gui(selenium, user, oz_page,
                                                    provider_name, host, hosts,
                                                    with_refresh=False):
    panel_name = "GO TO YOUR FILES"
    item_type = "provider"

    if with_refresh:
        refresh_site(selenium, user)
    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    assert_there_is_item_named_in_oz_panel_list(selenium, user, item_type,
                                                provider_name, panel_name,
                                                oz_page, hosts)
    wt_click_on_provider_in_go_to_your_files_oz_panel(selenium, user,
                                                      provider_name, oz_page,
                                                      hosts)
    assert_provider_popup_has_appeared_on_map(selenium, user, provider_name,
                                              oz_page)
    assert_provider_hostname_matches_given_domain(selenium, user, host, oz_page)


def assert_there_is_no_provider_in_oz_gui(selenium, user, oz_page,
                                          provider_name, hosts):
    panel_name = "GO TO YOUR FILES"
    item_type = "provider"

    refresh_site(selenium, user)
    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    assert_there_is_no_item_named_in_oz_panel_list(selenium, user, item_type,
                                                   provider_name, panel_name,
                                                   oz_page, hosts)
