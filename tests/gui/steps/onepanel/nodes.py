"""This module contains gherkin steps to run acceptance tests featuring
nodes management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import re

from tests.gui.constants import WAIT_FRONTEND
from tests.gui.utils import Onepanel
from tests.gui.utils.generic import parse_elements_sequence, transform
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} sees that {options:ElementsSequence} options are "
        "enabled for {host_pattern} host in Nodes page in Onepanel",
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_options_enabled_for_host_in_nodes(
    selenium: SeleniumDrivers,
    browser_id: str,
    options: list[str],
    host_pattern: str,
) -> None:
    option_names = [transform(option) for option in options]
    error_message = f"{{}} not enabled for {host_pattern} in Nodes page in Onepanel"
    for host in Onepanel(selenium[browser_id]).content.nodes.hosts:
        if re.match(host_pattern, host.name):
            for option in option_names:
                toggle = getattr(host, option)
                assert toggle.is_checked(), error_message.format(option)


@wt(
    parsers.parse(
        "user of {browser_id} sees that {options:ElementsSequence} options cannot "
        "be changed for {host_pattern} host in Nodes page in Onepanel",
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_options_cannot_be_changed_for_host_in_nodes(
    selenium: SeleniumDrivers,
    browser_id: str,
    options: list[str],
    host_pattern: str,
) -> None:
    option_names = [transform(option) for option in options]
    error_message = (
        f"{{}} can be changed for {host_pattern} in Nodes page in Onepanel, "
        "while it should not be"
    )
    for host in Onepanel(selenium[browser_id]).content.nodes.hosts:
        if re.match(host_pattern, host.name):
            for option in option_names:
                toggle = getattr(host, option)
                assert not toggle.is_enabled(), error_message.format(option)
