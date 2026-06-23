"""This module provides utility functions for bdd tests."""

# pylint: disable=invalid-name,redefined-outer-name

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import inspect
from collections.abc import Callable, Iterable, Mapping
from functools import wraps
from types import NoneType, UnionType
from typing import (
    Any,
    Literal,
    Optional,
    Protocol,
    TypeAliasType,
    Union,
    cast,
    get_args,
    get_origin,
    is_typeddict,
)

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

type Converter = Callable[[str], object]
type Converters = Mapping[str, Converter]
type StepFunction[**params, return_type] = Callable[params, return_type]


class StepDecorator(Protocol):
    def __call__[**params, return_type](
        self, fun: StepFunction[params, return_type]
    ) -> StepFunction[params, return_type]: ...


def _get_runtime_cast_target(ann: object) -> Optional[type]:
    while isinstance(ann, TypeAliasType):
        ann = ann.__value__

    if (
        ann is Any
        or is_typeddict(ann)
        or (
            getattr(ann, "_is_protocol", False)
            and not getattr(ann, "_is_runtime_protocol", False)
        )
    ):
        return None

    origin = get_origin(ann)
    if origin in (Union, UnionType):
        possible_types = tuple(arg for arg in get_args(ann) if arg is not NoneType)
        if len(possible_types) == 1:
            return _get_runtime_cast_target(possible_types[0])
        return None

    if origin is Literal:
        return None

    target_type = ann if origin is None else origin
    return cast(Optional[type], target_type if isinstance(target_type, type) else None)


def given(
    name: object,
    fixture: Optional[object] = None,
    converters: Optional[Converters] = None,
    scope: str = "function",
    target_fixture: Optional[str] = None,
) -> StepDecorator:
    wrappers = [
        sanitize_arguments,
        pytest_bdd_given(name, converters, target_fixture, stacklevel=2),
    ]
    _ = (fixture, scope)
    return _create_decorator(given, wrappers)


def when(name: object, converters: Optional[Converters] = None) -> StepDecorator:
    wrappers = [sanitize_arguments, pytest_bdd_when(name, converters, stacklevel=2)]
    return _create_decorator(when, wrappers)


def then(name: object, converters: Optional[Converters] = None) -> StepDecorator:
    wrappers = [sanitize_arguments, pytest_bdd_then(name, converters, stacklevel=2)]
    return _create_decorator(then, wrappers)


def wt(name: object, converters: Optional[Converters] = None) -> StepDecorator:
    wrappers = [
        sanitize_arguments,
        pytest_bdd_when(name, converters, stacklevel=2),
        pytest_bdd_then(name, converters, stacklevel=2),
    ]
    return _create_decorator(wt, wrappers)


def sanitize_arguments[**params, return_type](
    fun: StepFunction[params, return_type],
) -> StepFunction[params, return_type]:
    sig = inspect.signature(fun)
    parameters = sig.parameters
    is_gen = inspect.isgeneratorfunction(fun)

    def _cast_arguments(
        args: tuple[object, ...], kwargs: dict[str, object]
    ) -> inspect.BoundArguments:
        ba = sig.bind(*args, **kwargs)
        ba.apply_defaults()

        for param in parameters.values():
            ann = param.annotation
            if ann is not inspect.Parameter.empty and param.name in ba.arguments:
                target_type = _get_runtime_cast_target(ann)
                if target_type is None:
                    continue

                value = ba.arguments[param.name]
                if not isinstance(value, str):
                    continue

                try:
                    if not isinstance(value, target_type):
                        ba.arguments[param.name] = target_type(value)
                except Exception as ex:
                    msg = f"Cannot cast '{param.name}' <{value}> to {ann}"
                    raise ValueError(msg) from ex

        return ba

    if is_gen:

        @wraps(fun)
        def wrapper(*args: object, **kwargs: object) -> Iterable[object]:
            ba = _cast_arguments(args, kwargs)
            yield from cast(Iterable[object], fun(*ba.args, **ba.kwargs))

    else:

        @wraps(fun)
        def wrapper(*args: object, **kwargs: object) -> object:
            ba = _cast_arguments(args, kwargs)
            return fun(*ba.args, **ba.kwargs)

    return cast(StepFunction[params, return_type], wrapper)


def _create_decorator(
    wrapped: Callable[..., object], wrappers: list[StepDecorator]
) -> StepDecorator:

    @wraps(wrapped)
    def decorator[**params, return_type](
        original_fun: StepFunction[params, return_type],
    ) -> StepFunction[params, return_type]:
        fun = original_fun
        for wrapper in wrappers:
            fun = wrapper(fun)

        return fun

    return cast(StepDecorator, decorator)


# pylint: disable=line-too-long
scenarios_to_rerun = {
    "test_user_resume_workflow_execution_after_pausing_execution_of_created_workflow_while_lane_had_preparing_status",
    "test_user_sees_status_cancelled_in_lane1_and_unscheduled_in_lane2_after_cancelling_execution_of_uploaded_workflowwithsleeptwolanes_workflow",
    "test_user_sees_status_status_in_lane2_after_stopping_execution_of_uploaded_workflowwithsleeptwolanes_workflow",
}
