"""This module provides utility functions for bdd tests."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import inspect
import sys
from functools import wraps
from types import CodeType

from pytest_bdd import (scenario,
                        scenarios,
                        parsers,
                        given as pytest_bdd_given,
                        when as pytest_bdd_when,
                        then as pytest_bdd_then)


__all__ = ['scenario', 'scenarios', 'parsers', 'given', 'when', 'then', 'wt']


def given(name, fixture=None, converters=None, scope='function',
          target_fixture=None):
    wrappers = [
        sanitize_arguments,
        pytest_bdd_given(name, fixture, converters, scope, target_fixture)
    ]
    return _create_decorator(given, wrappers)


def when(name, converters=None):
    wrappers = [
        sanitize_arguments,
        pytest_bdd_when(name, converters)
    ]
    return _create_decorator(when, wrappers)


def then(name, converters=None):
    wrappers = [
        sanitize_arguments,
        pytest_bdd_then(name, converters)
    ]
    return _create_decorator(then, wrappers)


def wt(name, converters=None):
    wrappers = [
        sanitize_arguments,
        pytest_bdd_when(name, converters),
        pytest_bdd_then(name, converters)
    ]
    return _create_decorator(wt, wrappers)


def sanitize_arguments(fun):
    sig = inspect.signature(fun)
    parameters = sig.parameters

    @wraps(fun)
    def wrapper(*args, **kwargs):
        ba = sig.bind(*args, **kwargs)
        ba.apply_defaults()

        for param in parameters.values():
            ann = param.annotation
            if ann is not inspect.Parameter.empty:
                value = ba.arguments[param.name]
                try:
                    if not isinstance(value, ann):
                        ba.arguments[param.name] = ann(value)
                except Exception as ex:
                    msg = f"Cannot cast '{param.name}' <{value}> to {ann}"
                    raise ValueError(msg) from ex

        return fun(*ba.args, **ba.kwargs)

    return wrapper


_CO_ATTRS = [
    'co_argcount',
    'co_kwonlyargcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_lnotab',
    'co_freevars',
    'co_cellvars'
]


def _create_decorator(wrapped, wrappers):
    """Creates decorator that can be used in other modules.

    Due to limitations of pytest_bdd plugin (step decorators mess with decorated
    function's module dictionary) it is necessary to define decorators, that
    internally calls pytest_bdd decorators, in the same module as decorated
    function.
    This is impractical (copy pasting the same decorator in every module) and
    can be avoided by defining decorator once and before executing it for
    decorated function modifying it's code object such that it would be
    virtually defined in decorated function module (modification of
    'co_filename' attr of code object).
    """

    @wraps(wrapped)
    def decorator(original_fun):
        module = inspect.getmodule(original_fun)

        def virtual_decorator():
            fun = original_fun
            for wrapper in wrappers:
                fun = wrapper(fun)

            return fun

        code = virtual_decorator.__code__

        if sys.version_info.minor >= 8:
            virtual_decorator.__code__ = code.replace(co_filename = module.__file__)
        else:
            code_attrs = [getattr(code, attr) for attr in _CO_ATTRS]
            code_attrs[_CO_ATTRS.index('co_filename')] = module.__file__
            virtual_decorator.__code__ = CodeType(*code_attrs)

        virtual_decorator.__module__ = module.__name__

        return virtual_decorator()

    return decorator
