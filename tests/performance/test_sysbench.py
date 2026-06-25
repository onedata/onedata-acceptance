"""This module contains performance tests of oneclient using sysbench benchmark."""

# pylint: disable=consider-using-f-string,unused-argument

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.performance.conftest import AbstractPerformanceTest, mount_performance_client
from tests.performance.type_definitions import (
    PerformanceParams,
    int_parameter,
    str_parameter,
)
from tests.type_definitions import EnvDesc, Hosts, Users
from tests.utils.client_utils import Client, CommandResult
from tests.utils.performance_utils import generate_configs, performance

REPEATS = 1
SUCCESS_RATE = 100


class TestSysbench(AbstractPerformanceTest):

    @performance(
        default_config={
            "repeats": REPEATS,
            "success_rate": SUCCESS_RATE,
            "parameters": {
                "files_number": {"description": "Number of files", "unit": ""},
                "threads": {"description": "Number of threads to use", "unit": ""},
                "mode": {"description": "Modes", "unit": ""},
                "total_size": {"description": "Total size", "unit": "MB"},
                "validate": {
                    "description": "Perform validation of test results where possible",
                    "unit": "",
                },
                "events": {
                    "description": "Limit for total number of events.",
                    "unit": "",
                },
                "report_interval": {
                    "description": (
                        "Periodically report intermediate statistics with a "
                        "specified interval in seconds. Note that statistics "
                        "produced by this option is per-interval rather "
                        "than cumulative. 0 disables intermediate reports"
                    ),
                    "unit": "s",
                },
                "time": {
                    "description": "Limit for total execution time in seconds.",
                    "unit": "s",
                },
                "file_block_size": {
                    "description": "Block size to use in all I/O operations",
                    "unit": "KB",
                },
            },
            "description": "Testing file system using sysbench",
        },
        configs=generate_configs(
            {
                "files_number": [1],
                "threads": [1],
                "total_size": [2048],
                "mode": ["rndrd", "rndrw", "rndwr", "seqrd", "seqwr"],
                "validate": ["on"],
                "events": [100000],
                "report_interval": [15],
                "time": [0],
                "file_block_size": [4],
            },
            "SYSBENCH TEST -- "
            "Files number: {files_number} "
            "Threads number: {threads} "
            "Total Size: {total_size} "
            "Mode: {mode}",
        ),
    )
    def test_sysbench(
        self, hosts: Hosts, users: Users, env_desc: EnvDesc, params: PerformanceParams
    ) -> None:
        user_directio = "user1"
        user_proxy = "user2"
        client_directio = mount_performance_client(
            users, hosts, env_desc, user_directio, "oneclient-1", "client11"
        )
        client_proxy = mount_performance_client(
            users, hosts, env_desc, user_proxy, "oneclient-2", "client21"
        )

        threads = int_parameter(params, "threads")
        files_number = int_parameter(params, "files_number")
        total_size = int_parameter(params, "total_size")
        mode = str_parameter(params, "mode")
        validate = str_parameter(params, "validate")
        events = int_parameter(params, "events")
        report_interval = int_parameter(params, "report_interval")
        time = int_parameter(params, "time")
        file_block_size = int_parameter(params, "file_block_size")

        dir_path_directio = client_directio.mkdtemp(
            directory=client_directio.absolute_path("space1")
        )

        dir_path_proxy = client_proxy.mkdtemp(
            directory=client_proxy.absolute_path("space1")
        )

        print(
            "\n################################## DIRECT-IO client (%s)"
            " ##################################\n" % (mode)
        )

        execute_sysbench_test(
            client_directio,
            user_directio,
            threads,
            total_size,
            files_number,
            mode,
            validate,
            events,
            report_interval,
            time,
            file_block_size,
            dir_path_directio,
        )

        print(
            "\n################################## PROXY-IO client (%s)"
            " ##################################\n" % (mode)
        )

        execute_sysbench_test(
            client_proxy,
            user_proxy,
            threads,
            total_size,
            files_number,
            mode,
            validate,
            events,
            report_interval,
            time,
            file_block_size,
            dir_path_proxy,
        )

        client_directio.rm(dir_path_directio, recursive=True, force=True)
        client_proxy.rm(dir_path_proxy, recursive=True, force=True)


################################################################################


