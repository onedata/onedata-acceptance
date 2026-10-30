"""This module contains meta steps for operations on Space Marketplaces
in Onezone using web GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import yaml

from tests.gui.steps.onezone.space_configuration import (
    add_tags_in_space_configuration_tab,
    set_description_of_a_space,
    set_space_data_in_configuration_tab,
)
from tests.gui.steps.onezone.space_marketplace import (
    assert_creation_time_in_space_marketplace,
    assert_element_in_space_marketplace,
    assert_elements_list_in_space_marketplace,
    assert_marketplace_refresh_button_is_enabled,
    assert_space_with_request_access_in_marketplace_subpage,
    clear_marketplace_tags_filter,
    click_marketplace_tags_selector_trigger,
    select_marketplace_tag,
    select_marketplace_tag_category,
    write_into_marketplace_search_input,
)
from tests.gui.steps.rest.spaces import modify_space_using_rest
from tests.type_definitions import Hosts, JsonValue, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.user_utils import Users


@given(
    parsers.parse(
        'using REST, user {user} configures "{space_name}" space in "{zone_host}" '
        "Onezone service as follows:\n{config}"
    )
)
def configure_space_using_rest(
    user: str,
    space_name: str,
    zone_host: str,
    config: str,
    hosts: Hosts,
    users: Users,
    spaces: dict[str, str],
) -> None:
    space_data = yaml.load(config, yaml.Loader)
    modify_space_using_rest(
        hosts[zone_host]["hostname"],
        users[user].username,
        users[user].password,
        spaces[space_name],
        space_data,
    )


def update_marketplace_tags_filter(selenium: SeleniumDrivers, browser_id: str, config: str) -> None:
    tags_to_add: dict[str, list[str]] = yaml.load(config, yaml.Loader)

    clear_marketplace_tags_filter(selenium, browser_id)
    click_marketplace_tags_selector_trigger(selenium, browser_id)
    for tag_type, tags in tags_to_add.items():
        select_marketplace_tag_category(selenium, browser_id, tag_type)
        for tag in tags:
            select_marketplace_tag(selenium, browser_id, tag)
    click_marketplace_tags_selector_trigger(selenium, browser_id)


@wt(parsers.parse("user of {browser_id} sets Marketplace filters as follows:\n{config}"))
def set_marketplace_filters(browser_id: str, config: str, selenium: SeleniumDrivers) -> None:
    """Set any combination of the Marketplace search and tags filters.

    Example configuration:
        search: "example"              ---> optional
        tags:                           ---> optional
          general:
            - archival
            - demo
    """
    data: dict[str, JsonValue] = yaml.load(config, yaml.Loader)

    if "search" in data:
        search_input: str = data["search"]
        write_into_marketplace_search_input(selenium, browser_id, search_input)

    if "tags" in data:
        update_marketplace_tags_filter(selenium, browser_id, yaml.dump(data["tags"]))

    assert_marketplace_refresh_button_is_enabled(selenium, browser_id)


@wt(parsers.parse("user of {browser_id} sets space configuration as follows:\n{config}"))
def configure_space_manually(browser_id: str, config: str, selenium: SeleniumDrivers) -> None:
    """Adjust space configuration according to given config.

    Config format given in yaml is as follows:
        space name: space_name
        organization name: organization_name
        tags:                           ---> optional
          general:
            - general-tags
          domains:
            - domain-tags
        description: description


    Example configuration:
        space name: "space1"
        organization name: "onedata"
        tags:                           ---> optional
          general:
            - EU-funded
            - big-data
            - open-science
          domains:
            - science
        description: "space advertised in marketplace"
    """
    _configure_space_manually(browser_id, config, selenium)


@wt(
    parsers.parse(
        "user of {browser_id} provides space configuration without saving as follows:\n{config}"
    )
)
def configure_space_manually_without_saving(
    browser_id: str, config: str, selenium: SeleniumDrivers
) -> None:
    """Adjust space configuration according to given config.

    Config format given in yaml is as in the previous function:
    """
    _configure_space_manually(browser_id, config, selenium, with_save=False)


def _configure_space_manually(
    browser_id: str,
    config: str,
    selenium: SeleniumDrivers,
    with_save: bool = True,
) -> None:
    data = yaml.load(config, yaml.Loader)

    space_name_option = "space name"
    organization_name_option = "organization name"

    space_name = data[space_name_option]
    organization_name = data[organization_name_option]
    tags = data.get("tags", None)
    description = data["description"]

    set_space_data_in_configuration_tab(
        selenium,
        browser_id,
        space_name_option,
        space_name,
        with_save=with_save,
    )
    set_space_data_in_configuration_tab(
        selenium,
        browser_id,
        organization_name_option,
        organization_name,
        with_save=with_save,
    )

    if tags:
        add_tags_in_space_configuration_tab(selenium, browser_id, tags, with_save=with_save)

    set_description_of_a_space(selenium, browser_id, description, with_save=with_save)


@wt(
    parsers.parse(
        'user of {browser_id} sees "{space_name}" space in Space Marketplace '
        "subpage with following details:\n{config}"
    )
)
def assert_space_details_in_marketplace(
    selenium: SeleniumDrivers,
    browser_id: str,
    space_name: str,
    config: str,
) -> None:
    """Assert selected details of a space advertised in the marketplace.

    Config format given in yaml is as follows:
    access state: "membership granted" or "request access"  ---> optional
    tags:                               ---> optional
      - tag
    organization name: organization_name                       ---> optional
    creation time: date (DD-Mon-YYYY) or "current"             ---> optional
    providers:                                                  ---> optional
      - provider_name
    description: description                                    ---> optional

    Example configuration:
    access state: membership granted
    tags:
      - archival
      - big-data
      - science
    organization name: "onedata"
    creation time: "05 Mar 2023" or "current"
    providers:
      - dev-oneprovider-krakow
    description: "Example of a space advertised in a Marketplace"

    """
    data = yaml.load(config, yaml.Loader)

    access_state = data.get("access state")
    if access_state == "membership granted":
        assert_element_in_space_marketplace(
            selenium,
            browser_id,
            space_name,
            "access_info",
            "Membership granted",
        )
    elif access_state == "request access":
        assert_space_with_request_access_in_marketplace_subpage(
            selenium,
            browser_id,
            space_name,
        )
    elif access_state is not None:
        raise ValueError(f"Unsupported marketplace access state: {access_state}")

    for option in ("organization name", "description"):
        if option in data:
            assert_element_in_space_marketplace(
                selenium,
                browser_id,
                space_name,
                option,
                data[option],
            )

    if "creation time" in data:
        assert_creation_time_in_space_marketplace(
            selenium,
            browser_id,
            space_name,
            data["creation time"],
        )

    for option, element_type in (("tags", "tag"), ("providers", "provider")):
        if option in data:
            assert_elements_list_in_space_marketplace(
                selenium,
                browser_id,
                space_name,
                element_type,
                data[option],
            )
