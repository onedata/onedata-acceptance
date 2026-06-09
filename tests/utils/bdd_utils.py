"""This module provides utility functions for bdd tests."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, get_origin

from pytest_bdd import given as pytest_bdd_given
from pytest_bdd import parsers, scenario, scenarios
from pytest_bdd import then as pytest_bdd_then
from pytest_bdd import when as pytest_bdd_when

__all__ = [
    "scenario",
    "scenarios",
    "parsers",
    "given",
    "when",
    "then",
    "wt",
    "scenarios_to_rerun",
]

StepFunction = Callable[..., Any]
StepDecorator = Callable[[StepFunction], StepFunction]


def given(
    name: object,
    fixture: Any = None,
    converters: Any = None,
    scope: str = "function",
    target_fixture: Any = None,
) -> StepDecorator:  # pylint: disable=unused-argument
    wrappers = [
        sanitize_arguments,
        pytest_bdd_given(name, converters, target_fixture, stacklevel=2),
    ]
    return _create_decorator(given, wrappers)


def when(name: object, converters: Any = None) -> StepDecorator:
    wrappers = [sanitize_arguments, pytest_bdd_when(name, converters, stacklevel=2)]
    return _create_decorator(when, wrappers)


def then(name: object, converters: Any = None) -> StepDecorator:
    wrappers = [sanitize_arguments, pytest_bdd_then(name, converters, stacklevel=2)]
    return _create_decorator(then, wrappers)


def wt(name: object, converters: Any = None) -> StepDecorator:
    wrappers = [
        sanitize_arguments,
        pytest_bdd_when(name, converters, stacklevel=2),
        pytest_bdd_then(name, converters, stacklevel=2),
    ]
    return _create_decorator(wt, wrappers)


def sanitize_arguments(fun: StepFunction) -> StepFunction:
    sig = inspect.signature(fun)
    parameters = sig.parameters
    is_gen = inspect.isgeneratorfunction(fun)

    def _cast_arguments(
        args: tuple[Any, ...], kwargs: dict[str, Any]
    ) -> inspect.BoundArguments:
        ba = sig.bind(*args, **kwargs)
        ba.apply_defaults()

        for param in parameters.values():
            ann = param.annotation
            if ann is not inspect.Parameter.empty and param.name in ba.arguments:
                value = ba.arguments[param.name]
                try:
                    origin = get_origin(ann)
                    target_type = ann if origin is None else origin
                    if not isinstance(value, target_type):
                        ba.arguments[param.name] = target_type(value)
                except Exception as ex:
                    msg = f"Cannot cast '{param.name}' <{value}> to {ann}"
                    raise ValueError(msg) from ex

        return ba

    if is_gen:

        @wraps(fun)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            ba = _cast_arguments(args, kwargs)
            yield from fun(*ba.args, **ba.kwargs)

    else:

        @wraps(fun)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            ba = _cast_arguments(args, kwargs)
            return fun(*ba.args, **ba.kwargs)

    return wrapper


def _create_decorator(
    wrapped: StepFunction, wrappers: list[StepDecorator]
) -> StepDecorator:

    @wraps(wrapped)
    def decorator(original_fun: StepFunction) -> StepFunction:
        fun = original_fun
        for wrapper in wrappers:
            fun = wrapper(fun)

        return fun

    return decorator


# pylint: disable=line-too-long
scenarios_to_rerun = {
    "test_user_resume_workflow_execution_after_pausing_execution_of_created_workflow_while_lane_had_preparing_status",
    "test_user_sees_status_cancelled_in_lane1_and_unscheduled_in_lane2_after_cancelling_execution_of_uploaded_workflowwithsleeptwolanes_workflow",
    "test_user_sees_status_status_in_lane2_after_stopping_execution_of_uploaded_workflowwithsleeptwolanes_workflow",
}
