"""This file contains utility functions for operation on file paths.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import inspect
import os
import sys
import time
import json
import yaml

SERVICE_TO_ARTIFACT_PLAN = {
    'onezone': ('onezone-pkg', 'docker-build-list.json'),
    'oneprovider': ('oneprovider-pkg', 'docker-build-list.json'),
    'oneclient': ('oneclient_docker_build', 'oc-docker-build-list.json'),
    'rest_cli': ('rest_cli_docker_build', 'rest-cli-docker-build-report.json')
}


def config_file(relative_file_path):
    """Returns a path to file located in {test_name}_data directory, where
    {test_name} is name of the test module that called this function.
    example: using test_utils.config_file('my_file') in my_test.py will return
    'tests/my_test_data/my_file'
    """
    caller = inspect.stack()[1]
    caller_mod = inspect.getmodule(caller[0])
    caller_mod_file_path = caller_mod.__file__
    return '{0}_data/{1}'.format(caller_mod_file_path.rstrip('.py'),
                                 relative_file_path)


def get_file_name(file_path):
    """Returns name of file, basing on file_path.
    Name is acquired by removing parent directories from file_path and stripping
    extension.
    i.e. get_file_name("dir1/dir2/file.py") will return "file"
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def get_logdir_name(root_dir, test_name):
    """Returns path to logs directory
    i.e. get_logdir_name("tests/mytest", "test1") will return
    "tests/mytest/test1.<timestamp>"
    """
    timestamp = str(time.time())
    return os.path.join(root_dir, ".".join([test_name, timestamp]))


def make_logdir(root_dir, test_name):
    """Creates logdir if it doesn't exist."""
    name = get_logdir_name(root_dir, test_name)
    if not os.path.exists(name):
        os.makedirs(name)
    return name


def get_json_files(dir, relative=False):
    """Gets all .json files from given directory
    Returns list of files' absolute paths"""
    jsons = []
    for file in os.listdir(dir):
        if file.endswith('.json'):
            if not relative:
                jsons.append(os.path.join(dir, file))
            else:
                jsons.append(file)
    return jsons


def save_log_to_file(file_path, log):
    """Saves log to file pointed by file_path"""
    f = open(file_path, 'w')
    f.write(log)
    f.close()


def get_module(name):
    """Returns module object"""
    return sys.modules[name]


def get_function(module, function_name):
    """Returns function object from given module"""
    return getattr(module, function_name)


def ensure_json(file):
    """Ensures that file has .json extension."""
    if os.path.splitext(file)[1] != ".json":
        file = ".".join([file, "json"])
    return file


def ensure_yaml(file):
    """Ensures that file has .yaml extension."""
    if os.path.splitext(file)[1] != '.yaml':
        file = '.'.join([file, 'yaml'])
    return file


def absolute_path_to_env_file(dir, file):
    """Returns absolute path to environment file from dir. Ensures that file
    has .json extension"""
    return os.path.join(dir, ensure_yaml(file))


def escape_path(path):
    """Returns path with escaped space and apostrophe"""
    return path.replace("'", "\\'").replace(' ', '\ ')


def get_first_path_element(path):
    """Returns first element in path"""
    return next(elem for elem in path.split(os.path.sep) if elem)


def read_image_from_artifact(service, fail_on_error=False):
    """Returns service image from artifact downloaded by onenv pull_artifact"""
    sources_info_path = os.path.join(os.getcwd(), 'sources_info.yaml')
    try:
        with open(sources_info_path, 'r') as sources_info_file:
            sources_info = yaml.load(sources_info_file, yaml.Loader)
            (plan_name, file_name) = SERVICE_TO_ARTIFACT_PLAN[service]
            file_path = sources_info[plan_name]['extracted_sources_path']
            abs_file_path = os.path.join(file_path, file_name)
            with open(abs_file_path, 'r') as images_cfg_file:
                image = json.load(images_cfg_file).get('git-commit')
                return image
    except (FileNotFoundError, KeyError) as e:
        if fail_on_error:
            print("[ERROR] Error when reading image for {} from sources info file {}: {}.".format(
                service, sources_info_path, e))
            raise e
        print("[WARNING] Could not read image for '{}' from sources info file '{}': {}. Image "
              "provided in scenario yaml will be used.".format(service, sources_info_path, e))
        return None
