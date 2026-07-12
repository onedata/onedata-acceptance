"""Generic GUI testing utils - mainly helpers and extensions for Selenium."""

__author__ = "Jakub Liput, Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import json
import os
import re
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from enum import Enum
from itertools import islice
from time import sleep
from typing import Literal, Optional, TypeVar, cast, overload

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from tests import gui
from tests.gui.type_definitions import WebElemRoot
from tests.type_definitions import JsonValue

T = TypeVar("T")

# RE_URL regexp is matched as shown below:
#
# https://172.18.0.8/#/onedata/data/small_space/g2gDZAAEZ3VpZG0AAAAkZzJnQ
# \       \        /   \     / \  / \         /                        /
#  \        domain      \   /   tab  \___id__/                        /
#   \            /      access                                       /
#    \_base_url_/         \_________________method__________________/

RE_URL = re.compile(
    r"(?P<base_url>https?://(?P<domain>.*?)"
    r"(/(?P<where>[^/]*)/(?P<cluster>[^/]*))?)"
    r"(/i#)?(?P<method>/(?P<access>[^/]*)/(?P<tab>[^/]*)"
    r"(/(?P<id>[^/]*).*)?)"
)


def parse_url(url: str) -> re.Match[str]:
    match = RE_URL.match(url)
    if match is None:
        raise ValueError(f"Invalid URL: {url}")
    return match


def go_to_relative_url(selenium: WebDriver, relative_url: str) -> None:
    match = parse_url(selenium.current_url)
    new_url = match.group("base_url") + relative_url
    selenium.get(new_url)


@overload
def parse_seq(
    seq: str,
    pattern: Optional[str] = None,
    separator: Optional[str] = None,
) -> list[str]: ...


@overload
def parse_seq(
    seq: str,
    pattern: Optional[str] = None,
    separator: Optional[str] = None,
    *,
    default: Callable[[str], T],
) -> list[T]: ...


@overload
def parse_seq(
    seq: str,
    pattern: Optional[str],
    separator: Optional[str],
    default: Callable[[str], T],
) -> list[T]: ...


def parse_seq(
    seq: str,
    pattern: Optional[str] = None,
    separator: Optional[str] = None,
    default: Callable[[str], T] = cast(Callable[[str], T], str),
) -> list[T]:
    if pattern is not None:
        return [default(el.group()) for el in re.finditer(pattern, seq)]
    separator = "," if separator is None else separator
    return [
        default(el.strip().strip('"'))
        for el in seq.strip("[]").split(separator)
        if el != ""
    ]


def upload_file_path(file_name: str) -> str:
    """Resolve an absolute path for file with name file_name stored
    in upload_files dir
    """
    return os.path.join(
        os.path.dirname(os.path.abspath(gui.__file__)),
        "upload_files",
        file_name,
    )


def upload_workflow_path(workflow_name: Optional[str] = None) -> str:
    """Resolve an absolute path for workflow file with name workflow_name
    stored in automation-examples submodule
    """
    if workflow_name:
        return os.path.abspath(
            os.path.join(
                os.path.dirname(gui.__file__),
                "..",
                "..",
                "automation-examples",
                "workflows",
                workflow_name,
            )
        )
    return os.path.abspath(
        os.path.join(
            os.path.dirname(gui.__file__),
            "..",
            "..",
            "automation-examples",
            "workflows",
        )
    )


def upload_lambda_path(lambda_name: Optional[str]) -> str:
    """Resolve an absolute path for lambda dump file with name lambda_name
    stored in automation-examples submodule
    """
    if lambda_name:
        return os.path.abspath(
            os.path.join(
                os.path.dirname(gui.__file__),
                "..",
                "..",
                "automation-examples",
                "lambdas",
                lambda_name,
            )
        )
    return os.path.abspath(
        os.path.join(
            os.path.dirname(gui.__file__),
            "..",
            "..",
            "automation-examples",
            "lambdas",
        )
    )


def strip_path(path_string: str, separator: str = "/") -> str:
    """Strips string from whitespaces inside file path. Useful for file
     paths rendered
    in DOM which contains `\\n` characters in `innerText`.
    """
    return separator.join(
        [path_item.strip() for path_item in path_string.split(separator)]
    )


@contextmanager
def implicit_wait(
    driver: WebDriver, timeout: int | float, prev_timeout: int | float
) -> Iterator[None]:
    driver.implicitly_wait(timeout)
    try:
        yield
    finally:
        driver.implicitly_wait(prev_timeout)


def iter_ahead(iterable: Iterable[T]) -> Iterator[tuple[T, T]]:
    read_ahead = iter(iterable)
    next(read_ahead, None)
    for item, next_item in zip(iterable, read_ahead):
        yield item, next_item


