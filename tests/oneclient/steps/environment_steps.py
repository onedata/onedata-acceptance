"""This module contains tests steps concerning environments operations"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time

from tests.type_definitions import Hosts
from tests.utils.bdd_utils import parsers, wt
from tests.utils.environment_utils import run_kubectl_command, verify_env_ready
from tests.utils.onenv_utils import run_onenv_command, service_name_to_alias_mapping
from tests.utils.user_utils import Users


@wt(parsers.re(r"(?P<user>\w+) restarts oneprovider (?P<name>.*)"))
def restart_provider(name: str, users: Users, hosts: Hosts) -> None:
    run_onenv_command("exec", [name, "--", "op_worker", "stop"])
    verify_env_ready(users["admin"], hosts)


# NOTE: because of underlying escript implementation this step currently works
# only for krakow oneprovider (TODO VFS-11324)
@wt(
    parsers.re(
        r"(?P<user>\w+) stops network on oneprovider (?P<name>.*) for "
        r"(?P<stop_time>.*) seconds"
    )
)
def restart_network(name: str, stop_time: str, hosts: Hosts) -> None:
    pod_name = hosts[service_name_to_alias_mapping(name)]["pod_name"]
    # TODO VFS-11325 do not copy escripts for each function invocation
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/escript_utils.erl",
            f"{pod_name}:/tmp/escript_utils.erl",
        ],
    )
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/https_restart.escript",
            f"{pod_name}:/tmp/https_restart.escript",
        ],
    )
    run_kubectl_command(
        "exec", [pod_name, "--", "/tmp/https_restart.escript", stop_time]
    )
    time.sleep(int(stop_time))


@wt(parsers.re(r"(?P<user>\w+) stops network on oneprovider (?P<name>.*)"))
def stop_network(name: str, hosts: Hosts) -> None:
    pod_name = hosts[service_name_to_alias_mapping(name)]["pod_name"]
    # TODO VFS-11325 do not copy escripts for each function invocation
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/escript_utils.erl",
            f"{pod_name}:/tmp/escript_utils.erl",
        ],
    )
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/https_stop.escript",
            f"{pod_name}:/tmp/https_stop.escript",
        ],
    )
    run_kubectl_command("exec", [pod_name, "--", "/tmp/https_stop.escript"])


@wt(parsers.re(r"(?P<user>\w+) starts network on oneprovider (?P<name>.*)"))
def start_network(name: str, hosts: Hosts) -> None:
    pod_name = hosts[service_name_to_alias_mapping(name)]["pod_name"]
    # TODO VFS-11325 do not copy escripts for each function invocation
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/escript_utils.erl",
            f"{pod_name}:/tmp/escript_utils.erl",
        ],
    )
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/https_start.escript",
            f"{pod_name}:/tmp/https_start.escript",
        ],
    )
    run_kubectl_command("exec", [pod_name, "--", "/tmp/https_start.escript"])


# NOTE: because of underlying escript implementation this step currently works
# only for krakow oneprovider (TODO VFS-11324)
@wt(parsers.re(r"user mocks archive verifiction on (?P<name>.*) Oneprovider to fail"))
def mock_archive_verification(name: str, hosts: Hosts, run_unmock: object) -> None:
    _ = run_unmock
    pod_name = hosts[service_name_to_alias_mapping(name)]["pod_name"]
    # TODO VFS-11325 do not copy escripts for each function invocation
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/escript_utils.erl",
            f"{pod_name}:/tmp/escript_utils.erl",
        ],
    )
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/archive_verification_mock.escript",
            f"{pod_name}:/tmp/archive_verification_mock.escript",
        ],
    )
    run_kubectl_command(
        "exec", [pod_name, "--", "/tmp/archive_verification_mock.escript"]
    )


# NOTE: because of underlying escript implementation this step currently works
# only for krakow oneprovider (TODO VFS-11324)
@wt(parsers.re(r"Archive verification is unmocked on (?P<name>.*) Oneprovider"))
def unmock_archive_verification(name: str, hosts: Hosts) -> None:
    pod_name = hosts[service_name_to_alias_mapping(name)]["pod_name"]
    # TODO VFS-11325 do not copy escripts for each function invocation
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/escript_utils.erl",
            f"{pod_name}:/tmp/escript_utils.erl",
        ],
    )
    run_kubectl_command(
        "cp",
        [
            "tests/utils/escripts/archive_verification_unmock.escript",
            f"{pod_name}:/tmp/archive_verification_unmock.escript",
        ],
    )
    run_kubectl_command(
        "exec", [pod_name, "--", "/tmp/archive_verification_unmock.escript"]
    )
