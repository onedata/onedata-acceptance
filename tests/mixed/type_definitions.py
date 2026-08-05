"""Shared types for mixed acceptance test helpers and fixtures."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Callable, Iterable, Mapping, MutableMapping, Sequence
from typing import Any, Literal, NotRequired, Optional, TypedDict

from tests.type_definitions import JsonObject, JsonValue


type IdMap = Mapping[str, str]
type MutableIdMap = MutableMapping[str, str]
type HostsConfig = Mapping[str, Mapping[str, str]]
type Spaces = Mapping[str, str]
type MutableSpaces = MutableMapping[str, str]
type GroupMap = Mapping[str, str]
type SpaceMap = Mapping[str, str]

type Mailbox = MutableMapping[str, str]
type UserTmpMemory = MutableMapping[str, Mailbox]
type RestOnezoneTmpMemory = MutableMapping[str, UserTmpMemory]
type SpaceManagementTmpMemoryEntry = MutableMapping[str, Mailbox | str]
type SpaceManagementTmpMemory = MutableMapping[str, SpaceManagementTmpMemoryEntry]
type SpecialDirsTmpMemory = MutableMapping[Any, dict[str, str]]

type InputFiles = list[str]
type ExecutionResult = tuple[list[JsonObject], InputFiles | list[InputFiles]]
type ResolveId = Callable[[str], str]
type UploadFile = Callable[[str, str], None]

type Content = Optional[Iterable["ContentItem"]]
type ContentItem = str | Mapping[str, Content]
type AclEntry = MutableMapping[str, str]
type Acl = list[AclEntry]
type IsDir = Callable[[str], bool]
type ListDir = Callable[[str], Sequence[str]]
type AssertFileContent = Callable[[str, str], None]

type ResolverResult = str | list[str]
type Resolver = Callable[[str], ResolverResult]

type FileAttrs = dict[str, str | int]
type EventResult = str | tuple[str, float] | dict[str, FileAttrs]
type ExpectedAttrs = Mapping[str, Optional[str | int]]

type MappingValue = Optional[str | int]

UserMapping = TypedDict(
    "UserMapping",
    {
        "storage uid": MappingValue,
        "display uid": NotRequired[MappingValue],
    },
)
SpaceMapping = TypedDict(
    "SpaceMapping",
    {
        "space POSIX storage defaults": MappingValue,
        "space display defaults": NotRequired[MappingValue],
    },
)


class StorageMappings(TypedDict):
    type: str
    users: NotRequired[dict[str, UserMapping]]
    spaces: NotRequired[dict[str, SpaceMapping]]


type LumaMappings = dict[str, dict[str, StorageMappings]]


class SpaceAlias(TypedDict):
    name: str
    sid: str


type SpaceAliases = MutableMapping[str, SpaceAlias]


class UserMemory(TypedDict):
    mailbox: MutableMapping[str, str]


type DataAdvancedTmpMemory = MutableMapping[str, UserMemory]

type DatasetSubtree = list[str | dict[str, "DatasetSubtree"]]
type DatasetTree = list[dict[str, DatasetSubtree]]

type ArchiveTmpMemory = MutableMapping[str, str]
type ArchiveConfigValue = str | MutableMapping[str, str]
type ArchiveConfig = dict[str, ArchiveConfigValue]

type TokenValue = JsonValue | list[str] | list["TokenCaveat"] | dict[str, TokenValue]
type ConfigMap = Mapping[str, TokenValue]
type TokenCaveat = dict[str, TokenValue]
type TokenConfig = dict[str, TokenValue]

PrivilegeGroupConfig = TypedDict(
    "PrivilegeGroupConfig",
    {
        "granted": bool | Literal["Partially"],
        "privilege subtypes": NotRequired[Mapping[str, bool]],
    },
)
