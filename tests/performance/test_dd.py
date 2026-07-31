"""This module contains performance tests of dd operation in oneclient."""

# pylint: disable=consider-using-f-string,invalid-name

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import re

from tests.performance.conftest import AbstractPerformanceTest, mount_performance_client
from tests.performance.type_definitions import (
    PerformanceParams,
    int_parameter,
    str_parameter,
)
from tests.type_definitions import EnvDesc, Hosts
from tests.utils.client_utils import Client, user_home_dir
from tests.utils.performance_utils import Result, generate_configs, performance
from tests.utils.user_utils import Users

REPEATS = 3
SUCCESS_RATE = 95
DD_OUTPUT_REGEX = r".*\s+s, (\d+\.?\d+?) (\w+/s)"
DD_OUTPUT_PATTERN = re.compile(DD_OUTPUT_REGEX)
SYSBENCH_OUTPUT_REGEX = (
    r"Total transferred \d+.?\d+?\w+\s+\((\d+.?\d+)"
    r"(\w+/\w+)\)\s+(\d+.?\d+?)\s+(\w+/\w+)"
)
SYSBENCH_OUTPUT_PATTERN = re.compile(SYSBENCH_OUTPUT_REGEX, re.MULTILINE)


class Testdd(AbstractPerformanceTest):

    @performance(
        default_config={
            "repeats": REPEATS,
            "success_rate": SUCCESS_RATE,
            "parameters": {
                "size": {"description": "size", "unit": "kB"},
                "block_size": {"description": "size of block", "unit": "kB"},
            },
            "description": "Test of dd throughput",
        },
        configs=generate_configs(
            {
                "block_size": [1, 4, 128, 1024],
                "size": [1024, 10240],  # , 1048576, 10485760]
            },
            "DD TEST -- block size: {block_size} size: {size}",
        ),
    )
    def test_dd(
        self, hosts: Hosts, users: Users, env_desc: EnvDesc, params: PerformanceParams
    ) -> list[Result]:
        user_directio = "user1"
        user_proxy = "user2"
        client_directio = mount_performance_client(
            users, hosts, env_desc, user_directio, "oneclient-1", "client11"
        )
        client_proxy = mount_performance_client(
            users, hosts, env_desc, user_proxy, "oneclient-2", "client21"
        )

        size = int_parameter(params, "size")
        size_unit = str_parameter(params, "size", "unit")
        block_size = int_parameter(params, "block_size")
        block_size_unit = str_parameter(params, "block_size", "unit")

        test_file_directio = client_directio.mkstemp(
            directory=client_directio.absolute_path("space1")
        )

        test_file_proxy = client_proxy.mkstemp(
            directory=client_proxy.absolute_path("space1")
        )
        test_file_host = client_proxy.mkstemp(directory=user_home_dir(user_proxy))

        test_result1 = execute_dd_test(
            client_directio,
            test_file_directio,
            block_size,
            block_size_unit,
            size,
            size_unit,
            "direct IO",
        )

        test_result2 = execute_dd_test(
            client_proxy,
            test_file_proxy,
            block_size,
            block_size_unit,
            size,
            size_unit,
            "cluster-proxy",
        )

        test_result3 = execute_dd_test(
            client_proxy,
            test_file_host,
            block_size,
            block_size_unit,
            size,
            size_unit,
            "host system",
        )

        client_directio.rm(test_file_directio, recursive=True, force=True)
        client_proxy.rm(test_file_proxy, recursive=True, force=True)
        client_proxy.rm(test_file_host, recursive=True, force=True)

        return test_result1 + test_result2 + test_result3


################################################################################


def execute_dd_test(
    client: Client,
    test_file: str,
    block_size: int | float,
    block_size_unit: str,
    size: int | float,
    size_unit: str,
    description: str,
) -> list[Result]:

    dev_zero = os.path.join("/dev", "zero")

    write_throughput = parse_dd_output(
        do_dd(client, dev_zero, test_file, block_size, block_size_unit, size, size_unit)
    )

    read_throughput = parse_dd_output(
        do_dd(client, test_file, dev_zero, block_size, block_size_unit, size, size_unit)
    )

    return [
        Result(
            "write_throughput_{}".format(description),
            write_throughput,
            "Throughput of write operation in case of {}".format(description),
            "MB/s",
        ),
        Result(
            "read_throughput_{}".format(description),
            read_throughput,
            "Throughput of read operation in case of {}".format(description),
            "MB/s",
        ),
    ]


def do_dd(
    client: Client,
    input_file: str,
    output: str,
    block_size: int | float,
    block_size_unit: str,
    size: int | float,
    size_unit: str,
) -> str:
    block_size_unit = SI_prefix_to_default(block_size_unit)
    size_unit = SI_prefix_to_default(size_unit)
    size = convert_size(size, size_unit, "k")
    block_size = convert_size(block_size, block_size_unit, "k")
    count = size // block_size

    result = client.dd(
        int(block_size),
        int(count),
        output,
        unit="k",
        output=True,
        error=True,
        input_file=input_file,
    )
    if not isinstance(result, str):
        raise TypeError("dd did not return its output")
    return result


def parse_dd_output(dd_output: str) -> float:
    dd_output = dd_output.split("\n")[-2].strip()
    m = re.match(DD_OUTPUT_PATTERN, dd_output)
    if m is None:
        raise ValueError(f"Cannot parse dd output: {dd_output}")
    value = float(m.group(1))
    unit = m.group(2)
    size_unit = unit.split("/")[0]
    return convert_size(value, size_unit, "M")


def convert_size(value: int | float, prefix: str, convert_to_prefix: str) -> float:
    convert_to_prefix = convert_to_prefix.upper()
    si_powers_prefixes = ["kB", "MB", "GB", "TB"]
    si_powers_values = [1000**p for p in range(1, 5)]
    si_powers = dict(zip(si_powers_prefixes, si_powers_values))
    powers_prefixes = ["K", "M", "G", "T"]
    powers_values = [1024**p for p in range(1, 5)]
    powers = dict(zip(powers_prefixes, powers_values))

    if is_SI_prefix(prefix):
        factor = float(si_powers[prefix]) / powers[convert_to_prefix]
    else:
        factor = float(powers[prefix]) / powers[convert_to_prefix]

    return value * factor


def is_SI_prefix(prefix: str) -> bool:
    return prefix.endswith("B")


def SI_prefix_to_default(prefix: str) -> str:
    return prefix.upper().strip("B")
