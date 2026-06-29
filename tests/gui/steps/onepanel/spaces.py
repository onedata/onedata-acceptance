"""This module contains gherkin steps to run acceptance tests featuring
spaces management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
import time
from subprocess import CalledProcessError

import yaml
from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.conftest import SELENIUM_IMPLICIT_WAIT, WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.common import wait_for_checking_toggle
from tests.gui.steps.common.docker import docker_ls
from tests.gui.steps.common.login import login_using_basic_auth
from tests.gui.steps.common.miscellaneous import _enter_text
from tests.gui.steps.modals.modal import wt_wait_for_modal_to_appear
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals, Onepanel, Popups
from tests.gui.utils.generic import implicit_wait, parse_seq, transform
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} selects "{storage}" from storage '
        "selector in support space form in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_storage_in_support_space_form(
    selenium: SeleniumDrivers, browser_id: str, storage: str
) -> None:
    storage_selector = Onepanel(
        selenium[browser_id]
    ).content.spaces.form.storage_selector
    storage_selector.click()
    Popups(selenium[browser_id]).power_select.choose_item(storage)


@wt(
    parsers.parse(
        "user of {browser_id} clicks on Support space button "
        "in spaces page in Onepanel if there are some spaces "
        "already supported"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_support_space_btn_on_condition(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    # set implicit wait in case spaces list take time to load,
    # otherwise one can miss it and not click the button
    with implicit_wait(driver, 1, SELENIUM_IMPLICIT_WAIT):
        spaces_page = Onepanel(driver).content.spaces
        if spaces_page.spaces.count() > 0:
            spaces_page.support_space()


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) selects (?P<btn>MiB|GiB|TiB) "
        "radio button in support space form in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_unit_in_space_support_form(
    selenium: SeleniumDrivers, browser_id: str, btn: str
) -> None:
    Onepanel(selenium[browser_id]).content.spaces.form.units[btn].click()


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) selects (?P<btn>auto|manual) "
        "radio button in support space form in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_mode_in_space_support_form(
    selenium: SeleniumDrivers, browser_id: str, btn: str
) -> None:
    form = Onepanel(selenium[browser_id]).content.spaces.form
    form.storage_import_configuration.modes[btn].click()


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) clicks on Support space "
        "button in support space form in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_space_support_form(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    Onepanel(selenium[browser_id]).content.spaces.form.support_space()


@wt(
    parsers.parse(
        "user of {browser_id} types received token to Support token "
        "field in support space form in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_received_token_to_support_token_field(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    form = Onepanel(selenium[browser_id]).content.spaces.form
    form.token = tmp_memory[browser_id]["mailbox"]["token"]


@wt(
    parsers.parse(
        'user of {browser_id} types "{text}" to {input_box} input '
        "field in support space form in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_input_box_in_space_support_form(
    selenium: SeleniumDrivers, browser_id: str, text: str, input_box: str
) -> None:
    form = Onepanel(selenium[browser_id]).content.spaces.form
    setattr(form, transform(input_box), text)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) enables "
        r"(?P<toggle>.*) option "
        r"in support space form in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enable_option_box_in_space_support_form(
    selenium: SeleniumDrivers, browser_id: str, toggle: str
) -> None:
    storage_import_configuration = Onepanel(
        selenium[browser_id]
    ).content.spaces.form.storage_import_configuration
    getattr(storage_import_configuration, transform(toggle)).check()


def wt_disable_option_box_in_space_support_form(
    selenium: SeleniumDrivers, browser_id: str, toggle: str
) -> None:
    storage_import_configuration = Onepanel(
        selenium[browser_id]
    ).content.spaces.form.storage_import_configuration
    getattr(storage_import_configuration, transform(toggle)).uncheck()


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{space_name}" space name is displayed in the'
        " supported spaces overview panel in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_correct_supported_space_opened(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    overview = Onepanel(selenium[browser_id]).content.spaces.space.overview
    assert (
        space_name == overview.space_name
    ), f'opened space "{overview.name}" instead of expected "{space_name}"'


@wt(
    parsers.parse(
        "user of {browser_id} sees that list of supported spaces "
        "is empty in Spaces page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_supported_spaces_list_is_empty(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    count = Onepanel(selenium[browser_id]).content.spaces.spaces.count()
    assert (
        count == 0
    ), f"There is(are) {count} supported spaces instead of expected none"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) selects (?P<strategy>.*?) "
        r"strategy from strategy selector in (?P<conf>IMPORT|UPDATE) "
        r"CONFIGURATION in support space form in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_strategy_in_conf_in_support_space_form(
    selenium: SeleniumDrivers, browser_id: str, strategy: str, conf: str
) -> None:
    config = getattr(
        Onepanel(selenium[browser_id]).content.spaces.form,
        conf.lower() + "_configuration",
    )
    strategy_selector = config.strategy_selector
    strategy_selector.expand()
    strategy_selector.options[strategy].click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" '
        r"to (?P<input_box>.*) input field in support space form "
        r"in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_input_box_in_storage_import_configuration(
    selenium: SeleniumDrivers, browser_id: str, text: str, input_box: str
) -> None:
    input_name = transform(input_box)
    form = Onepanel(selenium[browser_id]).content.spaces.form
    if hasattr(form, input_name):
        setattr(form, input_name, text)
    elif hasattr(form.storage_import_configuration, input_name):
        setattr(form.storage_import_configuration, input_name, text)
    else:
        raise RuntimeError(
            f"failed typing text into {input_box} input field in support space form "
        )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) selects (?P<strategy>.*?) "
        r"strategy from strategy selector in (?P<conf>IMPORT|UPDATE) "
        r'CONFIGURATION in "(?P<space>.*?)" record '
        r"in Spaces page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_strategy_in_conf_in_space_record(
    selenium: SeleniumDrivers, browser_id: str, strategy: str, conf: str
) -> None:
    config = getattr(
        Onepanel(selenium[browser_id]).content.spaces.space.sync_chart,
        conf.lower() + "_configuration",
    )
    strategy_selector = config.strategy_selector
    strategy_selector.expand()
    strategy_selector.options[strategy].click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" '
        r"to (?P<input_box>.*) input field in (?P<conf>IMPORT|UPDATE) "
        r'CONFIGURATION in "(?P<space>.*?)" record '
        r"in Spaces page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_input_box_in_conf_in_space_record(
    selenium: SeleniumDrivers,
    browser_id: str,
    text: str,
    input_box: str,
    conf: str,
) -> None:
    config = getattr(
        Onepanel(selenium[browser_id]).content.spaces.space.sync_chart,
        conf.lower() + "_configuration",
    )
    setattr(config, transform(input_box), text)


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {button} "
        'button in "{space}" record in Spaces page in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_button_in_space_record(
    selenium: SeleniumDrivers, browser_id: str, button: str
) -> None:
    driver = selenium[browser_id]
    sync_chart = Onepanel(driver).content.spaces.space.sync_chart
    getattr(sync_chart, transform(button)).click()


@wt(
    parsers.parse(
        'user of {browser_id} opens "{space}" record on '
        "spaces list in Spaces page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_open_space_item_in_spaces_page_op_panel(
    selenium: SeleniumDrivers, browser_id: str, space: str
) -> None:
    Onepanel(selenium[browser_id]).content.spaces.spaces[space].click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that {sync_type} strategy "
        'configuration for "{space_name}" is as follow:\n{conf}'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_proper_space_configuration_in_panel(
    selenium: SeleniumDrivers,
    browser_id: str,
    sync_type: str,
    space_name: str,
    conf: str,
) -> None:
    """Assert configuration displayed in space record in panel.

    conf should be in yaml format exactly as seen in panel, e.g.
        Mode: auto
        Max depth: 2
        Synchronize ACL: false
        Detect modifications: false
        Detect deletions: false
        Continuous scan: true
        Scan interval [s]: 10

    """

    driver = selenium[browser_id]
    space = Onepanel(driver).content.spaces.space
    space.navigation.overview()
    displayed_conf = getattr(space.overview, sync_type.lower() + "_strategy")

    for attr, val in yaml.load(conf, yaml.Loader).items():
        displayed_val = displayed_conf[attr]
        assert str(val).lower() == displayed_val.lower(), (
            f"Displayed {displayed_val} as {attr} instead of expected {val} in"
            f' {sync_type} strategy of "{space_name}" configuration'
        )


@wt(
    parsers.parse(
        'user of {browser_id} copies Id of "{space}" space in Spaces page in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_copy_space_id_in_spaces_page_in_onepanel(
    selenium: SeleniumDrivers, browser_id: str, space: str, tmp_memory: TmpMemory
) -> None:
    record = Onepanel(selenium[browser_id]).content.spaces.space
    tmp_memory["spaces"][space] = record.overview.space_id


@wt(
    parsers.parse(
        'user of {browser_id} expands toolbar for "{space_name}" '
        "space record in Spaces page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_expands_toolbar_icon_for_space_in_onepanel(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    driver = selenium[browser_id]
    Onepanel(driver).content.spaces.spaces[space_name].expand_menu()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on "
        r"(?P<option>Revoke space support|"
        r"Configure data synchronization|"
        r"Cancel sync. configuration) "
        r"option in space's toolbar in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_btn_in_space_toolbar_in_panel(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    toolbar = Popups(selenium[browser_id]).toolbar
    if toolbar.is_displayed():
        toolbar.options[option].click()
    else:
        raise RuntimeError("no space toolbar found in Onepanel")


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on "
        r"(?P<button>Cease support|Cancel) button "
        r"in cease oneprovider support for space modal in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_btn_in_cease_support_modal(
    selenium: SeleniumDrivers, browser_id: str, button: str
) -> None:
    modal = Modals(selenium[browser_id]).cease_support_for_space
    if button == "Cease support":
        modal.cease_support()
    else:
        modal.cancel()


# TODO: delete after space support revoke fixes in 21.02 (VFS-6383)
@wt(
    parsers.re(
        r"user of (?P<browser_id>\S+) removes space using "
        "delete space modal invoked from provided link"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_space_instead_of_revoke(selenium: SeleniumDrivers, browser_id: str) -> None:
    Modals(selenium[browser_id]).cease_support_for_space.space_delete_link()
    time.sleep(2)
    Modals(selenium[browser_id]).remove_modal.understand_notice()
    Modals(selenium[browser_id]).remove_modal.remove()


# TODO: delete after space support revoke fixes in 21.02 (VFS-6383)
@wt(
    parsers.parse(
        'user of {browser_id} logs in as "{user}" to Onezone service '
        "and removes space using delete space modal invoked from "
        "provided link"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def login_and_remove_space_instead_of_revoke(
    selenium: SeleniumDrivers,
    browser_id: str,
    user: str,
    users: Users,
    tmp_memory: TmpMemory,
) -> None:
    modal_name = "Cease oneprovider support for space"
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    Modals(selenium[browser_id]).cease_support_for_space.space_delete_link()
    time.sleep(3)
    login_using_basic_auth(selenium, browser_id, user, users, "Onezone")
    modal_name = "Remove space"
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    Modals(selenium[browser_id]).remove_modal.understand_notice()
    Modals(selenium[browser_id]).remove_modal.remove()


@wt(
    parsers.parse(
        "user of {browser_id} checks the understand notice "
        "in cease oneprovider support for space modal in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_understand_risk_in_cease_support_modal(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    (Modals(selenium[browser_id]).cease_support_for_space.understand_risk_checkbox())


@wt(
    parsers.parse(
        "user of {browser_id} clicks on "
        'Configure button in "{space}" '
        "record in Spaces page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_configure(selenium: SeleniumDrivers, browser_id: str) -> None:
    (Onepanel(selenium[browser_id]).content.spaces.space.sync_chart.configure())


@wt(
    parsers.parse(
        "user of {browser_id} clicks settings in Storage import in Spaces page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_option_in_spaces_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    space = Onepanel(selenium[browser_id]).content.spaces.space
    space.sync_chart.import_settings_list[0].click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that number of "
        r"(?P<bar_type>inserted|updated|deleted) files for "
        r'"(?P<space_name>.*?)" shown on Synchronization files '
        r"processing charts equals (?P<num>\d+) "
        r"in Spaces page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 10, interval=2)
def assert_correct_number_displayed_on_sync_charts(
    selenium: SeleniumDrivers,
    browser_id: str,
    bar_type: str,
    num: str,
    hosts: Hosts,
) -> None:
    files_mount_point = docker_ls("", hosts)
    try:
        files_dir1 = docker_ls("dir1", hosts)
    except CalledProcessError:
        files_dir1 = []
    try:
        files_dir2 = docker_ls("dir2", hosts)
    except CalledProcessError:
        files_dir2 = []

    expected_num = int(num)
    record = Onepanel(selenium[browser_id]).content.spaces.space
    displayed_num = getattr(record.sync_chart, bar_type)
    assert displayed_num == expected_num, (
        f"Displayed {displayed_num} as number of {bar_type} files on sync "
        f"chart instead of expected {num}. Files in mount point: "
        f"{files_mount_point}. Files in dir1: {files_dir1}."
        f"Files in dir2: {files_dir2}."
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees {tab_list} navigation tabs for space "{space_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def are_nav_tabs_for_space_displayed(
    selenium: SeleniumDrivers, browser_id: str, tab_list: str, space_name: str
) -> None:
    nav = Onepanel(selenium[browser_id]).content.spaces.spaces[space_name].navigation

    for tab in parse_seq(tab_list):
        assert (
            getattr(nav, transform(tab, strip_char='"')) is not None
        ), f"no navigation tab {tab} found"


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {tab_name} navigation "
        'tab in space "{space_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_navigation_tab_in_space(
    browser_id: str, tab_name: str, selenium: SeleniumDrivers
) -> None:
    nav = Onepanel(selenium[browser_id]).content.spaces.space.navigation
    tab = transform(tab_name, strip_char='"')
    getattr(nav, tab).click()


@wt(parsers.parse("user of {browser_id} clicks on {interval} update view"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_interval_update(
    browser_id: str, interval: str, selenium: SeleniumDrivers
) -> None:
    getattr(
        Onepanel(selenium[browser_id]).content.spaces.space.sync_chart,
        transform(interval + " view"),
    ).click()


@wt(
    parsers.parse(
        "user of {browser_id} cannot click on {tab_name} "
        'navigation tab in space "{space_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def cannot_click_on_navigation_tab_in_space(
    browser_id: str, tab_name: str, selenium: SeleniumDrivers
) -> None:
    nav = Onepanel(selenium[browser_id]).content.spaces.space.navigation
    tab = transform(tab_name, strip_char='"')
    try:
        getattr(nav, tab).click()
    except RuntimeError:
        return
    raise RuntimeError(f"can click on {tab_name}")


@wt(
    parsers.parse(
        'user of {browser_id} enables {toggle_name} in "{space}" space in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def enable_space_option_in_onepanel(
    selenium: SeleniumDrivers, browser_id: str, toggle_name: str
) -> None:
    driver = selenium[browser_id]
    option = toggle_name.replace("-", "_")
    tab = getattr(Onepanel(driver).content.spaces.space, option)
    toggle = getattr(tab, f"enable_{option}")
    toggle.check()
    wait_for_checking_toggle(toggle, toggle_name=toggle_name)


@wt(
    parsers.parse(
        "user of {browser_id} enables {option} in auto-cleaning tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def enable_option_in_auto_cleaning(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    tab = Onepanel(driver).content.spaces.space.auto_cleaning
    if option == "selective cleaning":
        tab.selective_cleaning.check()
    else:
        tab.selective_cleaning_form[option].checkbox.check()


@wt(
    parsers.parse(
        "user of {browser_id} clicks {option} on dropdown "
        "{rule} rule in auto-cleaning tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_option_on_dropdown_rule(
    selenium: SeleniumDrivers, browser_id: str, option: str, rule: str
) -> None:
    driver = selenium[browser_id]
    tab = Onepanel(driver).content.spaces.space.auto_cleaning
    for _ in range(20):
        time.sleep(0.2)
        if tab.selective_cleaning_form[rule].value_limit != option:
            tab.selective_cleaning_form[rule].dropdown_button()
            tab.selective_cleaning_form[rule].dropdown[option].click()
        else:
            break
    else:
        err_msg = f"Failed do set {rule} for {option}"
        assert tab.selective_cleaning_form[rule].value_limit == option, err_msg


@wt(
    parsers.parse(
        "user of {browser_id} clicks change {quota} quota button "
        "in auto-cleaning tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_change_quota_button(
    selenium: SeleniumDrivers, browser_id: str, quota: str
) -> None:
    button = f"click_rename_{quota}_quota_button"
    driver = selenium[browser_id]
    getattr(Onepanel(driver).content.spaces.space.auto_cleaning, button)(driver)


@wt(
    parsers.parse(
        'user of {browser_id} types "{value}" to {quota} quota '
        "input field in auto-cleaning tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_value_to_quota_input(
    selenium: SeleniumDrivers, browser_id: str, quota: str, value: str
) -> None:
    quota = f"{quota}_quota"
    driver = selenium[browser_id]
    _enter_text(
        getattr(Onepanel(driver).content.spaces.space.auto_cleaning, quota).edit_input,
        value,
    )


@wt(
    parsers.parse(
        "user of {browser_id} confirms changing value "
        "of {quota} quota in auto-cleaning tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_quota_value_change(
    selenium: SeleniumDrivers, browser_id: str, quota: str
) -> None:
    quota = f"{quota}_quota"
    driver = selenium[browser_id]
    getattr(Onepanel(driver).content.spaces.space.auto_cleaning, quota).accept_button()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Start cleaning now" button '
        "in auto-cleaning tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_start_cleaning_now(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    Onepanel(driver).content.spaces.space.auto_cleaning.start_cleaning_now()


@wt(
    parsers.parse(
        "user of {browser_id} sees {size} released size in cleaning report in Onepanel"
    )
)
@repeat_failed(
    interval=1,
    timeout=220,
    exceptions=(AssertionError, StaleElementReferenceException),
)
def see_released_size_in_cleaning_report(
    selenium: SeleniumDrivers, browser_id: str, size: str
) -> None:
    driver = selenium[browser_id]
    cleaning_reports = Onepanel(
        driver
    ).content.spaces.space.auto_cleaning.cleaning_reports
    for cleaning_report in cleaning_reports:
        match = re.match(
            r"((\d+) (MiB|B)) \(out of (\d*\.\d+|\d+) MiB\)",
            cleaning_report.released_size.text,
        )
        if match is None:
            raise ValueError(
                f"Cannot parse released size from: {cleaning_report.released_size.text}"
            )
        released_size = match.group(1)

        if released_size == size:
            return
    err_msg = f"released size: {released_size}  is not expected size: {size}"
    assert False, err_msg


def toggle_in_storage_import_configuration_is_enabled(
    selenium: SeleniumDrivers, browser_id: str, toggle_name: str
) -> bool:
    storage_import_conf = Onepanel(
        selenium[browser_id]
    ).content.spaces.form.storage_import_configuration
    return storage_import_conf.is_toggle_checked(transform(toggle_name))


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Start scan" button '
        "in storage import tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_start_scan_button_in_storage_import_tab(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    Onepanel(driver).content.spaces.space.sync_chart.start_scan()


@wt(
    parsers.parse(
        "user of {browser_id} waits until scanning is finished "
        "in storage import tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND, interval=4)
def wait_until_scanning_is_finished_in_storage_import_tab(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    assert Onepanel(
        driver
    ).content.spaces.space.sync_chart.start_scan_is_green(), (
        'Scanning did not finish correctly, "Start scan" button is not green'
    )


@wt(
    parsers.parse(
        "user of {browser_id} opens advanced settings "
        "in file popularity tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def open_advanced_settings_in_file_popularity_onepanel(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    Onepanel(driver).content.spaces.space.file_popularity.advanced_settings.click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "file popularity documentation" link '
        "in file popularity tab in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_docs_link_in_file_popularity_onepanel(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    Onepanel(
        driver
    ).content.spaces.space.file_popularity.file_popularity_documentation.click()
