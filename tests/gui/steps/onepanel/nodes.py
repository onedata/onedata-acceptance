"""This module contains gherkin steps to run acceptance tests featuring
nodes management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


import re

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} sees that {options} options are "
        "enabled for {host_regexp} host in Nodes page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_options_enabled_for_host_in_nodes(
    selenium, browser_id, options, host_regexp, onepanel
):
    options = [transform(option) for option in parse_seq(options)]
    err_msg = f"{{}} not enabled for {host_regexp} in Nodes page in Onepanel"
    for host in onepanel(selenium[browser_id]).content.nodes.hosts:
        if re.match(host_regexp, host.name):
            for option in options:
                toggle = getattr(host, option)
                assert toggle.is_checked(), err_msg.format(option)


@wt(
    parsers.parse(
        "user of {browser_id} sees that {options} options cannot "
        "be changed for {host_regexp} host in Nodes page "
        "in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_options_cannot_be_changed_for_host_in_nodes(
    selenium, browser_id, options, host_regexp, onepanel
):
    options = [transform(option) for option in parse_seq(options)]
    err_msg = (
        f"{{}} can be changed for {host_regexp} in Nodes page in Onepanel, "
        "while it should not be"
    )
    for host in onepanel(selenium[browser_id]).content.nodes.hosts:
        if re.match(host_regexp, host.name):
            for option in options:
                toggle = getattr(host, option)
                assert not toggle.is_enabled(), err_msg.format(option)
