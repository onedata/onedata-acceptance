"""This module contains gherkin steps to run acceptance tests featuring
harvester configuration management in onezone web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} {action} Public toggle on "
        "harvester configuration page"
    )
)
def check_public_toggle_on_harvester_config_page(
    selenium, browser_id, oz_page, action
):
    driver = selenium[browser_id]
    page = oz_page(driver)["discovery"].configuration_page
    if action == "checks":
        page.public.check()
    else:
        page.public.uncheck()


@wt(
    parsers.parse(
        "user of {browser_id} sees that Public toggle is {checked} "
        "on harvester configuration page"
    )
)
def assert_public_toggle_on_harvester_config_page(
    selenium, browser_id, oz_page, checked
):
    driver = selenium[browser_id]
    page = oz_page(driver)["discovery"].configuration_page
    if "not" in checked:
        assert page.public.is_unchecked(), "Harvester is checked as public"
    else:
        assert page.public.is_checked(), "Harvester is not checked as public"


@wt(
    parsers.parse(
        "user of {browser_id} clicks on copy icon of public harvester URL"
    )
)
def copy_public_harvester_url(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)[
        "discovery"
    ].configuration_page.general_tab.copy_public_url()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {tab_name} tab on "
        "harvester configuration page"
    )
)
def click_on_tab_of_harvester_config_page(
    selenium, browser_id, tab_name, oz_page
):
    driver = selenium[browser_id]
    page = oz_page(driver)["discovery"].configuration_page
    getattr(page, transform(tab_name) + "_button")()


@wt(
    parsers.parse(
        "user of {browser_id} chooses {plugin} GUI plugin "
        "from local directory to be uploaded"
    )
)
def upload_discovery_gui_plugin(selenium, browser_id, plugin, tmpdir, oz_page):
    driver = selenium[browser_id]
    path = tmpdir.join(browser_id).join(plugin)
    page = oz_page(driver)["discovery"].configuration_page.gui_plugin_tab
    uploader = page.upload_file_input
    uploader.send_keys(str(path))


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{button}" button in '
        "{tab_name} of harvester configuration page"
    )
)
def click_button_in_tab_of_harvester_config_page(
    selenium, browser_id, oz_page, button, tab_name
):
    driver = selenium[browser_id]
    page = getattr(
        oz_page(driver)["discovery"].configuration_page, transform(tab_name)
    )
    getattr(page, transform(button) + "_button")()


@wt(parsers.parse("user of {browser_id} waits until plugin upload finish"))
@repeat_failed(timeout=WAIT_BACKEND * 2)
def wait_until_plugin_upload_finish(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    page = oz_page(driver)["discovery"].configuration_page.gui_plugin_tab
    assert (
        page.gui_status == "uploaded"
    ), "GUI plugin upload not finished until given time"


@wt(
    parsers.parse(
        "user of {browser_id} sees that GUI plugin version is {version}"
    )
)
def assert_plugin_version(selenium, browser_id, version, oz_page):
    driver = selenium[browser_id]
    page = oz_page(driver)["discovery"].configuration_page.gui_plugin_tab
    assert (
        page.version == version
    ), f"Actual plugin version is {page.version} when expected {version}"


@wt(
    parsers.parse(
        "user of {browser_id} sees that harvester index for "
        '{plugin_index} GUI plugin index is "{harvester_index}"'
    )
)
def assert_plugin_index_value(
    selenium, browser_id, plugin_index, harvester_index, oz_page
):
    driver = selenium[browser_id]
    page = oz_page(driver)["discovery"].configuration_page.gui_plugin_tab
    actual_index_value = page.indices[plugin_index].harvester_index
    assert actual_index_value == harvester_index, (
        f"Actual {plugin_index} "
        "index value is "
        f"{actual_index_value} "
        "when expected "
        f"{harvester_index}"
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that injected configuration "
        "is: {configuration}"
    )
)
def assert_plugin_injected_config(selenium, browser_id, oz_page, configuration):
    driver = selenium[browser_id]
    page = oz_page(driver)["discovery"].configuration_page.gui_plugin_tab
    actual_conf = f"{{{page.injected_config}}}"
    assert actual_conf == configuration, (
        "Actual injected plugin config is "
        f"{actual_conf} when expected "
        f"{configuration}"
    )
