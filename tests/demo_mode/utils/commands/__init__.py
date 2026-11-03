"""Registry and execution interfaces for demo-mode guide commands."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.demo_mode.utils.commands.command_template import CommandTemplate

RUN_ONEZONE_FOREGROUND = CommandTemplate("run_in_foreground/run_onezone.sh")
RUN_ONEPROVIDER_FOREGROUND = CommandTemplate("run_in_foreground/run_oneprovider.sh")
RUN_ONEZONE_BACKGROUND = CommandTemplate("run_in_background/run_onezone.sh")
RUN_ONEPROVIDER_BACKGROUND = CommandTemplate("run_in_background/run_oneprovider.sh")
AWAIT_ONEZONE = CommandTemplate("run_in_background/await_onezone.sh")
AWAIT_ONEPROVIDER = CommandTemplate("run_in_background/await_oneprovider.sh")
GET_ACCESS_TOKEN = CommandTemplate("access_token/get_access_token.sh")
RUN_ONEZONE_PERSISTENT = CommandTemplate("persistency/run_onezone.sh")
RUN_ONEPROVIDER_PERSISTENT = CommandTemplate("persistency/run_oneprovider.sh")
RUN_COMPREHENSIVE_EXAMPLE = CommandTemplate("comprehensive_example/example.sh")
