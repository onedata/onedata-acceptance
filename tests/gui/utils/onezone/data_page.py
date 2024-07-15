"""Utils to facilitate operations on discovery page in Onezone gui"""

__author__ = "Michal Stanisz, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import re

from selenium.webdriver import ActionChains
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               WebItemsSequence, Label,
                                               WebItem, WebElement,
                                               WebElementsSequence, Icon, Input)
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from .common import EditBox, InputBox
from .members_subpage import MembersPage
from .space_configuration_subpage import SpaceConfigurationPage
from .space_marketplace import SpaceMarketplacePage


class Space(Element):
    name = id = Label('.one-label')
    support_size = Label('.status-toolbar-icon:first-of-type')
    supporting_providers_number = Label('.status-toolbar-icon:last-of-type')
    advertised_icon = Icon('.oneicon-cart-checked')
    home_icon = WebElement('.status-toolbar-icon:first-of-type span')

    overview = NamedButton('.one-list-level-2 .item-header',
                           text='Overview')
    files = NamedButton('.one-list-level-2 .item-header',
                        text='Files')
    shares_open_data = NamedButton('.one-list-level-2 .item-header',
                                   text='Shares, Open Data')
    transfers = NamedButton('.one-list-level-2 .item-header',
                            text='Transfers')
    datasets_archives = NamedButton('.one-list-level-2 .item-header',
                                    text='Datasets, Archives')
    providers = NamedButton('.one-list-level-2 .item-header',
                            text='Providers')
    members = NamedButton('.one-list-level-2 .item-header',
                          text='Members')
    harvesters_discovery = NamedButton('.one-list-level-2 .item-header',
                                       text='Harvesters, Discovery')
    automation_workflows = NamedButton('.one-list-level-2 .item-header',
                                       text='Automation Workflows')
    configuration = NamedButton('.one-list-level-2 .item-header',
                                text='Configuration')
    menu_button = Button('.collapsible-toolbar-toggle')



    def click_menu(self):
        self.click()
        self.menu_button.click()

    def is_element_disabled(self, element_name):
        element = getattr(self, element_name)
        return 'disabled' in element.web_elem.get_attribute("class")

    def is_element_enabled(self, element_name):
        element = getattr(self, element_name)
        return 'disabled' not in element.web_elem.get_attribute("class")

    def is_active(self):
        return 'active' in self.web_elem.get_attribute('class')


class Provider(Element):
    id = name = Label('.one-label')
    support = Label('.outer-text')
    menu_button = Button('.provider-menu-toggle')
    information_button = Button('.oneicon-provider')


class SpaceInfoTile(PageObject):
    rename = Button('.edit-icon')
    edit_name_box = WebItem('.editor', cls=EditBox)
    shares_count = Label('.shares-count')


class SpaceMembersTile(PageObject):
    direct_groups = Label('.direct-groups-counter')
    direct_users = Label('.direct-users-counter')
    effective_groups = Label('.effective-groups-counter')
    effective_users = Label('.effective-users-counter')


class SpaceDetailsTile(PageObject):
    organization_name = Label('.organization-name')
    description = Label('.description-row')
    tags = WebElementsSequence('.tag-item')


class SpaceMarketplaceTile(PageObject):
    advertise_info = Label('.figure-bottom-text')
    configure_advertisement = Button('.tile-footer-link')
    show = Button('.more-link')


class ProvidersMap(Element):
    providers = WebElementsSequence('.one-atlas-point')

    def click_provider(self, provider_name, driver):
        for prov in self.providers:
            ActionChains(driver).move_to_element(prov).perform()
            name = driver.find_element_by_css_selector('.tooltip-inner').text
            if name == provider_name:
                prov.click()
                return

        raise RuntimeError(f'Provider {provider_name} was not found on the map')

    def hover_and_check_provider(self, provider_name, driver):
        for prov in self.providers:
            ActionChains(driver).move_to_element(prov).perform()
            name = driver.find_element_by_css_selector('.tooltip-inner').text
            if name == provider_name:
                return

        raise RuntimeError(f'Provider {provider_name} was not found on the map')

    def get_provider_horizontal_position(self, provider_name, driver):
        for prov in self.providers:
            ActionChains(driver).move_to_element(prov).perform()
            name = driver.find_element_by_css_selector('.tooltip-inner').text
            if name == provider_name:
                style = prov.get_attribute('style')
                position = re.search(r'left:\s*(\d+\.*\d*)px', style).group(1)
                position = float(position)

                return position

        raise RuntimeError(f'Provider {provider_name} was not found on the map')


