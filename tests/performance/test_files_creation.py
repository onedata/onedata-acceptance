"""This module contains performance tests of oneclient,
testing creation of 10000 files.
"""

# pylint: disable=consider-using-f-string,protected-access

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os.path
import time
from functools import partial

from tests.performance.conftest import AbstractPerformanceTest, mount_performance_client
from tests.performance.type_definitions import (
    PerformanceParams,
    bool_parameter,
    int_parameter,
)
from tests.type_definitions import EnvDesc, Hosts, Users
from tests.utils.client_utils import Client, user_home_dir
from tests.utils.performance_utils import (
    Result,
    flushed_print,
    generate_configs,
    performance,
)

REPEATS = 1
SUCCESS_RATE = 100
LOGGING_INTERVAL = 30
RPYC_TIMEOUT = 120

# value written to files at their creation
TEXT = "asd"


class TestFilesCreation(AbstractPerformanceTest):

    @performance(
        default_config={
            "repeats": REPEATS,
            "success_rate": SUCCESS_RATE,
            "parameters": {
                "files_number": {"description": "number of files", "unit": "int"},
                "empty_files": {
                    "description": "if true, files will be created with no content",
                    "unit": "boolean",
                },
            },
            "description": "Testing file creation",
        },
        configs=generate_configs(
            {"files_number": [5000], "empty_files": [True, False]},
            "FILE CREATION TEST -- "
            "Files number: {files_number} "
            "Empty files: {empty_files}",
        ),
    )
    def test_files_creation(
        self, hosts: Hosts, users: Users, env_desc: EnvDesc, params: PerformanceParams
    ) -> list[Result]:
        user_proxy = "user2"
        client_directio = mount_performance_client(
            users, hosts, env_desc, "user1", "oneclient-1", "client11"
        )
        client_proxy = mount_performance_client(
            users, hosts, env_desc, user_proxy, "oneclient-2", "client21"
        )

        files_number = int_parameter(params, "files_number")
        empty_files = bool_parameter(params, "empty_files")

        for client in (client_directio, client_proxy):
            conn = client.rpyc_connection
            conn._config["sync_request_timeout"] = RPYC_TIMEOUT

        dir_path_directio = client_directio.mkdtemp(
            directory=client_directio.absolute_path("space1")
        )

        dir_path_proxy = client_proxy.mkdtemp(
            directory=client_proxy.absolute_path("space1")
        )
        dir_path_host = client_proxy.mkdtemp(directory=user_home_dir(user_proxy))

        test_result1 = execute_file_creation_test(
            client_directio, files_number, empty_files, dir_path_directio, "direct IO"
        )
        test_result2 = execute_file_creation_test(
            client_proxy, files_number, empty_files, dir_path_proxy, "cluster-proxy"
        )
        test_result3 = execute_file_creation_test(
            client_proxy, files_number, empty_files, dir_path_host, "host system"
        )

        # removal of entire directory tree can take several minutes, so as to
        # evade connection timeout while removing everything at once,
        # rm files one at time instead
        teardown_after_file_creation_test(
            client_directio, files_number, dir_path_directio
        )
        teardown_after_file_creation_test(client_proxy, files_number, dir_path_proxy)
        teardown_after_file_creation_test(client_proxy, files_number, dir_path_host)

        client_directio.rm(dir_path_directio, recursive=True, force=True)
        client_proxy.rm(dir_path_proxy, recursive=True, force=True)
        client_proxy.rm(dir_path_host, recursive=True, force=True)

        return test_result1 + test_result2 + test_result3


################################################################################


def execute_file_creation_test(
    client: Client,
    files_number: int,
    empty_files: bool,
    dir_path: str,
    description: str,
) -> list[Result]:
    start = time.time()
    logging_time = start + LOGGING_INTERVAL

    fun = client.create_file if empty_files else partial(client.write, text=TEXT)
    for i in range(files_number):
        fun(file_path=os.path.join(dir_path, "file{}".format(i)))
        if time.time() >= logging_time:
            flushed_print("\t\t\tCreated {}nth file".format(i))
            logging_time = time.time() + LOGGING_INTERVAL

    end = time.time()

    return [
        Result(
            "[{}] {} files creation".format(description, files_number),
            end - start,
            "{} files creation time using oneclient with {} content".format(
                files_number, ("no" if empty_files else "some")
            ),
            "seconds",
        )
    ]


def teardown_after_file_creation_test(
    client: Client, files_number: int, dir_path: str
) -> None:
    logging_time = time.time() + LOGGING_INTERVAL
    for i in range(files_number):
        client.rm(os.path.join(dir_path, "file{}".format(i)))
        if time.time() >= logging_time:
            flushed_print("\t\t\tDeleted {}nth file".format(i))
            logging_time = time.time() + LOGGING_INTERVAL
