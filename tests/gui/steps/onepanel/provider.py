"""This module contains gherkin steps to run acceptance tests featuring
provider management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import cast

from selenium.common.exceptions import NoSuchElementException

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils import Modals, Onepanel, Popups
from tests.gui.utils.generic import transform
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def get_provider_name_from_provider_panel(
    selenium: SeleniumDrivers, browser_id: str
) -> str:
    return Onepanel(selenium[browser_id]).content.provider.details.provider_name


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that (?P<attribute>ID|"
        r"Provider name|Subdomain|Domain|URLs|Latitude|Longitude) "
        r'attribute is equal to "(?P<val>.*?)" in Provider panel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_value_of_provider_attribute(
    selenium: SeleniumDrivers, browser_id: str, attribute: str, val: str
) -> None:
    details = Onepanel(selenium[browser_id]).content.provider.details
    displayed_val = getattr(details, transform(attribute))
    assert (
        displayed_val == val
    ), f"displayed {displayed_val} instead of expected {val} as provider's {attribute}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that "
        r"(?P<attribute>Provider name|Domain) attribute is "
        r'equal to the (?P<property_name>name|hostname) of "(?P<host>.*?)" '
        r"provider in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_value_of_provider_attribute_is_known(
    selenium: SeleniumDrivers,
    browser_id: str,
    attribute: str,
    property_name: str,
    host: str,
    hosts: Hosts,
) -> None:
    expected_val = cast(dict[str, str], hosts[host])[property_name]
    details = Onepanel(selenium[browser_id]).content.provider.details
    displayed_val = getattr(details, transform(attribute))
    assert displayed_val == expected_val, (
        f"displayed {displayed_val} instead of expected {expected_val} as"
        f" provider's {attribute}"
    )


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) types "(?P<val>.*?)" to '
        r"(?P<attribute>Provider name|Subdomain|Domain|Latitude|Longitude) "
        r"input box in modify provider details form in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_val_to_in_box_in_provider_details_form(
    selenium: SeleniumDrivers, browser_id: str, val: str, attribute: str
) -> None:
    form = Onepanel(selenium[browser_id]).content.provider.form
    setattr(form, transform(attribute), val)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) checks "Request a subdomain" '
        r"toggle in modify provider details form in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_check_request_subdomain_toggle_in_provider_details_form(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    form = Onepanel(selenium[browser_id]).content.provider.form
    form.subdomain_delegation.check()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) types (?P<host_property>name|"
        r'hostname) of "(?P<host>.*?)" provider to '
        r"(?P<attribute>Provider name|Subdomain|Domain) input box in modify provider"
        r" details form in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_host_domain_to_in_box_in_provider_details_form(
    selenium: SeleniumDrivers,
    browser_id: str,
    host_property: str,
    host: str,
    attribute: str,
    hosts: Hosts,
) -> None:
    form = Onepanel(selenium[browser_id]).content.provider.form
    setattr(
        form,
        transform(attribute),
        cast(dict[str, str], hosts[host])[host_property],
    )


@wt(
    parsers.parse(
        "user of {browser_id} clicks Discard button on modal in Provider panel"
    )
)
def click_discard_button_on_modal_in_provider_panel(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    Onepanel(driver).discard_button()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on Discard button in the configure web cert modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_discard_btn_in_domain_change_modal(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    try:
        modal = Modals(selenium[browser_id]).configure_web_cert
    except NoSuchElementException:
        return
    modal.discard()


@wt(parsers.parse("user of {browser_id} activates Request a subdomain toggle"))
def activate_request_subdomain_toggle(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    (
        Onepanel(
            selenium[browser_id]
        ).content.deployment.step2.subdomain_delegation.check()
    )


@wt(parsers.parse("user of {browser_id} deactivates Request a subdomain toggle"))
def deactivate_request_subdomain_toggle(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    (
        Onepanel(
            selenium[browser_id]
        ).content.deployment.step2.subdomain_delegation.uncheck()
    )


matcher_wt_enter_test_domain_in_deployment_step2 = parsers.re(
    r"user of (?P<browser_id>.+?) types test hostname of "
    r'"(?P<provider>.+?)" to Domain input box in modify provider '
    r"details form in Provider panel"
)


@wt(matcher_wt_enter_test_domain_in_deployment_step2)
def wt_enter_test_domain_in_deployment_step2(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    Onepanel(selenium[browser_id]).content.provider.form.domain = (
        f"{hosts[provider][r'hostname']}.test"
    )


matcher_wt_assert_value_of_provider_domain = parsers.re(
    r"user of (?P<browser_id>.+?) sees that Domain attribute "
    r'is equal to test hostname of "(?P<provider>.+?)" in Provider panel'
)


@wt(matcher_wt_assert_value_of_provider_domain)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_value_of_provider_domain(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    displayed_val = Onepanel(selenium[browser_id]).content.provider.details.domain
    expected_val = f"{hosts[provider][r'hostname']}.test"
    assert displayed_val == expected_val, (
        f"displayed {displayed_val} instead of expected {expected_val} as"
        " provider's domain"
    )


@wt(
    parsers.parse(
        "user of {browser_id} clicks go to emergency interface "
        "in provider deregistration popups"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_emergency_interface(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    Popups(driver).deregister_provider.buttons["Go to emergency interface"].click()
