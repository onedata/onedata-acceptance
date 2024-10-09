"""This module contains gherkin steps to run acceptance tests featuring
spaces management in space overview page in onezone web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

import yaml
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} writes "{space_name}" '
        "into rename space text field"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_space_name_on_rename_space_input_on_overview_page(
    selenium, browser_id, space_name, oz_page
):
    driver = selenium[browser_id]
    oz_page(driver)["data"].overview_page.info_tile.rename()
    oz_page(driver)[
        "data"
    ].overview_page.info_tile.edit_name_box.value = space_name


@wt(
    parsers.parse(
        "user of {browser_id} clicks on confirmation button on overview page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_space_by_click_on_confirmation_button_on_overview_page(
    selenium, browser_id, oz_page
):
    driver = selenium[browser_id]
    oz_page(driver)["data"].overview_page.info_tile.edit_name_box.confirm()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on cancel button on overview page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_cancel_rename_button_on_overview_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["data"].overview_page.info_tile.edit_name_box.cancel()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) confirms rename the space "
        "using (?P<option>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_rename_the_space(selenium, browser_id, option, oz_page):
    if option == "enter":
        press_enter_on_active_element(selenium, browser_id)
    else:
        rename_space_by_click_on_confirmation_button_on_overview_page(
            selenium, browser_id, oz_page
        )


@wt(
    parsers.parse(
        "user of {browser_id} sees in the INFO section of Overview "
        "page that number of shares is {number}"
    )
)
def assert_number_of_shares_on_overview_page(
    browser_id, selenium, oz_page, number: int
):
    driver = selenium[browser_id]
    shares_count = int(
        oz_page(driver)["data"].overview_page.info_tile.shares_count
    )
    assert (
        number == shares_count
    ), f"number of shares equals {shares_count}, not {{number}} as expected"


@wt(
    parsers.parse(
        'user of {browser_id} sees "{space_name}" label on overview page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_name_label_of_space_on_overview_page(
    selenium, browser_id, space_name, oz_page
):
    driver = selenium[browser_id]
    assert (
        oz_page(driver)["data"].overview_page.space_name == space_name
    ), 'space "{}" not found on overview page'.format(space_name)


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_mes_at_field_in_space_details_in_overview(
    selenium, browser_id, text, field, oz_page
):
    driver = selenium[browser_id]
    details_tile = oz_page(driver)["data"].overview_page.space_details_tile
    field = transform(field)
    visible_mes = getattr(details_tile, field)
    err_msg = f"user sees {visible_mes} instead of {text} at {field}"
    assert text == visible_mes, err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tags_in_space_details_in_overview(
    selenium, browser_id, tags_to_check, oz_page
):
    tags = "tags"
    driver = selenium[browser_id]
    details_tile = oz_page(driver)["data"].overview_page.space_details_tile
    visible_mes = getattr(details_tile, tags)
    visible_tags = [t.text.split("\n")[0] for t in visible_mes]
    err_msg = f"user sees tags: {visible_tags} instead of {tags_to_check}"
    assert len(tags_to_check) == len(visible_tags), err_msg
    for tag in tags_to_check:
        assert tag in visible_tags, err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees that the space {option} "
        "advertised in the Marketplace tile in space overview "
        "subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_space_advertised_in_space_marketplace_in_overview(
    browser_id, option, selenium, oz_page
):
    driver = selenium[browser_id]
    marketplace_tile = oz_page(driver)["data"].overview_page.marketplace_tile
    advertise_info = marketplace_tile.advertise_info
    if option == "is":
        err_msg = (
            f"space should be advertised but visible info is {advertise_info}"
        )
        assert advertise_info == "Space advertised", err_msg
    elif option == "is not":
        err_msg = (
            "space should not be advertised but visible info is "
            f"{advertise_info}"
        )
        assert advertise_info == "Not advertised", err_msg


@wt(
    parsers.parse(
        'user of {browser_id} clicks "{link}" link '
        "in the Marketplace tile in space overview subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_link_in_space_marketplace_in_overview(
    browser_id, link, selenium, oz_page
):
    driver = selenium[browser_id]
    marketplace_tile = oz_page(driver)["data"].overview_page.marketplace_tile
    link = getattr(marketplace_tile, transform(link))
    link.click()


@wt(
    parsers.parse(
        "user of {browser_id} sees Space Details tile in space "
        "overview subpage with following information:\n{config}"
    )
)
def assert_space_in_overview_with_config(browser_id, selenium, oz_page, config):
    """Assert space advertised in marketplace according to given config.

    Config format given in yaml is as follows:
    tags:                               ---> optional
      - tag
    organization name: organization_name
    description: description

    Example configuration:
    tags:
      - archival
      - big-data
      - science
    organization name: "onedata"
    description: "Example of a space advertised in a Marketplace"

    """

    _assert_space_in_overview_with_config(browser_id, config, selenium, oz_page)


def _assert_space_in_overview_with_config(
    browser_id, config, selenium, oz_page
):
    data = yaml.load(config, yaml.Loader)

    organization_name_option = "organization name"
    description_option = "description"

    organization_name = data[organization_name_option]
    tags = data.get("tags", False)
    description = data[description_option]

    assert_mes_at_field_in_space_details_in_overview(
        selenium,
        browser_id,
        organization_name,
        organization_name_option,
        oz_page,
    )
    assert_mes_at_field_in_space_details_in_overview(
        selenium, browser_id, description, description_option, oz_page
    )

    if tags:
        assert_tags_in_space_details_in_overview(
            selenium, browser_id, tags, oz_page
        )
