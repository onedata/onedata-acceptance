"""This module implements some common basic functions and functionality for
acceptance tests of onedata.
"""
__author__ = "Jakub Kudzia, Piotr Ociepka, Michal Stanisz"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time
import inspect
import six
import subprocess
from functools import wraps
from types import CodeType

from pytest_bdd import when, then, parsers


TIME_ATTR_MAPPING = {
    'access': 'atime',
    'modification': 'mtime',
    'status-change': 'ctime'
}


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


@wt(parsers.re('user of (?P<browser_id>.+?) is idle for '
               '(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds'))
@wt(parsers.re('user .* waits for (?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) '
               'seconds'))
@wt(parsers.re('(?P<user>.+?) waits (?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) '
               'seconds?'))
def wait_given_time(seconds):
    time.sleep(float(seconds))


@wt(parsers.parse('last operation by {user} succeeds'))
def success(user, users):
    assert not users[user].last_operation_failed


@wt(parsers.parse('last operation by {user} fails'))
def failure(user, users):
    assert users[user].last_operation_failed


def time_attr(parameter, prefix='st'):
    return '{}_{}'.format(prefix, TIME_ATTR_MAPPING[parameter])


def compare(val1, val2, comparator):
    if comparator == 'equal':
        return val1 == val2
    elif comparator == 'not equal':
        return val1 != val2
    elif comparator == 'greater':
        return val1 > val2
    elif comparator == 'less':
        return val1 < val2
    elif comparator == 'not greater':
        return val1 <= val2
    elif comparator == 'not less':
        return val1 >= val2
    else:
        raise ValueError('Wrong argument comparator to function compare')
