"""Catalog of commands exercised by the demo-mode test suite."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from pathlib import Path
from shlex import quote

from tests.demo_mode.utils.commands.command import Command
from tests.demo_mode.utils.commands.command_template import CommandTemplate

_FOREGROUND_ONEZONE = CommandTemplate("run_in_foreground/run_onezone.sh")
_FOREGROUND_ONEPROVIDER = CommandTemplate("run_in_foreground/run_oneprovider.sh")
_BACKGROUND_ONEZONE = CommandTemplate("run_in_background/run_onezone.sh")
_BACKGROUND_ONEPROVIDER = CommandTemplate("run_in_background/run_oneprovider.sh")
_AWAIT_ONEZONE = CommandTemplate("run_in_background/await_onezone.sh")
_AWAIT_ONEPROVIDER = CommandTemplate("run_in_background/await_oneprovider.sh")
_PERSISTENT_ONEZONE = CommandTemplate("persistency/run_onezone.sh")
_PERSISTENT_ONEPROVIDER = CommandTemplate("persistency/run_oneprovider.sh")
_ACCESS_TOKEN = CommandTemplate("access_token/get_access_token.sh")
_COMPREHENSIVE_EXAMPLE = CommandTemplate("comprehensive_example/example.sh")
_PYTHON_SETUP = CommandTemplate("python_access/setup_environment.sh")
_PYTHON_ACCESS = CommandTemplate("python_access/check_python_access.py")


class DemoCommands:
    """Catalog of all commands exercised by the demo-mode suite."""

    def foreground_onezone(self) -> Command:
        return _FOREGROUND_ONEZONE.bind()

    def foreground_oneprovider(self, container: str) -> Command:
        return _FOREGROUND_ONEPROVIDER.bind(container=container)

    def background_onezone(self) -> Command:
        return _BACKGROUND_ONEZONE.bind()

    def background_oneprovider(self, container: str) -> Command:
        return _BACKGROUND_ONEPROVIDER.bind(container=container)

    def await_onezone(self) -> Command:
        return _AWAIT_ONEZONE.bind()

    def await_oneprovider(self, container: str) -> Command:
        return _AWAIT_ONEPROVIDER.bind(container=container)

    def persistent_onezone(self) -> Command:
        return _PERSISTENT_ONEZONE.bind()

    def persistent_oneprovider(self, container: str) -> Command:
        return _PERSISTENT_ONEPROVIDER.bind(container=container)

    def access_token(self, container: str) -> Command:
        return _ACCESS_TOKEN.bind(container=container)

    def comprehensive_example(self) -> Command:
        return _COMPREHENSIVE_EXAMPLE.bind()

    def python_access(
        self,
        *,
        environment_root: Path,
        setup_log_path: Path,
    ) -> Command:
        setup_script = quote(str(_PYTHON_SETUP.path))
        setup_log = quote(str(setup_log_path))
        access_script = quote(str(_PYTHON_ACCESS.path))
        command = "\n".join(
            (
                "set -e",
                f"source {setup_script} > {setup_log} 2>&1",
                f"python3 {access_script}",
            )
        )
        return Command(command, "python-access", environment_root)
