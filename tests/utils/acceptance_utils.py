"""This module implements some common basic functions and functionality for
acceptance tests of onedata.
"""
__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

from pytest_bdd import parsers
from pytest_bdd import when, then
from functools import wraps
import six
import inspect
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
