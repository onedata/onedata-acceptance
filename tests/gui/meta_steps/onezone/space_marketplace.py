"""This module contains meta steps for operations on Space Marketplaces
in Onezone using web GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from tests.gui.steps.onezone.marketplace import \
    assert_organization_name_in_space_marketplace, \
    assert_description_in_space_marketplace, \
    assert_creation_time_in_space_marketplace, \
    assert_tags_in_space_marketplace, assert_support_in_space_marketplace
from tests.gui.steps.onezone.space_configuration import \
    set_space_data_in_configuration_tab, \
    set_description_of_a_space, \
    add_tags_in_space_configuration_tab
from tests.utils.bdd_utils import wt, parsers


@wt(parsers.parse('user of {browser_id} sets space configuration '
                  'as follows:\n{config}'))
def configure_space_manually(browser_id, config, selenium, oz_page, popups):
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
    _configure_space_manually(browser_id, config, selenium, oz_page, popups)


def _configure_space_manually(browser_id, config, selenium, oz_page, popups):
    data = yaml.load(config)
    space_name = data['space name']
    organization_name = data['organization name']
    tags = data.get('tags', False)
    description = data['description']

    set_space_data_in_configuration_tab(selenium, browser_id, oz_page,
                                        'space_name', space_name)
    set_space_data_in_configuration_tab(selenium, browser_id, oz_page,
                                        'organization_name', organization_name)
    set_description_of_a_space(selenium, browser_id, oz_page, description)

    if tags:
        if tags['general']:
            add_tags_in_space_configuration_tab(selenium, browser_id, oz_page,
                                                popups, 'general',
                                                tags['general'])
        if tags['domains']:
            add_tags_in_space_configuration_tab(selenium, browser_id, oz_page,
                                                popups, 'domains',
                                                tags['domains'])


@wt(parsers.parse('user of {browser_id} sees advertised space '
                  'on Space Marketplace '
                  'subpage with following parameters:\n{config}'))
def assert_space_in_marketplace_with_config(browser_id, selenium, oz_page,
                                            config):
    """Assert space advertised in marketplace according to given config.

        Config format given in yaml is as follows:
        space name: space_name
        tags:                               ---> optional
          - tag
        organization name: organization_name
        creation time: date                (DD-Mon-YYYY)
        providers:
          - provider_name
        description: description

        Example configuration:
        space name: "space1"
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

    _assert_space_in_marketplace_with_config(browser_id, config, selenium,
                                             oz_page)


def _assert_space_in_marketplace_with_config(browser_id, config, selenium,
                                             oz_page):
    data = yaml.load(config)
    space_name = data['space name']

    organization_name = data['organization name']
    creation_time = data['creation time']
    tags = data.get('tags', False)
    providers = data.get('providers', False)
    description = data['description']

    assert_organization_name_in_space_marketplace(selenium, browser_id, oz_page,
                                                  space_name, organization_name)

    if tags:
        assert_tags_in_space_marketplace(selenium, browser_id, oz_page,
                                         space_name, tags)

    assert_creation_time_in_space_marketplace(selenium, browser_id, oz_page,
                                              space_name, creation_time)
    if providers:
        assert_support_in_space_marketplace(selenium, browser_id, oz_page,
                                            space_name, providers)

    assert_description_in_space_marketplace(selenium, browser_id, oz_page,
                                            space_name, description)
