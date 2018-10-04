from tests import *


def map_test_type_to_env_dir(test_type):
    return {
        'acceptance': ACCEPTANCE_ENV_DIR,
        'performance': PERFORMANCE_ENV_DIR,
        'gui': GUI_ENV_DIR,
        'mixed_swaggers': GUI_ENV_DIR
    }[test_type]


def map_test_type_to_logdir(test_type):
    return {
        'acceptance': ACCEPTANCE_LOGDIR,
        'performance': PERFORMANCE_LOGDIR,
        'mixed_swaggers': MIXED_SWAGGERS_LOGDIR,
        'mixed_oneclient': MIXED_ONECLIENT_LOGDIR,
        'gui': GUI_LOGDIR
    }.get(test_type, ACCEPTANCE_LOGDIR)


def map_test_type_to_test_config_file(test_type):
    return {
        'acceptance': ACCEPTANCE_TEST_CONFIG,
        'performance': PERFORMANCE_TEST_CONFIG
    }.get(test_type)


def map_test_type_to_scenario_dir(test_type):
    return {
        'acceptance': ACCEPTANCE_SCENARIO_DIR
    }.get(test_type)


def map_test_type_to_landscape_dir(test_type):
    return {
        'acceptance': ACCEPTANCE_LANDSCAPE_DIR
    }.get(test_type)


def get_test_type(request):
    return request.config.getoption('test_type')
