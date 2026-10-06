"""Enums shared by GUI tests and utilities."""

from enum import Enum, StrEnum


class OnedataService(Enum):
    WORKERS = "workers"
    ONES3 = "ones3"


class OneS3ServiceState(StrEnum):
    STOPPED = "stopped"
    STARTING = "starting"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    STOPPING = "stopping"
    MISSING = "missing"


class TransferState(Enum):
    ENDED = "ended"
    ONGOING = "ongoing"
    WAITING = "waiting"


class SpecialDir(Enum):
    ARCHIVE_DIR = "archive directory"
    DATASET_ARCHIVES_DIR = "dataset archives directory"
    OPENED_DELETED_FILES_DIR = "opened deleted files directory"
    SHARE_CONTAINER = "share container"
    SPACE_ARCHIVES_DIR = "space archives directory"
    SPACE_DIR = "space directory"
    TMP_DIR = "tmp directory"
    TRASH_DIR = "trash directory"
    USER_ROOT_DIR = "user root directory"


class FileAttr(Enum):
    ACL = "acl"
    ACTIVE_PERMISSIONS_TYPE = "activePermissionsType"
    AGGREGATE_QOS_STATUS = "aggregateQosStatus"
    ARCHIVE_RECALL_ROOT_FILE_ID = "archiveRecallRootFileId"
    ATIME = "atime"
    CONFLICTING_NAME = "conflictingName"
    CREATION_TIME = "creationTime"
    CTIME = "ctime"
    DIRECT_SHARE_IDS = "directShareIds"
    DISPLAY_GID = "displayGid"
    DISPLAY_UID = "displayUid"
    EFF_DATASET_INHERITANCE_PATH = "effDatasetInheritancePath"
    EFF_DATASET_PROTECTION_FLAGS = "effDatasetProtectionFlags"
    EFF_PROTECTION_FLAGS = "effProtectionFlags"
    EFF_QOS_INHERITANCE_PATH = "effQosInheritancePath"
    FILE_ID = "fileId"
    HARDLINK_COUNT = "hardlinkCount"
    HAS_CUSTOM_METADATA = "hasCustomMetadata"
    HAS_JSON_METADATA = "hasJsonMetadata"
    INDEX = "index"
    IS_FULLY_REPLICATED_LOCALLY = "isFullyReplicatedLocally"
    JSON_METADATA = "jsonMetadata"
    LOCAL_REPLICATION_RATE = "localReplicationRate"
    MTIME = "mtime"
    NAME = "name"
    ORIGIN_PROVIDER_ID = "originProviderId"
    OWNER_USER_ID = "ownerUserId"
    PARENT_FILE_ID = "parentFileId"
    PATH = "path"
    POSIX_PERMISSIONS = "posixPermissions"
    SIZE = "size"
    SYMLINK_VALUE = "symlinkValue"
    TYPE = "type"
    XATTR_KEY = "xattr.key"


class ListElement(Enum):
    """
    Represents supported list-like element types available on pages.

    Each enum value corresponds to a logical list of elements that can be
    displayed in the GUI, for example spaces, groups, files, tokens or workflows.

    This enum should be used whenever code needs to refer to a specific type of
    list in a page-independent way, instead of passing raw strings such as
    "spaces", "groups headers" or "shares sidebar".

    The enum values are used to build attribute names dynamically, for example:
        ListElement.SPACES -> "spaces" -> "spaces_list"
        ListElement.GROUPS_HEADERS -> "groups headers" -> "groups_headers_list"

    Use this enum when:
    - selecting which elements list should be read from a page,
    - calling generic helpers such as get_visible_items_list(),
    - avoiding hardcoded string literals in step definitions or page utilities,
    - ensuring that only supported list types are passed to generic list-handling code.
    """

    SHARES = "shares"
    SHARES_SIDEBAR = "shares sidebar"
    GROUPS = "groups"
    GROUPS_HEADERS = "groups headers"
    SPACES = "spaces"
    SPACES_HEADERS = "spaces headers"
    FILES = "files"
    UPLOADS = "uploads"
    PROVIDERS = "providers"
    HARVESTERS = "harvesters"
    TOKENS = "tokens"
    AUTOMATIONS = "automations"
    LAMBDAS = "lambdas"
    WORKFLOWS = "workflows"


class HostPattern(Enum):
    PROVIDER_PANEL = r"oneprovider-[0-9]+ provider panel"
    ZONE_PANEL = r"(?:onezone zone panel|[Oo]nezone panel)"
    ZONE = r"[Oo]nezone"
    ONEPANEL_EMERGENCY = r"emergency interface of Onepanel"
    ONEZONE_EMERGENCY = r"emergency interface of Onezone"
    PROVIDER_NODE = r"node[0-9]+ of oneprovider-[0-9]+ provider panel"
