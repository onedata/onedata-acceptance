"""This module contains gherkin steps to run acceptance tests featuring
provider management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import when, then, parsers

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import repeat_failed, transform


@when(parsers.re('user of (?P<browser_id>.*?) sees that (?P<attr>ID|'
                 'Provider name|Subdomain|Domain|URLs|Latitude|Longitude) '
                 'attribute is equal to "(?P<val>.*?)" '
                 'in Provider panel'))
@then(parsers.re('user of (?P<browser_id>.*?) sees that (?P<attr>ID|'
                 'Provider name|Subdomain|Domain|URLs|Latitude|Longitude) '
                 'attribute is equal to "(?P<val>.*?)" '
                 'in Provider panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_value_of_provider_attribute(selenium, browser_id,
                                          attr, val, onepanel):
    details = onepanel(selenium[browser_id]).content.provider.details
    displayed_val = getattr(details, transform(attr))
    assert displayed_val == val, \
        ('displayed {} instead of expected {} as '
         'provider\'s {}'.format(displayed_val, val, attr))


@when(parsers.re('user of (?P<browser_id>.*?) sees that '
                 '(?P<attr>Provider name|Domain) attribute is equal to the '
                 '(?P<prop>name|hostname) of "(?P<host>.*?)" provider in '
                 'Provider panel'))
@then(parsers.re('user of (?P<browser_id>.*?) sees that '
                 '(?P<attr>Provider name|Domain) attribute is '
                 'equal to the (?P<prop>name|hostname) of "(?P<host>.*?)" '
                 'provider in Provider panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_value_of_provider_attribute_is_known(selenium, browser_id, attr,
                                                   prop, host, hosts, onepanel):
    expected_val = hosts[host][prop]
    details = onepanel(selenium[browser_id]).content.provider.details
    displayed_val = getattr(details, transform(attr))
    assert displayed_val == expected_val, \
        ('displayed {} instead of expected {} '
         'as provider\'s {}'.format(displayed_val, expected_val, attr))


@when(parsers.re('user of (?P<browser_id>.*?) types "(?P<val>.*?)" to '
                 '(?P<attr>Provider name|Subdomain|Domain|Latitude|Longitude) '
                 'input box in modify provider details form in Provider panel'))
@then(parsers.re('user of (?P<browser_id>.*?) types "(?P<val>.*?)" to '
                 '(?P<attr>Provider name|Subdomain|Domain|Latitude|Longitude) '
                 'input box in modify provider details form in Provider panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_val_to_in_box_in_provider_details_form(selenium, browser_id,
                                                   val, attr, onepanel):
    form = onepanel(selenium[browser_id]).content.provider.form
    setattr(form, transform(attr), val)


@when(parsers.re('user of (?P<browser_id>.*?) types (?P<property>name|'
                 'hostname) of "(?P<host>.*?)" provider to '
                 '(?P<attr>Provider name|Domain) input box in modify provider '
                 'details form in Provider panel'))
@then(parsers.re('user of (?P<browser_id>.*?) types (?P<property>name|'
                 'hostname) of "(?P<host>.*?)" provider to '
                 '(?P<attr>Provider name|Domain) input box in modify provider'
                 ' details form in Provider panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_host_domain_to_in_box_in_provider_details_form(selenium, browser_id,
                                                           property, host, attr,
                                                           hosts, onepanel):
    form = onepanel(selenium[browser_id]).content.provider.form
    setattr(form, transform(attr), hosts[host][property])


@when(parsers.parse('user of {browser_id} clicks on Modify provider details '
                    'button in provider details form in Provider panel'))
@then(parsers.parse('user of {browser_id} clicks on Modify provider details '
                    'button in provider details form in Provider panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_modify_provider_detail_form(selenium, browser_id, onepanel):
    onepanel(selenium[browser_id]).content.provider.form.modify_provider_details()


@when(parsers.parse('user of {browser_id} activates Request a subdomain toggle'))
@then(parsers.parse('user of {browser_id} activates Request a subdomain toggle'))
def activate_request_subdomain_toggle(selenium, browser_id, onepanel):
    (onepanel(selenium[browser_id]).content
                                   .deployment
                                   .step2
                                   .subdomain_delegation
                                   .check())


@when(parsers.parse('user of {browser_id} deactivates Request a subdomain toggle'))
@then(parsers.parse('user of {browser_id} deactivates Request a subdomain toggle'))
def deactivate_request_subdomain_toggle(selenium, browser_id, onepanel):
    (onepanel(selenium[browser_id]).content
                                   .deployment
                                   .step2
                                   .subdomain_delegation
                                   .uncheck())


matcher_wt_enter_test_domain_in_deployment_step2 = \
    parsers.re('user of (?P<browser_id>.+?) types test hostname of '
               '"(?P<provider>.+?)" to Domain input box in modify provider '
               'details form in Provider panel')


@when(matcher_wt_enter_test_domain_in_deployment_step2)
@then(matcher_wt_enter_test_domain_in_deployment_step2)
def wt_enter_test_domain_in_deployment_step2(selenium, browser_id, provider,
                                             hosts, onepanel):
    onepanel(selenium[browser_id]).content.provider.form.domain = \
        "{}.test".format(hosts[provider]['hostname'])


matcher_wt_assert_value_of_provider_domain = \
    parsers.re('user of (?P<browser_id>.+?) sees that Domain attribute '
               'is equal to test hostname of "(?P<provider>.+?)" in '
               'Provider panel')


@when(matcher_wt_assert_value_of_provider_domain)
@then(matcher_wt_assert_value_of_provider_domain)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_value_of_provider_domain(selenium, browser_id, provider, hosts,
                                       onepanel):
    displayed_val = onepanel(selenium[browser_id]).content.provider.details.domain
    expected_val = "{}.test".format(hosts[provider]['hostname'])
    assert displayed_val == expected_val, \
        ('displayed {} instead of expected {} as '
         'provider\'s domain'.format(displayed_val, expected_val))
