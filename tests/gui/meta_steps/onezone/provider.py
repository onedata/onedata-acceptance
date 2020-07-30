"""Utils and fixtures to facilitate operations on providers in Onezone
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.utils.bdd_utils import parsers, given
from tests.utils.acceptance_utils import *

from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.onepanel.spaces import (
    wt_clicks_on_understand_risk_in_cease_support_modal,
    wt_clicks_on_btn_in_cease_support_modal)
from tests.gui.steps.onezone.providers import (
    assert_provider_hostname_matches_test_hostname,
    assert_provider_hostname_matches_known_domain,
    click_on_provider_in_providers_sidebar_with_provider_name,
    assert_provider_is_not_in_providers_list_in_data_sidebar,
    click_on_menu_button_of_provider_on_providers_list,
    click_on_cease_support_in_menu_of_provider_on_providers_list)
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.onezone.clusters import (copy_registration_cluster_token,
                                              click_button_in_cluster_page)


def assert_provider_has_name_and_hostname_in_oz_gui(selenium, user, oz_page,
                                                    provider_name,
                                                    domain_provider, hosts,
                                                    modals, with_refresh=False,
                                                    test_domain=False):
    option = 'Data'

    if with_refresh:
        refresh_site(selenium, user)

    click_on_option_in_the_sidebar(selenium, user, option, oz_page)
    click_on_provider_in_providers_sidebar_with_provider_name(selenium, user,
                                                              oz_page,
                                                              provider_name)

    if test_domain:
        assert_provider_hostname_matches_test_hostname(selenium, user,
                                                       domain_provider,
                                                       hosts, modals)
    else:
        assert_provider_hostname_matches_known_domain(selenium, user,
                                                      domain_provider,
                                                      hosts, modals)


def assert_there_is_no_provider_in_oz_gui(selenium, user, oz_page,
                                          provider_name, hosts):
    option = 'Data'

    refresh_site(selenium, user)
    click_on_option_in_the_sidebar(selenium, user, option, oz_page)
    assert_provider_is_not_in_providers_list_in_data_sidebar(selenium, user,
                                                             oz_page,
                                                             provider_name, hosts)


def send_copied_invite_token_in_oz_gui(selenium, user, oz_page, browser_list,
                                       tmp_memory, displays, clipboard):
    item_type = 'token'
    button = 'add new provider cluster'

    click_button_in_cluster_page(selenium, user, oz_page, button)
    copy_registration_cluster_token(selenium, user, oz_page)
    send_copied_item_to_other_users(user, item_type, browser_list,
                                    tmp_memory, displays, clipboard)


@wt(parsers.parse('user of {browser_id} revokes space support of "{provider}" '
                  'provider in oneproviders list in data sidebar'))
def revoke_support_of_provider_in_list(selenium, browser_id, provider, oz_page,
                                       popups, modals, hosts):
    driver = selenium[browser_id]
    provider_name = hosts[provider]['name']
    button = 'Cease support'
    notify_type = 'info'
    notify_text_regexp = 'Ceased.*[Ss]upport.*'

    click_on_menu_button_of_provider_on_providers_list(driver, provider_name,
                                                       oz_page)
    click_on_cease_support_in_menu_of_provider_on_providers_list(driver, popups)
    wt_clicks_on_understand_risk_in_cease_support_modal(selenium, browser_id,
                                                        modals)
    wt_clicks_on_btn_in_cease_support_modal(selenium, browser_id, button,
                                            modals)
    notify_visible_with_text(selenium, browser_id, notify_type,
                             notify_text_regexp)
