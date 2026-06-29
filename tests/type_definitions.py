"""Shared types for acceptance tests."""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections import defaultdict
from collections.abc import Callable, MutableMapping
from typing import (
    Any,
    Literal,
    Optional,
    ParamSpec,
    Protocol,
    TypedDict,
    TypeVar,
)

from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from tests.utils.user_utils import User

type JsonValue = Optional[
    str | int | float | bool | list["JsonValue"] | dict[str, "JsonValue"]
]
type Capabilities = dict[str, JsonValue]


class HostPanel(TypedDict):
    hostname: str


class HostDescription(TypedDict, total=False):
    pod_name: str
    service_type: str
    name: str
    hostname: str
    ip: str
    container_id: str
    provider_host: str
    panel: HostPanel


type Hosts = dict[str, HostDescription]
type TestConfig = dict[str, JsonValue]
type SeleniumDrivers = dict[str, WebDriver]
type SeleniumFixtureState = dict[str, WebDriver | FixtureRequest]
type Users = dict[str, User]
type Storages = MutableMapping[str, MutableMapping[str, str]]
type Tokens = dict[str, dict[str, str]]
type WorkflowExecutions = dict[str, dict[str, object]]
type PreviousEnv = dict[str, str | bool]
type TestType = Literal[
    "gui", "oneclient", "mixed", "performance", "upgrade"
]
type WebDriverConfigurator = Callable[[WebDriver], WebDriver]
FactoryParams = ParamSpec("FactoryParams")
FactoryResult = TypeVar("FactoryResult")
FactoryResult_co = TypeVar("FactoryResult_co", covariant=True)
type FactoryFunction[**FactoryParams, FactoryResult] = Callable[
    FactoryParams, FactoryResult
]


class FactoryCallable(Protocol[FactoryParams, FactoryResult_co]):
    def __call__(
        self, *args: FactoryParams.args, **kwargs: FactoryParams.kwargs
    ) -> FactoryResult_co: ...

    def get_instance(
        self, *args: FactoryParams.args, **kwargs: FactoryParams.kwargs
    ) -> FactoryResult_co: ...


type WebDriverFactory = FactoryCallable[[], WebDriver]


class HookOutcome(Protocol):
    def get_result(self) -> object: ...


class LogEntry(TypedDict):
    timestamp: int
    level: str
    message: str


class WebDriverWithAllLogs(Protocol):
    def get_all_logs(self) -> defaultdict[str, list[LogEntry]]: ...


class EnvDesc(TypedDict, total=False):
    scenario: str
    patch: str
    entities_config: str
