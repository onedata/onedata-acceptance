"""Utils and fixtures to facilitate operations on providers in Onezone
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.onezone.providers import (
    assert_provider_hostname_matches_test_hostname,
    assert_provider_hostname_matches_known_domain,
    click_on_provider_in_data_sidebar_with_provider_name,
    assert_provider_in_providers_list_in_data_sidebar)
from tests.gui.steps.onezone.spaces import click_on_spaces_in_the_sidebar


def assert_provider_has_name_and_hostname_in_oz_gui(selenium, user, oz_page,
                                                    provider_name,
                                                    domain_provider, hosts,
                                                    modals, with_refresh=False,
                                                    test_domain=False):
    option = 'Data'

    if with_refresh:
        refresh_site(selenium, user)

    click_on_spaces_in_the_sidebar(selenium, user, option, oz_page)
    click_on_provider_in_data_sidebar_with_provider_name(selenium, user,
                                                         oz_page, provider_name)

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
    click_on_spaces_in_the_sidebar(selenium, user, option, oz_page)
    assert_provider_in_providers_list_in_data_sidebar(selenium, user, oz_page,
                                                      provider_name, hosts)

