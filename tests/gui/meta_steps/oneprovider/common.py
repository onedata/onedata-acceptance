"""This module contains meta steps for common operations in Oneprovider
using web GUI
"""

from pytest_bdd import given, parsers
from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.data_space_management import *
from tests.gui.steps.onezone.providers import *
from tests.gui.steps.oneprovider.common import *
from tests.gui.steps.oneprovider_common import *


@given(parsers.re('opened "(?P<tab_name>spaces)" tab in web GUI by '
                  '(users? of )?(?P<browser_id_list>.*)'))
def go_to_tab_in_provider(browser_id_list, tab_name, selenium):
    g_click_on_the_given_main_menu_tab(selenium, browser_id_list, tab_name)


def navigate_to_tab_in_op_using_gui(selenium, user, oz_page, provider,
                                    main_menu_tab):
    panel_name = button_name = "GO TO YOUR FILES"
    item_type = "provider"
    title = selenium[user].title

    if "onezone" in title.lower():
        wt_expand_oz_panel(selenium, user, panel_name, oz_page)
        assert_there_is_item_named_in_oz_panel_list(selenium, user, item_type,
                                                    provider, panel_name,
                                                    oz_page, hosts)
        wt_click_on_provider_in_go_to_your_files_oz_panel(selenium, user,
                                                          provider,
                                                          oz_page)
        assert_provider_popup_has_appeared_on_map(selenium, user, provider,
                                                  oz_page)
        wt_click_on_btn_in_provider_popup(selenium, user, button_name, provider,
                                          oz_page)
        wt_wait_for_op_session_to_start(selenium, user)

    wt_click_on_the_given_main_menu_tab(selenium, user, main_menu_tab)
