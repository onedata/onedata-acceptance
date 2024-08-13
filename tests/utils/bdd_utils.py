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
        pytest_bdd_given(name, converters, target_fixture, stacklevel=2)
    ]
    return _create_decorator(given, wrappers)


def when(name, converters=None):
    wrappers = [
        sanitize_arguments,
        pytest_bdd_when(name, converters, stacklevel=2)
    ]
    return _create_decorator(when, wrappers)


def then(name, converters=None):
    wrappers = [
        sanitize_arguments,
        pytest_bdd_then(name, converters, stacklevel=2)
    ]
    return _create_decorator(then, wrappers)


def wt(name, converters=None):
    wrappers = [
        sanitize_arguments,
        pytest_bdd_when(name, converters, stacklevel=2),
        pytest_bdd_then(name, converters, stacklevel=2)
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


def _create_decorator(wrapped, wrappers):

    @wraps(wrapped)
    def decorator(original_fun):
        fun = original_fun
        for wrapper in wrappers:
            fun = wrapper(fun)

        return fun

    return decorator
