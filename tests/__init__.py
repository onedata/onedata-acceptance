"""This file contains definitions of constants used in tests.
It also append useful modules to sys.path to make them available in tests.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"
import os
import sys


_current_dir = os.path.dirname(os.path.realpath(__file__))

# # Define constants for use in tests
# directories
PROJECT_DIR = os.path.dirname(_current_dir)
APPMOCK_DIR = os.path.join(PROJECT_DIR, 'appmock')
BAMBOOS_DIR = os.path.join(PROJECT_DIR, 'bamboos')
DOCKER_DIR = os.path.join(BAMBOOS_DIR, 'docker')
TEST_DIR = os.path.join(PROJECT_DIR, 'tests')
UTILS_DIR = os.path.join(TEST_DIR, 'utils')
ACCEPTANCE_DIR = os.path.join(TEST_DIR, 'acceptance')
ACCEPTANCE_TEST_CONFIG = os.path.join(ACCEPTANCE_DIR, 'test_config.json')
ENV_UP_DIR = os.path.join(TEST_DIR, 'env_up')
PERFORMANCE_DIR = os.path.join(TEST_DIR, 'performance')
PERFORMANCE_TEST_CONFIG = os.path.join(PERFORMANCE_DIR, 'test_config.json')
GUI_DIR = os.path.join(TEST_DIR, 'gui')
MIXED_SWAGGERS_DIR = os.path.join(TEST_DIR, 'mixed_swaggers')
ACCEPTANCE_ENV_DIR = os.path.join(ACCEPTANCE_DIR, 'environments')
GUI_ENV_DIR = os.path.join(GUI_DIR, 'environments')
ACCEPTANCE_LOGDIR = os.path.join(ACCEPTANCE_DIR, 'logs')
ENV_UP_LOGDIR = os.path.join(ENV_UP_DIR, 'logs')
PERFORMANCE_LOGDIR = os.path.join(PERFORMANCE_DIR, 'logs')
PROFILING_LOGDIR = os.path.join(ACCEPTANCE_DIR, 'profiling_data')
GUI_LOGDIR = os.path.join(GUI_DIR, 'logs')
MIXED_SWAGGERS_LOGDIR = os.path.join(MIXED_SWAGGERS_DIR, 'logs')
PERFORMANCE_ENV_DIR = os.path.join(PERFORMANCE_DIR, 'environments')
PERFORMANCE_OUTPUT = os.path.join(PERFORMANCE_LOGDIR, 'performance.json')
EXAMPLE_ENV_DIR = os.path.join(BAMBOOS_DIR, 'example_env')
PROVIDER_CERT_DIR = os.path.join('root', 'bin', 'node', 'etc', 'certs')
PROVIDER_KEY_FILE = 'ozp_key.pem'
PROVIDER_CERT_FILE = 'ozp_cert.pem'
PROVIDER_KEY_PATH = os.path.join(PROVIDER_CERT_DIR, PROVIDER_KEY_FILE)
PROVIDER_CERT_PATH = os.path.join(PROVIDER_CERT_DIR, PROVIDER_CERT_FILE)
ENV_CONFIGURATOR_ESCRIPT = os.path.join(BAMBOOS_DIR, 'env_configurator',
                                        'env_configurator.escript')
UPLOAD_FILES_DIR = os.path.join(GUI_DIR, 'upload_files')

# env_up log files
PREPARE_ENV_LOG_FILE = 'prepare_test_environment.log'
PREPARE_ENV_ERROR_LOG_FILE = 'prepare_test_environment_error.log'

OZ_REST_PORT = 443
OP_REST_PORT = 443
PANEL_REST_PORT = 9443
PANEL_REST_PATH_PREFIX = '/api/v3/onepanel'
OZ_REST_PATH_PREFIX = '/api/v3/onezone'
PROVIDER_REST_PATH_PREFIX = '/api/v3/oneprovider'
CDMI_REST_PATH_PREFIX = '/cdmi'
DEFAULT_HEADERS = {'content-type': 'application/json'}

MEGABYTE = 1024 * 1024

# Append useful modules to the path
sys.path = [PROJECT_DIR, DOCKER_DIR] + sys.path
