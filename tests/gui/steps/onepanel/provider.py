"""This module contains gherkin steps to run acceptance tests featuring
provider management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from typing import Any, cast

from tests.conftest import Hosts, SeleniumDrivers
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils import Modals, Onepanel, Popups
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) sees that (?P<attr>ID|"
        "Provider name|Subdomain|Domain|URLs|Latitude|Longitude) "
        'attribute is equal to "(?P<val>.*?)" '
        "in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_value_of_provider_attribute(
    selenium: SeleniumDrivers, browser_id: Any, attr: Any, val: Any
) -> Any:
    details = Onepanel(selenium[browser_id]).content.provider.details
    displayed_val = getattr(details, transform(attr))
    assert (
        displayed_val == val
    ), f"displayed {displayed_val} instead of expected {val} as provider's {attr}"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) sees that "
        "(?P<attr>Provider name|Domain) attribute is "
        'equal to the (?P<prop>name|hostname) of "(?P<host>.*?)" '
        "provider in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_value_of_provider_attribute_is_known(
    selenium: SeleniumDrivers,
    browser_id: Any,
    attr: Any,
    prop: Any,
    host: Any,
    hosts: Hosts,
) -> Any:
    expected_val = cast(str, cast(dict[str, str], hosts[host])[prop])
    details = Onepanel(selenium[browser_id]).content.provider.details
    displayed_val = getattr(details, transform(attr))
    assert displayed_val == expected_val, (
        f"displayed {displayed_val} instead of expected {expected_val} as"
        f" provider's {attr}"
    )


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) types "(?P<val>.*?)" to '
        "(?P<attr>Provider name|Subdomain|Domain|Latitude|Longitude) "
        "input box in modify provider details form in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_val_to_in_box_in_provider_details_form(
    selenium: SeleniumDrivers, browser_id: Any, val: Any, attr: Any
) -> Any:
    form = Onepanel(selenium[browser_id]).content.provider.form
    setattr(form, transform(attr), val)


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) checks "Request a subdomain" '
        "toggle in modify provider details form in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_check_request_subdomain_toggle_in_provider_details_form(
    selenium: SeleniumDrivers, browser_id: Any
) -> Any:
    form = Onepanel(selenium[browser_id]).content.provider.form
    form.subdomain_delegation.check()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) types (?P<host_property>name|"
        'hostname) of "(?P<host>.*?)" provider to '
        "(?P<attr>Provider name|Subdomain|Domain) input box in modify provider"
        " details form in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_host_domain_to_in_box_in_provider_details_form(
    selenium: SeleniumDrivers,
    browser_id: Any,
    host_property: Any,
    host: Any,
    attr: Any,
    hosts: Hosts,
) -> Any:
    form = Onepanel(selenium[browser_id]).content.provider.form
    setattr(
        form,
        transform(attr),
        cast(str, cast(dict[str, str], hosts[host])[host_property]),
    )


@wt(
    parsers.parse(
        "user of {browser_id} saves changes in provider details form in Provider panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_save_changes_in_modify_provider_detail_form(
    selenium: SeleniumDrivers, browser_id: Any
) -> Any:
    driver = selenium[browser_id]
    Onepanel(driver).content.provider.form.save()


@wt(
    parsers.parse(
        "user of {browser_id} clicks Discard button on modal in Provider panel"
    )
)
def click_discard_button_on_modal_in_provider_panel(
    selenium: SeleniumDrivers, browser_id: Any
) -> Any:
    driver = selenium[browser_id]
    Onepanel(driver).discard_button()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on Discard button in the configure web cert modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_discard_btn_in_domain_change_modal(
    selenium: SeleniumDrivers, browser_id: Any
) -> Any:
    try:
        Modals(selenium[browser_id]).configure_web_cert.discard()
    except RuntimeError as e:
        if re.match(r"no.*item found in modals", str(e)):
            pass
        else:
            raise


@wt(parsers.parse("user of {browser_id} activates Request a subdomain toggle"))
def activate_request_subdomain_toggle(
    selenium: SeleniumDrivers, browser_id: Any
) -> Any:
    (
        Onepanel(
            selenium[browser_id]
        ).content.deployment.step2.subdomain_delegation.check()
    )


@wt(parsers.parse("user of {browser_id} deactivates Request a subdomain toggle"))
def deactivate_request_subdomain_toggle(
    selenium: SeleniumDrivers, browser_id: Any
) -> Any:
    (
        Onepanel(
            selenium[browser_id]
        ).content.deployment.step2.subdomain_delegation.uncheck()
    )


matcher_wt_enter_test_domain_in_deployment_step2 = parsers.re(
    "user of (?P<browser_id>.+?) types test hostname of "
    '"(?P<provider>.+?)" to Domain input box in modify provider '
    "details form in Provider panel"
)


@wt(matcher_wt_enter_test_domain_in_deployment_step2)
def wt_enter_test_domain_in_deployment_step2(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, hosts: Hosts
) -> Any:
    Onepanel(selenium[browser_id]).content.provider.form.domain = (
        f"{hosts[provider]['hostname']}.test"
    )


matcher_wt_assert_value_of_provider_domain = parsers.re(
    "user of (?P<browser_id>.+?) sees that Domain attribute "
    'is equal to test hostname of "(?P<provider>.+?)" in '
    "Provider panel"
)


@wt(matcher_wt_assert_value_of_provider_domain)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_value_of_provider_domain(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, hosts: Hosts
) -> Any:
    displayed_val = Onepanel(selenium[browser_id]).content.provider.details.domain
    expected_val = f"{hosts[provider]['hostname']}.test"
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
def go_to_emergency_interface(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    driver = selenium[browser_id]
    Popups(driver).deregister_provider.buttons["Go to emergency interface"].click()