class SpaceOverviewPage(PageObject):
    space_name = Label('.header-row .one-label')
    info_tile = WebItem('.resource-info-tile', cls=SpaceInfoTile)
    members_tile = WebItem('.resource-members-tile .tile-main',
                           cls=SpaceMembersTile)
    map = WebItem('.map-container', cls=ProvidersMap)
    space_details_tile = WebItem('.space-details-tile', cls=SpaceDetailsTile)
    marketplace_tile = WebItem('.space-marketplace-tile',
                               cls=SpaceMarketplaceTile)


class WelcomePage(PageObject):
    create_a_space = NamedButton('.info .ember-view', text='Create a space')
    join_an_existing_space = NamedButton('.info .ember-view',
                                         text='join an existing space')
    join_group = NamedButton('.info .ember-view', text='join a group')


class HarvesterRow(Element):
    name = id = Label('.item-name')
    harvester = WebElement('.item-name')
    harvester_menu_button = WebElement('.collapsible-toolbar-toggle')

    def click_harvester_menu_button(self, driver):
        ActionChains(driver).move_to_element(self.harvester).perform()
        self.harvester_menu_button.click()


class HarvestersPage(PageObject):
    harvesters_list = WebItemsSequence(
        '.main-content .one-collapsible-list-item', cls=HarvesterRow)
    add_one_of_harvesters = NamedButton(
        '.add-harvester-to-space-trigger.btn',
        text='Add one of your harvesters')
    invite_harvester_using_token = NamedButton(
        '.generate-invite-token-action.btn',
        text='Invite harvester using token')


class GetSupportPage(PageObject):
    request_support_modal = NamedButton('.nav-link', text='Request support')
    deploy_provider_modal = NamedButton('.nav-link',
                                        text='Deploy your own Oneprovider')
    expose_existing_data_modal = NamedButton('.nav-link',
                                             text='Expose existing data set')

    token_textarea = Label('.active textarea')
    copy = Button('.request-support-tab .copy-btn')
    forbidden_alert = WebElement('.error')
    insufficient_privileges = Label('.text-center .col-xs-12')


class SpaceProvidersPage(PageObject):
    providers_list = WebItemsSequence('.space-providers-list '
                                      'li.one-collapsible-list-item',
                                      cls=Provider)
    add_support = Button('.btn-add-support')
    get_support_page = WebItem('.ember-view', cls=GetSupportPage)
    map = WebItem('.space-providers-atlas', cls=ProvidersMap)


class _Provider(PageObject):
    name = id = Label('.record-name-general')


class DatasetHeader(PageObject):
    detached = Button('.btn-effecitve')
    attached = Button('.select-attached-datasets-btn')


class ArchiveHeader(PageObject):
    back_to_dataset_page = Button('.content-back-arrow-icon')


class DataPage(GenericPage):
    create_space_button = Button('.one-sidebar-toolbar-button '
                                 '.oneicon-add-filled')

    marketplace_button = Button('.one-sidebar-toolbar-button '
                                '.oneicon-cart')

    spaces_header_list = WebItemsSequence('.sidebar-spaces '
                                          'li.one-list-item.clickable '
                                          '.item-header', cls=Space)

    elements_list = WebItemsSequence('.sidebar-spaces '
                                     'li.one-list-item.clickable.resource-item',
                                     cls=Space)

    input_box = WebItem('.content-info-content-container', cls=InputBox)

    input_rename = Input('.name-editor .form-control')

    save_button = Button('.save-icon')

    overview_page = WebItem('.main-content', cls=SpaceOverviewPage)
    providers_page = WebItem('.main-content', cls=SpaceProvidersPage)
    members_page = WebItem('.main-content', cls=MembersPage)
    welcome_page = WebItem('.main-content', cls=WelcomePage)
    harvesters_page = WebItem('.main-content', cls=HarvestersPage)
    dataset_header = WebItem('.main-content', cls=DatasetHeader)
    configuration_page = WebItem('.main-content', cls=SpaceConfigurationPage)
    space_marketplace_page = WebItem('.main-content', cls=SpaceMarketplacePage)

    # button in top right corner on all subpages
    menu_button = Button('.with-menu .collapsible-toolbar-toggle')

    get_started = Button('.btn.btn-default.hide-sm-active.ember-view')

    tab_name = Label('.header-row')

    current_provider = Label('.current-oneprovider-bar .record-name-general')
    providers = WebItemsSequence('.provider-online', cls=_Provider)
    choose_other_provider = Button('.choose-oneprovider-link')
    error_header = Label('.content-info-content-container h1')

    def choose_space(self, name):
        for space in self.elements_list:
            if space.name == name or space.name == '':
                space.click()
                if space.name == name:
                    return
        else:
            raise RuntimeError(f'{name} space not found')
