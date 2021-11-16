"""This module contains performance tests of oneclient,
testing concurrent creation of 10000 files.
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time
import os.path
from functools import partial
from itertools import repeat, chain
from threading import Thread
from queue import Queue, Empty

from tests.performance.conftest import AbstractPerformanceTest
from tests.utils.performance_utils import (Result, generate_configs,
                                           performance, flushed_print)
from tests.utils.client_utils import user_home_dir

REPEATS = 1
SUCCESS_RATE = 100
LOGGING_INTERVAL = 30

# value written to files at their creation
TEXT = 'asd'


class TestConcurrentFilesCreation(AbstractPerformanceTest):

    @performance(
        default_config={
            'repeats': REPEATS,
            'success_rate': SUCCESS_RATE,
            'parameters': {
                'files_number': {
                    'description': 'number of files',
                    'unit': 'int'
                },
                'empty_files': {
                    'description': 'if true, files will be '
                                   'created with no content',
                    'unit': 'boolean'
                },
                'threads_num': {
                    'description': 'number of threads creating files',
                    'unit': 'int'
                }
            },
            'description': 'Testing file creation'
        },
        configs=generate_configs({
            'files_number': [10000],
            'empty_files': [True, False],
            'threads_num': [10]
        }, 'FILE CREATION TEST -- '
           'Files number: {files_number} '
           'Empty files: {empty_files} '
           'Threads number: {threads_num}'))
    def test_concurrent_files_creation(self, hosts, users, env_desc, params):
        user_proxy = 'user2'
        client_directio = users['user1'].mount_client('oneclient-1', 'client11', hosts, env_desc)
        client_proxy = users[user_proxy].mount_client('oneclient-2', 'client21', hosts, env_desc)

        files_number = params['files_number']['value']
        empty_files = params['empty_files']['value']
        threads_num = params['threads_num']['value']

        dir_path_directio = client_directio.mkdtemp(dir=client_directio.absolute_path('space1'))

        dir_path_proxy = client_proxy.mkdtemp(dir=client_proxy.absolute_path('space1'))
        dir_path_host = client_proxy.mkdtemp(dir=user_home_dir(user_proxy))

        test_result1 = _execute_test(client_directio, files_number, empty_files,
                                     threads_num, dir_path_directio, 'direct IO')
        test_result2 = _execute_test(client_proxy, files_number, empty_files,
                                     threads_num, dir_path_proxy, 'cluster-proxy')
        test_result3 = _execute_test(client_proxy, files_number, empty_files,
                                     threads_num, dir_path_host, 'host system')

        # removal of entire directory tree can take several minutes so as to
        # evade connection timeout while removing everything at once,
        # rm files one at time instead
        _teardown_after_test(client_directio, files_number,
                             dir_path_directio)
        _teardown_after_test(client_proxy, files_number,
                             dir_path_proxy)
        _teardown_after_test(client_proxy, files_number,
                             dir_path_host)

        client_directio.rm(dir_path_directio, recursive=True, force=True)
        client_proxy.rm(dir_path_proxy, recursive=True, force=True)
        client_proxy.rm(dir_path_host, recursive=True, force=True)

        return test_result1 + test_result2 + test_result3

################################################################################


def _execute_test(client, files_number, empty_files, threads_num,
                  dir_path, description):
    avg_work = files_number // threads_num
    intervals = chain(repeat(avg_work, threads_num-1),
                      [avg_work + files_number % threads_num])
    i = 0
    workers = []
    queue = Queue()
    for interval in intervals:
        j = i + interval
        workers.append(Thread(target=_create_files,
                              args=(client, i, j, empty_files,
                                    dir_path, queue)))
        i = j

    start = time.time()
    logging_time = start + LOGGING_INTERVAL

    for worker in workers:
        worker.start()

    flushed_print('\t\tStarted {} workers with avg {} file creation task each'
                  ''.format(len(workers), avg_work))

    while workers:
        try:
            ex = queue.get(timeout=5)
        except Empty:
            workers = [worker for worker in workers if worker.is_alive()]
        else:
            raise ex
        finally:
            if time.time() >= logging_time:
                flushed_print('\t\t\t{} workers alive'.format(len(workers)))
                logging_time = time.time() + LOGGING_INTERVAL

    if not queue.empty():
        raise queue.get()

    end = time.time()

    return [
        Result('[{}; {} threads] {} files creation'.format(description,
                                                           threads_num,
                                                           files_number),
               end - start,
               '{} files creation time using oneclient with {} content'
               ''.format(files_number, ('no' if empty_files else 'some')),
               'seconds')
    ]


def _create_files(client, start, end, empty_files, dir_path, queue):
    fun = client.create_file if empty_files else partial(client.write, text=TEXT)
    try:
        for i in range(start, end):
            fun(file_path=os.path.join(dir_path, 'file{}'.format(i)))
    except Exception as ex:
        queue.put(ex)


def _teardown_after_test(client, files_number, dir_path):
    logging_time = time.time() + LOGGING_INTERVAL
    for i in range(files_number):
        client.rm(os.path.join(dir_path, 'file{}'.format(i)))
        if time.time() >= logging_time:
            flushed_print('\t\t\tDeleted {}nth file'.format(i))
            logging_time = time.time() + LOGGING_INTERVAL