def execute_sysbench_test(
    client: Client,
    user: str,
    threads: int,
    total_size: int,
    files_number: int,
    mode: str,
    validate: str,
    events: int,
    report_interval: int,
    time: int,
    file_block_size: int,
    dir_path: str,
) -> None:
    sysbench_tests(
        threads,
        total_size,
        files_number,
        mode,
        validate,
        events,
        report_interval,
        time,
        file_block_size,
        client,
        user,
        dir_path,
    )


def sysbench_tests(
    threads: int,
    total_size: int,
    file_number: int,
    mode: str,
    validate: str,
    events: int,
    report_interval: int,
    time: int,
    file_block_size: int,
    client: Client,
    user: str,
    directory: str,
) -> None:
    run_sysbench_prepare(
        threads,
        total_size,
        file_number,
        mode,
        validate,
        events,
        report_interval,
        time,
        file_block_size,
        client,
        user,
        directory,
    )
    code = run_sysbench(
        threads,
        total_size,
        file_number,
        mode,
        validate,
        events,
        report_interval,
        time,
        file_block_size,
        client,
        user,
        directory,
    )
    assert code == 0
    run_sysbench_cleanup(
        threads,
        total_size,
        file_number,
        mode,
        validate,
        events,
        report_interval,
        time,
        file_block_size,
        client,
        user,
        directory,
    )


def run_sysbench_prepare(
    threads: int,
    total_size: int,
    file_number: int,
    mode: str,
    validate: str,
    events: int,
    report_interval: int,
    time: int,
    file_block_size: int,
    client: Client,
    user: str,
    directory: str,
) -> CommandResult:
    print("=== Preparing sysbench test files...")
    return sysbench(
        threads,
        total_size,
        file_number,
        mode,
        validate,
        events,
        report_interval,
        time,
        file_block_size,
        "prepare",
        client,
        user,
        directory,
        output=True,
    )


def run_sysbench_cleanup(
    threads: int,
    total_size: int,
    file_number: int,
    mode: str,
    validate: str,
    events: int,
    report_interval: int,
    time: int,
    file_block_size: int,
    client: Client,
    user: str,
    directory: str,
) -> CommandResult:
    print("=== Removing sysbench test files...")
    return sysbench(
        threads,
        total_size,
        file_number,
        mode,
        validate,
        events,
        report_interval,
        time,
        file_block_size,
        "cleanup",
        client,
        user,
        directory,
        output=True,
    )


def run_sysbench(
    threads: int,
    total_size: int,
    file_number: int,
    mode: str,
    validate: str,
    events: int,
    report_interval: int,
    time: int,
    file_block_size: int,
    client: Client,
    user: str,
    directory: str,
) -> CommandResult:
    return sysbench(
        threads,
        total_size,
        file_number,
        mode,
        validate,
        events,
        report_interval,
        time,
        file_block_size,
        "run",
        client,
        user,
        directory,
    )


def sysbench(
    threads: int,
    total_size: int,
    file_number: int,
    mode: str,
    validate: str,
    events: int,
    report_interval: int,
    time: int,
    file_block_size: int,
    operation: str,
    client: Client,
    user: str,
    directory: str,
    output: bool = False,
) -> CommandResult:
    cmd = sysbench_command(
        threads,
        total_size,
        file_number,
        mode,
        validate,
        events,
        report_interval,
        time,
        file_block_size,
        operation,
        directory,
    )

    return client.run_cmd(cmd, output=output)


def sysbench_command(
    threads: int,
    total_size: int,
    file_number: int,
    mode: str,
    validate: str,
    events: int,
    report_interval: int,
    time: int,
    file_block_size: int,
    operation: str,
    directory: str,
) -> str:

    cmd = (
        "cd {dir} && "
        "sysbench "
        "--threads={threads} "
        "--file-total-size={total_size}M "
        "--file-num={file_number} "
        "--file-test-mode={mode} "
        "--validate={validate} "
        "--events={events} "
        "--report-interval={report_interval} "
        "--time={time} "
        "--file-block-size={file_block_size}K "
        "fileio "
        "{type}"
    ).format(
        dir=directory,
        threads=threads,
        total_size=total_size,
        file_number=file_number,
        mode=mode,
        validate=validate,
        events=events,
        report_interval=report_interval,
        time=time,
        file_block_size=file_block_size,
        type=operation,
    )

    return cmd
