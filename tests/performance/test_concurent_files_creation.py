"""This module contains performance tests of oneclient,
testing concurrent creation of 10000 files.
"""

# pylint: disable=consider-using-f-string,broad-exception-caught

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os.path
import time
from functools import partial
from itertools import chain, repeat
from queue import Empty, Queue
from threading import Thread

from tests.conftest import EnvDesc, Hosts, Users
from tests.performance.conftest import AbstractPerformanceTest, mount_performance_client
from tests.performance.types import (
    ExceptionQueue,
    PerformanceParams,
    bool_parameter,
    int_parameter,
)
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

# value written to files at their creation
TEXT = "asd"


class TestConcurrentFilesCreation(AbstractPerformanceTest):

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
                "threads_num": {
                    "description": "number of threads creating files",
                    "unit": "int",
                },
            },
            "description": "Testing file creation",
        },
        configs=generate_configs(
            {
                "files_number": [10000],
                "empty_files": [True, False],
                "threads_num": [10],
            },
            "FILE CREATION TEST -- "
            "Files number: {files_number} "
            "Empty files: {empty_files} "
            "Threads number: {threads_num}",
        ),
    )
    def test_concurrent_files_creation(
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
        threads_num = int_parameter(params, "threads_num")

        dir_path_directio = client_directio.mkdtemp(
            directory=client_directio.absolute_path("space1")
        )

        dir_path_proxy = client_proxy.mkdtemp(
            directory=client_proxy.absolute_path("space1")
        )
        dir_path_host = client_proxy.mkdtemp(directory=user_home_dir(user_proxy))

        test_result1 = _execute_test(
            client_directio,
            files_number,
            empty_files,
            threads_num,
            dir_path_directio,
            "direct IO",
        )
        test_result2 = _execute_test(
            client_proxy,
            files_number,
            empty_files,
            threads_num,
            dir_path_proxy,
            "cluster-proxy",
        )
        test_result3 = _execute_test(
            client_proxy,
            files_number,
            empty_files,
            threads_num,
            dir_path_host,
            "host system",
        )

        # removal of entire directory tree can take several minutes so as to
        # evade connection timeout while removing everything at once,
        # rm files one at time instead
        _teardown_after_test(client_directio, files_number, dir_path_directio)
        _teardown_after_test(client_proxy, files_number, dir_path_proxy)
        _teardown_after_test(client_proxy, files_number, dir_path_host)

        client_directio.rm(dir_path_directio, recursive=True, force=True)
        client_proxy.rm(dir_path_proxy, recursive=True, force=True)
        client_proxy.rm(dir_path_host, recursive=True, force=True)

        return test_result1 + test_result2 + test_result3


################################################################################


def _execute_test(
    client: Client,
    files_number: int,
    empty_files: bool,
    threads_num: int,
    dir_path: str,
    description: str,
) -> list[Result]:
    avg_work = files_number // threads_num
    intervals = chain(
        repeat(avg_work, threads_num - 1), [avg_work + files_number % threads_num]
    )
    i = 0
    workers = []
    queue: ExceptionQueue = Queue()
    for interval in intervals:
        j = i + interval
        workers.append(
            Thread(
                target=_create_files, args=(client, i, j, empty_files, dir_path, queue)
            )
        )
        i = j

    start = time.time()
    logging_time = start + LOGGING_INTERVAL

    for worker in workers:
        worker.start()

    flushed_print(
        "\t\tStarted {} workers with avg {} file creation task each".format(
            len(workers), avg_work
        )
    )

    while workers:
        try:
            ex = queue.get(timeout=5)
        except Empty:
            workers = [worker for worker in workers if worker.is_alive()]
        else:
            raise ex
        finally:
            if time.time() >= logging_time:
                flushed_print("\t\t\t{} workers alive".format(len(workers)))
                logging_time = time.time() + LOGGING_INTERVAL

    if not queue.empty():
        raise queue.get()

    end = time.time()

    return [
        Result(
            "[{}; {} threads] {} files creation".format(
                description, threads_num, files_number
            ),
            end - start,
            "{} files creation time using oneclient with {} content".format(
                files_number, ("no" if empty_files else "some")
            ),
            "seconds",
        )
    ]


def _create_files(
    client: Client,
    start: int,
    end: int,
    empty_files: bool,
    dir_path: str,
    queue: ExceptionQueue,
) -> None:
    fun = client.create_file if empty_files else partial(client.write, text=TEXT)
    try:
        for i in range(start, end):
            fun(file_path=os.path.join(dir_path, "file{}".format(i)))
    except Exception as ex:
        queue.put(ex)


def _teardown_after_test(client: Client, files_number: int, dir_path: str) -> None:
    logging_time = time.time() + LOGGING_INTERVAL
    for i in range(files_number):
        client.rm(os.path.join(dir_path, "file{}".format(i)))
        if time.time() >= logging_time:
            flushed_print("\t\t\tDeleted {}nth file".format(i))
            logging_time = time.time() + LOGGING_INTERVAL
