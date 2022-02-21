"""Utils for operations on token caveats in GUI tests
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time
from datetime import datetime, timedelta

from selenium.webdriver.common.keys import Keys

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Label, WebElement, Button, WebItemsSequence, Input)


class CaveatTag(PageObject):
    name = id = Label('.tag-label')
    icon = WebElement('.tag-icon')

    def is_icon_type(self, i_type):
        if i_type == 'oneprovider':
            i_type = 'provider'
        return i_type in self.icon.get_attribute('class')


class PathEntry(PageObject):
    space_name = id = Label('.pathSpace-field')
    path = Label('.pathString-field')


class ObjectIdEntry(PageObject):
    name = id = Label('.text-like-field')


class CaveatField(PageObject):
    name = id = Label('.control-label')
    toggle = Toggle('.one-way-toggle')

    new_item = Button('.oneicon-plus')
    add_item = Button('.add-field-button')

    item_label = Label('.dropdown-field')
    expander = Button('.ember-power-select-trigger')
    time_input = Input('.form-control.date-time-picker')
    time_label = Label('.datetime-field')
    inner_input = Input('.tag-creator .text-editor-input')
    input = Input('.text-like-field .form-control')

    rest_control = Button('.option-rest .one-way-radio-control')
    oneclient_control = Button('.option-oneclient .one-way-radio-control')

    tags = WebItemsSequence('.tag-item', cls=CaveatTag)
    interface_label = Label('.radio-field')
    readonly_toggle = Toggle('.readonlyView-field .one-way-toggle')
    path_entries = WebItemsSequence('.pathEntry-collapse', cls=PathEntry)
    object_id_entries = WebItemsSequence('.objectIdEntry-field',
                                         cls=ObjectIdEntry)

    def activate(self):
        self.toggle.check()

    def deactivate(self):
        self.toggle.uncheck()

    def is_allow(self):
        return self.item_label == 'Allow'

    def set_allow(self, popups, selenium, browser_id):
        if not self.is_allow():
            self.expander()
            popups(selenium[browser_id]).power_select.choose_item('Allow')

    def set_deny(self, popups, selenium, browser_id):
        if self.is_allow():
            self.expander()
            popups(selenium[browser_id]).power_select.choose_item('Deny')

    def set_allowance(self, allow, popups, selenium, browser_id):
        if allow:
            self.set_allow(popups, selenium, browser_id)
        else:
            self.set_deny(popups, selenium, browser_id)

    def assert_allowance(self, allow):
        if allow:
            assert self.is_allow(), 'Caveat type should be Allow but is Deny'
        else:
            assert not self.is_allow(), ('Caveat type should be Deny but is '
                                         'Allow')

    def assert_num_caveats_equal(self, exp_items):
        msg = (f'Number of expected items {exp_items} does not equal actual '
               f'number of items {[tag.name for tag in self.tags]}')
        assert len(exp_items) == len(self.tags), msg

    # setters

    def set_item_in_inner_input(self, selenium, browser_id, item):
        self.new_item()
        self.inner_input = item
        driver = selenium[browser_id]
        driver.switch_to.active_element.send_keys(Keys.RETURN)

    # expiration caveat
    def set_expiration_caveat(self, expire_caveat, tmp_memory):
        self.activate()
        min_delta = expire_caveat['after']
        time = self.get_time_after_delta(min_delta)
        self.time_input = time
        tmp_memory['expire_time'] = time

    def get_time_after_delta(self, delta):
        now = datetime.now()
        delta = timedelta(minutes=delta)
        then = now + delta
        return then.strftime("%Y/%m/%d %-H:%M")

    # region caveat
    def set_region_caveats(self, selenium, browser_id, region_caveat, popups):
        self.activate()
        caveat_allow = region_caveat.get('allow', True)
        regions = region_caveat.get('region codes')
        self.set_allowance(caveat_allow, popups, selenium, browser_id)
        for region in regions:
            self.set_region_in_region_caveat(selenium, browser_id, region,
                                             popups)

    def set_region_in_region_caveat(self, selenium, browser_id, region, popups):
        self.new_item()
        driver = selenium[browser_id]
        popups(driver).selector_popup.selectors[region]()

    # country caveat
    def set_country_caveats(self, selenium, browser_id, country_caveat, popups):
        self.activate()
        caveat_allow = country_caveat.get('allow', True)
        countries = country_caveat.get('country codes')
        self.set_allowance(caveat_allow, popups, selenium, browser_id)
        for country in countries:
            self.set_item_in_inner_input(selenium, browser_id, country)

    # asn caveat
    def set_asn_caveats(self, selenium, browser_id, asn_list):
        self.activate()
        for asn in asn_list:
            self.set_item_in_inner_input(selenium, browser_id, str(asn))

    # ip caveat
    def set_ip_caveats(self, selenium, browser_id, ips):
        self.activate()
        for ip in ips:
            self.set_item_in_inner_input(selenium, browser_id, ip)

    # consumer caveat
    def set_consumer_caveats(self, selenium, browser_id, popups,
                             consumer_caveats, users, groups, hosts, oz_page):
        self.activate()
        oz_page(selenium[browser_id])['tokens'].create_token_page.hide_caveats()
        for consumer in consumer_caveats:
            consumer_type = consumer.get('type')
            method = consumer.get('by')
            value = consumer.get('consumer name')
            if method == 'id':
                if consumer_type == 'user':
                    value = users[value].user_id
                elif consumer_type == 'group':
                    value = groups[value]
            if consumer_type == 'oneprovider' and method == 'name' and 'Any' \
                    not in value:
                value = hosts[value]['name']
            self.set_consumer_in_consumer_caveat(selenium, browser_id, popups,
                                                 consumer_type, method, value)
        oz_page(selenium[browser_id])[
            'tokens'].create_token_page.expand_caveats()

    def set_consumer_in_consumer_caveat(self, selenium, browser_id, popups,
                                        consumer_type, method, value):
        self.new_item()
        driver = selenium[browser_id]
        popup = popups(driver).consumer_caveat_popup
        popup.expand_consumer_types()
        time.sleep(0.5)
        popup.select_type(consumer_type)
        if method == 'name':
            popup.list_option()
            popup.consumers[value]()
        else:
            popup.id_option()
            popup.input = value
            popup.add_button()

    # service caveat
    def set_service_caveats(self, selenium, browser_id, service_caveats,
                            popups):
        self.activate()
        service_cav = service_caveats.get('Service', [])
        service_onepanel_cav = service_caveats.get('Service Onepanel', [])
        for service in service_cav:
            self.set_service_in_service_caveat(selenium, browser_id,
                                               popups, 'Service', service)
        for service in service_onepanel_cav:
            self.set_service_in_service_caveat(selenium, browser_id, popups,
                                               'Service Onepanel', service)

    def set_service_in_service_caveat(self, selenium, browser_id, popups,
                                      consumer_type, value):
        self.new_item()
        driver = selenium[browser_id]
        popup = popups(driver).consumer_caveat_popup
        popup.expand_consumer_types()
        popup.consumer_types[consumer_type]()
        popup.list_option()

        # this line is to load elements, test fails without it
        [consumer.name for consumer in popup.consumers]
        time.sleep(0.5)
        popup.consumers[value]()

    # interface caveat
    def set_interface_caveat(self, caveat):
        self.activate()
        getattr(self, f'{caveat.lower()}_control').click()

    # readonly caveat
    def set_readonly_caveat(self):
        self.activate()

    # path caveat
    def set_path_caveats(self, path_caveats):
        self.activate()
        for path_caveat in path_caveats:
            self.set_path_caveat(path_caveat)

    def set_path_caveat(self, path_caveat):
        space = path_caveat['space']
        path = path_caveat['path']
        self.add_item()
        if not self.item_label == space:
            self.expander()
            self.options[space]()
        self.input = path

    # object id caveat
    def set_object_id_caveats(self, ids):
        self.activate()
        for object_id in ids:
            self.set_object_id_caveat(object_id)

    def set_object_id_caveat(self, object_id):
        self.add_item()
        self.input = str(object_id)

    # assertions

    # expiration caveat
    def assert_expiration_caveat(self, exp_caveat, tmp_memory):
        value_set = exp_caveat.get('set', False)
        if value_set:
            expected_time = tmp_memory.get('expire_time', None)
            actual_time = self.time_label
            msg = (f'Expected time {expected_time} does not match actual '
                   f'{actual_time}')
            assert expected_time == actual_time, msg
        else:
            msg = 'Time should not be set but it is'
            assert tmp_memory.get('expire_time', None) is None , msg

    # region caveat
    def assert_region_caveats(self, region_caveat):
        caveat_allow = region_caveat.get('allow', True)
        regions = region_caveat.get('region codes')
        self.assert_allowance(caveat_allow)
        self.assert_num_caveats_equal(regions)
        for region in regions:
            self.assert_region_in_region_caveat(region)

    def assert_region_in_region_caveat(self, region):
        assert region in self.tags, (f'{region} should be amongst region '
                                     f'caveats but is not')

    # country caveat
    def assert_country_caveats(self, country_caveat):
        caveat_allow = country_caveat.get('allow', True)
        countries = country_caveat.get('country codes')
        self.assert_allowance(caveat_allow)
        self.assert_num_caveats_equal(countries)
        for country in countries:
            self.assert_region_in_region_caveat(country)

    def assert_country_in_country_caveat(self, country):
        assert country in self.tags, (f'{country} should be amongst country '
                                      f'caveats but is not')

    # asn caveat
    def assert_asn_caveats(self, asn_list):
        self.assert_num_caveats_equal(asn_list)
        for asn in asn_list:
            self.assert_asn_in_asn_caveats(str(asn))

    def assert_asn_in_asn_caveats(self, asn):
        assert asn in self.tags, (f'{asn} should be amongst asn '
                                  f'caveats but is not')

    # ip caveat
    def assert_ip_caveats(self, ips):
        self.assert_num_caveats_equal(ips)
        for ip in ips:
            self.assert_ip_in_ip_caveats(ip)

    def assert_ip_in_ip_caveats(self, ip):
        assert ip in self.tags, (f'{ip} should be amongst ip '
                                 f'caveats but is not')

    # consumer caveat
    # creation parameter is to check if assertion is done directly after
    # creation - then consumer is checked only by name
    def assert_consumer_caveats(self, consumer_caveats, users, groups, hosts,
                                creation):
        for consumer in consumer_caveats:
            consumer_type = consumer.get('type')
            if creation:
                method = 'name'
            else:
                method = consumer.get('by')
            value = consumer.get('consumer name')
            if method == 'id':
                if consumer_type == 'user':
                    value = users[value].user_id
                elif consumer_type == 'group':
                    value = groups[value]
            if consumer_type == 'oneprovider' and method == 'name' and 'Any' \
                    not in value:
                value = hosts[value]['name']
            self.assert_consumer_in_consumer_caveat(consumer_type, method,
                                                    value)

    def assert_consumer_in_consumer_caveat(self, consumer_type, method,
                                           value):
        if method == 'name':
            tag = self.tags[value]
        else:
            tag = self.tags['ID: ' + value]
        assert tag.is_icon_type(consumer_type), (f'Consumer caveat for {value}'
                                                 f' is not {consumer_type}')

    # service caveat
    def assert_service_caveats(self, services):
        self.assert_num_caveats_equal(services)
        for service in services:
            self.assert_ip_in_ip_caveats(service)

    def assert_service_in_service_caveat(self, service):
        assert service in self.tags, (f'{service} should be amongst services '
                                      f'caveats but is not')

    # interface caveat
    def assert_interface_caveat(self, interface):
        assert self.interface_label == interface

    # readonly caveat
    def assert_readonly_caveat(self):
        assert self.readonly_toggle.is_checked(), 'Readonly not set'

    # path caveat
    def assert_path_caveats(self, paths):
        for path in paths:
            self.assert_path_caveat(path)

    def assert_path_caveat(self, path_caveat):
        space = path_caveat['space']
        path = path_caveat['path']
        entry = self.path_entries[space]
        assert entry.path == path, (f'Invalid path: {space} {path}. Actual: '
                                    f'{entry.space_name} {entry.path}')

    # object id caveat
    def assert_object_id_caveats(self, ids):
        for object_id in ids:
            self.assert_object_id_caveat(object_id)

    def assert_object_id_caveat(self, object_id):
        assert object_id in self.object_id_entries, (f'Object id {object_id} '
                                                     f'not in object ids')