def find_web_elem(
    web_elem_root: WebElemRoot,
    css_sel: str,
    err_msg: str | Callable[[], str],
    scroll: bool = True,
) -> WebElement:
    try:
        if scroll:
            _scroll_to_css_sel(web_elem_root, css_sel)
        item = web_elem_root.find_element(By.CSS_SELECTOR, css_sel)
    except NoSuchElementException as exc:
        if callable(err_msg):
            err_msg = err_msg()
        raise RuntimeError(err_msg) from exc
    return item


def find_web_elem_with_text(
    web_elem_root: WebElemRoot,
    css_sel: str,
    text: str,
    err_msg: str | Callable[[], str],
    scroll: bool = True,
) -> WebElement:
    items = web_elem_root.find_elements(By.CSS_SELECTOR, css_sel)
    if scroll:
        _scroll_to_css_sel(web_elem_root, css_sel)
    for item in items:
        if item.text.lower() == text.lower():
            return item
    if callable(err_msg):
        err_msg = err_msg()
    raise RuntimeError(f'Css element with "{text}" text not found. {err_msg}')


def click_on_web_elem(
    driver: WebDriver,
    web_elem: WebElement,
    err_msg: str | Callable[[], str],
    delay: bool | float = True,
) -> None:
    disabled = "disabled" in web_elem.get_attribute("class")
    # scroll to make the element visible
    if not web_elem.is_displayed():
        _ = web_elem.location_once_scrolled_into_view
    if web_elem.is_enabled() and web_elem.is_displayed() and not disabled:
        # TODO VFS-7484 make optional sleep and localize only those tests
        #  that need it or find better alternative
        # currently checking if elem is enabled not always work
        # (probably after striping disabled from web elem
        # elem is not immediately clickable)
        if delay:
            sleep(delay if isinstance(delay, float) else 0.25)
        action = ActionChains(driver)
        action.move_to_element(web_elem).click_and_hold(web_elem).release(web_elem)
        action.perform()
    else:
        if callable(err_msg):
            err_msg = err_msg()
        raise RuntimeError(err_msg)


def _scroll_to_css_sel(web_elem_root: WebElemRoot, css_sel: str) -> None:
    driver = getattr(web_elem_root, "parent", web_elem_root)
    driver.execute_script(
        "var el = (typeof $ === 'function' ? "
        f"$('{css_sel}')[0] : "
        f"document.querySelector('{css_sel}')); "
        "el && el.scrollIntoView(true);"
    )


@contextmanager
def suppress(*exceptions: type[BaseException]) -> Iterator[None]:
    try:
        yield
    except exceptions:
        pass


@contextmanager
def rm_css_cls(
    driver: WebDriver, web_elem: WebElement, css_cls: str
) -> Iterator[WebElement]:
    driver.execute_script(f"arguments[0].classList.remove('{css_cls}')", web_elem)
    yield web_elem
    driver.execute_script(f"arguments[0].classList.add('{css_cls}')", web_elem)


def nth(seq: Iterable[T], idx: int) -> Optional[T]:
    return next(islice(seq, idx, None), None)


@contextmanager
def redirect_display(new_display: str) -> Iterator[None]:
    """Replace DISPLAY environment variable with new value"""
    old_display = os.environ.get("DISPLAY", "DUMMY_DISPLAY")
    os.environ["DISPLAY"] = new_display
    try:
        yield
    finally:
        if old_display is not None:
            os.environ["DISPLAY"] = old_display
        else:
            del os.environ["DISPLAY"]


def transform(val: str, strip_char: Optional[str] = None) -> str:
    return val.strip(strip_char).lower().replace(" ", "_").replace("'", "")


def sort_json_keys(obj: JsonValue) -> JsonValue:
    if isinstance(obj, dict):
        items = list(obj.items())
        items.sort(reverse=True)
        return {k: sort_json_keys(v) for k, v in items}

    if isinstance(obj, list):
        return [sort_json_keys(x) for x in obj]
    return obj  # number or string


def sort_json_from_string(value: str) -> JsonValue:
    parsed_value = json.loads(value)
    return sort_json_keys(parsed_value)


class WhichBrowser(Enum):
    ARCHIVE_BROWSER = "archive browser"
    ARCHIVE_FILE_BROWSER = "archive file browser"
    DATASET_BROWSER = "dataset browser"
    FILE_BROWSER = "file browser"
    SHARES_FILE_BROWSER = "share's file browser"
    DATASET_ARCHIVE_BROWSER = "dataset archive browser"
    ARCHIVE_RECALL_BROWSER = "archive recall browser"


class OnedataService(Enum):
    WORKERS = "workers"
    ONES3 = "ones3"


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


class AlertPopup(Enum):
    AUTHENTICATION_SUCCEEDED = "Authentication succeeded!"
    STORAGE_IMPORT_SCAN_STARTED = "Storage import scan has started"
    TOKEN_CREATED = "Token has been created successfully."


PageName = Literal[
    "data",
    "shares",
    "providers",
    "groups",
    "tokens",
    "discovery",
    "automation",
    "clusters",
    "cluster",
]
