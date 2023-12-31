"""This module contains performance tests of on the fly transfer,
testing concurrent copy of 10000 files created on remote provider.
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time
import os.path
from itertools import repeat, chain
from threading import Thread
from queue import Queue, Empty

from tests.performance.conftest import AbstractPerformanceTest
from tests.utils.performance_utils import (Result, generate_configs,
                                           performance, flushed_print)

REPEATS = 1
SUCCESS_RATE = 100
LOGGING_INTERVAL = 30


class TestTransferOnf(AbstractPerformanceTest):

    @performance(
        default_config={
            'repeats': REPEATS,
            'success_rate': SUCCESS_RATE,
            'parameters': {
                'files_number': {
                    'description': 'number of files',
                    'unit': 'int'
                },
                'files_size': {
                    'description': 'size of each file in Bytes',
                    'unit': 'int'
                },
                'threads_num': {
                    'description': 'number of threads creating/copying files',
                    'unit': 'int'
                }
            },
            'description': 'Testing transfer on the fly with '
                           'concurrent copying of files'
        },
        configs=generate_configs({
            'files_number': [10000],
            'files_size': [20480],
            'threads_num': [10]
        }, 'TRANSFER ON THE FLY TEST -- '
           'Files number: {files_number} '
           'Files size: {files_size} '
           'Threads number: {threads_num}'))
    def test_transfer_onf(self, hosts, users, env_desc, params):
        client1 = users['user1'].mount_client('oneclient-1', 'client11', hosts, env_desc)
        client2 = users['user2'].mount_client('oneclient-2', 'client21', hosts, env_desc)

        files_number = params['files_number']['value']
        file_size = params['files_size']['value']
        threads_num = params['threads_num']['value']

        dir_path_1 = client1.absolute_path('space1')
        dir_path_2 = client2.absolute_path('space1')

        _create_files(client1, files_number, file_size, dir_path_1)
        # NOTE wait for synchronization between providers before copying
        time.sleep(60)

        test_result = _execute_test(client2, files_number, file_size / 1024,
                                    threads_num, dir_path_2)

        # removal of entire directory tree can take several minutes so as to
        # evade connection timeout while removing everything at once,
        # rm files one at time instead
        _teardown_after_test(client2, files_number, dir_path_2)

        return test_result

################################################################################


def _create_files(client, files_num, file_size, dir_path):
    flushed_print('\t\tStarted creation of {} files'.format(files_num))
    for i in range(files_num):
        if i % 100 == 0:
            flushed_print('\t\t\tCreated {}nth file'.format(i))
        client.truncate(os.path.join(dir_path, 'file{}'.format(i)), file_size)


def _execute_test(client, files_number, file_size, threads_num, dir_path):
    avg_work = files_number // threads_num
    intervals = chain(repeat(avg_work, threads_num-1),
                      [avg_work + files_number % threads_num])
    i = 0
    workers = []
    queue = Queue()
    for interval in intervals:
        j = i + interval
        workers.append(Thread(target=_copy_files,
                              args=(client, i, j, dir_path, queue)))
        i = j

    start = time.time()
    logging_time = start + LOGGING_INTERVAL

    for worker in workers:
        worker.start()

    flushed_print('\t\tStarted {} workers with avg {} file copying task each'
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
        Result('[{} threads] {} files copied'.format(threads_num, files_number),
               end - start,
               '{} files copying time using oneclient with {}MB size'
               ''.format(files_number, file_size),
               'seconds')
    ]


def _copy_files(client, start, end, dir_path, queue):
    try:
        for i in range(start, end):
            src_file = os.path.join(dir_path, 'file{}'.format(i))
            dst_file = os.path.join(dir_path, 'file{}.bak'.format(i))
            client.cp(src_file, dst_file)
    except Exception as ex:
        queue.put(ex)


def _teardown_after_test(client, files_number, dir_path):
    logging_time = time.time() + LOGGING_INTERVAL
    for i in range(files_number):
        client.rm(os.path.join(dir_path, 'file{}'.format(i)))
        client.rm(os.path.join(dir_path, 'file{}.bak'.format(i)))
        if time.time() >= logging_time:
            flushed_print('\t\t\tDeleted {}nth file'.format(i))
            logging_time = time.time() + LOGGING_INTERVAL
