"""This module contains performance tests of oneclient,
testing creation of 10000 files.
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time
import os.path
from functools import partial

from tests.performance.conftest import AbstractPerformanceTest
from tests.utils.performance_utils import (Result, generate_configs,
                                           performance, flushed_print)
from tests.utils.client_utils import user_home_dir

REPEATS = 1
SUCCESS_RATE = 100
LOGGING_INTERVAL = 30
RPYC_TIMEOUT = 120

# value written to files at their creation
TEXT = 'asd'


class TestFilesCreation(AbstractPerformanceTest):

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
                }
            },
            'description': 'Testing file creation'
        },
        configs=generate_configs({
            'files_number': [5000],
            'empty_files': [True, False]
        }, 'FILE CREATION TEST -- '
           'Files number: {files_number} '
           'Empty files: {empty_files}'))
    def test_files_creation(self, hosts, users, env_desc, params):
        user_proxy = 'user2'
        client_directio = users['user1'].mount_client('oneclient-1', 'client11', hosts, env_desc)
        client_proxy = users[user_proxy].mount_client('oneclient-2', 'client21', hosts, env_desc)

        files_number = params['files_number']['value']
        empty_files = params['empty_files']['value']

        for client in (client_directio, client_proxy):
            conn = client.rpyc_connection
            conn._config['sync_request_timeout'] = RPYC_TIMEOUT

        dir_path_directio = client_directio.mkdtemp(dir=client_directio.absolute_path('space1'))

        dir_path_proxy = client_proxy.mkdtemp(dir=client_proxy.absolute_path('space1'))
        dir_path_host = client_proxy.mkdtemp(dir=user_home_dir(user_proxy))

        test_result1 = execute_file_creation_test(client_directio, files_number,
                                                  empty_files, dir_path_directio,
                                                  'direct IO')
        test_result2 = execute_file_creation_test(client_proxy, files_number,
                                                  empty_files, dir_path_proxy,
                                                  'cluster-proxy')
        test_result3 = execute_file_creation_test(client_proxy, files_number,
                                                  empty_files, dir_path_host,
                                                  'host system')

        # removal of entire directory tree can take several minutes, so as to
        # evade connection timeout while removing everything at once,
        # rm files one at time instead
        teardown_after_file_creation_test(client_directio, files_number,
                                          dir_path_directio)
        teardown_after_file_creation_test(client_proxy, files_number,
                                          dir_path_proxy)
        teardown_after_file_creation_test(client_proxy, files_number,
                                          dir_path_host)

        client_directio.rm(dir_path_directio, recursive=True, force=True)
        client_proxy.rm(dir_path_proxy, recursive=True, force=True)
        client_proxy.rm(dir_path_host, recursive=True, force=True)

        return test_result1 + test_result2 + test_result3

################################################################################


def execute_file_creation_test(client, files_number, empty_files,
                               dir_path, description):
    start = time.time()
    logging_time = start + LOGGING_INTERVAL

    fun = client.create_file if empty_files else partial(client.write, text=TEXT)
    for i in range(files_number):
        fun(file_path=os.path.join(dir_path, 'file{}'.format(i)))
        if time.time() >= logging_time:
            flushed_print('\t\t\tCreated {}nth file'.format(i))
            logging_time = time.time() + LOGGING_INTERVAL

    end = time.time()

    return [
        Result('[{}] {} files creation'.format(description, files_number),
               end - start,
               '{} files creation time using oneclient with {} content'
               ''.format(files_number, ('no' if empty_files else 'some')),
               'seconds')
    ]


def teardown_after_file_creation_test(client, files_number, dir_path):
    logging_time = time.time() + LOGGING_INTERVAL
    for i in range(files_number):
        client.rm(os.path.join(dir_path, 'file{}'.format(i)))
        if time.time() >= logging_time:
            flushed_print('\t\t\tDeleted {}nth file'.format(i))
            logging_time = time.time() + LOGGING_INTERVAL
