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
import sys
from functools import wraps
from types import CodeType

from tests.utils.bdd_utils import wt, parsers

TIME_ATTR_MAPPING = {
    'access': 'atime',
    'modification': 'mtime',
    'status-change': 'ctime'
}


def list_parser(list):
    return [el.strip() for el in list.strip('[]').split(',') if el != '']


def make_arg_list(arg):
    return '[' + arg + ']'


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


@wt(parsers.re('if (?P<client>.+?) is web GUI, (?P<user>.+?) is idle for '
               r'(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds?'))
def wait_given_time_if_web_gui(client, seconds):
    if client == 'web GUI':
        wait_given_time(seconds)


@wt(parsers.re('user of (?P<browser_id>.+?) is idle for '
               '(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds?'))
@wt(parsers.re('(?P<user>.+?) is idle for '
               '(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds?'))
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
    elif comparator == 'not less' or comparator == 'greater or equal':
        return val1 >= val2
    else:
        raise ValueError(f'Wrong argument comparator to function compare')
