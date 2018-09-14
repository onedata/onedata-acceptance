"""This module implements some common basic functions and functionality for
acceptance tests of onedata.
"""
__author__ = "Jakub Kudzia, Piotr Ociepka, Michal Stanisz"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import six
import inspect
import subprocess
import json
import re
from pytest_bdd import when, then
from functools import wraps
from types import CodeType


def list_parser(list):
    return [el.strip() for el in list.strip('[]').split(',') if el != '']


def make_arg_list(arg):
    return '[' + arg + ']'


CO_ARG_NAMES = [
    'co_argcount', 'co_nlocals', 'co_stacksize', 'co_flags', 'co_code',
    'co_consts', 'co_names', 'co_varnames', 'co_filename', 'co_name',
    'co_firstlineno', 'co_lnotab', 'co_freevars', 'co_cellvars',
]
if six.PY3:
    CO_ARG_NAMES.insert(1, 'co_kwonlyargcount')


def wt(name, converters=None):
    when_decorator = when(name, converters)
    then_decorator = then(name, converters)

    @wraps(wt)
    def decorator(func):

        def tmp_fun():
            return then_decorator(when_decorator(func))

        mod = inspect.getmodule(func)
        tmp_fun.__module__ = mod.__name__
        code = tmp_fun.__code__ if six.PY3 else tmp_fun.func_code
        args = [mod.__file__ if arg == 'co_filename' else getattr(code, arg)
                for arg in CO_ARG_NAMES]
        new_code = CodeType(*args)
        if six.PY3:
            tmp_fun.__code__ = new_code
        else:
            tmp_fun.func_code = new_code
        return tmp_fun()

    return decorator


def execute_command(cmd, error=None, should_fail=False):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output, err = process.communicate()
    if (process.returncode != 0) ^ should_fail:
        raise RuntimeError('{}: {}; {}'.format(error, err, output) if error
                           else 'Command did not fail: {}, Err: {}, Output: {}'
                           .format(' '.join(cmd), err, output)
                           if should_fail else 'Error when executing command '
                           '"{}": {}; {}'.format(' '.join(cmd), err, output))
    return output


# TODO use onenv functions after change to python3
def get_pod_names_matching_regexp(regexp):
    cmd = ['kubectl', 'get', 'pods'] + \
          ['-o', 'json', '--field-selector=status.phase==Running']
    raw_json = execute_command(cmd, error='Error when listing pods')
    parsed_json = json.loads(raw_json)
    pods_names = [pod['metadata']['name'] for pod in parsed_json['items']]
    return [name for name in pods_names if re.search(regexp, name)]


def get_pod_ip(pod_name):
    cmd = ['kubectl', 'get'] + ['pod', pod_name, '-o', 'json']
    raw_json = execute_command(cmd)
    parsed_json = json.loads(raw_json)
    return parsed_json['status']['podIP']
