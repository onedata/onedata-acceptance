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
from functools import partial
from itertools import islice
from time import sleep
from typing import Literal, Optional, TypeVar, cast, overload

from _pytest._py.path import LocalPath
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    visibility_of,
    visibility_of_element_located,
)
from selenium.webdriver.support.ui import WebDriverWait

from tests import gui
from tests.gui.type_definitions import (
    VisibilityCondition,
    WebElementOrCssLocator,
    WebElementOrSelector,
    WebElemRoot,
)
from tests.gui.utils.common.constants import WAIT_FRONTEND, WAIT_NORMAL_DOWNLOAD
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
    """Parses regex-matched or separator-delimited values into a list,
    e.g. '["1", "2"]', '"1"', '1,2', or '1'.
    """
    if pattern is not None:
        return [default(el.group()) for el in re.finditer(pattern, seq)]
    separator = "," if separator is None else separator
    return [
        default(el.strip().strip('"'))
        for el in seq.strip("[]").split(separator)
        if el != ""
    ]


# An empty sequence, e.g. []
EMPTY_SEQUENCE = r"\[\]"

# A quoted element, including spaces and special characters, e.g. "dev-oneprovider-0"
QUOTED_ELEMENT = r'"[^"\n]+"'

# A single unquoted element without separators or whitespace, e.g. new_space1
UNQUOTED_ELEMENT = r'[^,\[\]"\s]+'

# An element inside a sequence can be quoted or contain unquoted whitespace,
# see BRACKETED_SEQUENCE
SEQUENCE_ELEMENT = rf'(?:{QUOTED_ELEMENT}|[^,\]"\n]+)'

# A comma-separated sequence of elements enclosed in square brackets.
# Examples:
#   [abc]                  -> element 1: abc
#   [abc, def]             -> element 1: abc       | element 2: def
#   [abc def, ghi]         -> element 1: abc def   | element 2: ghi
#   ["abc", "def ghi"]     -> element 1: abc       | element 2: def ghi
#   ["abc, def", ghi]      -> element 1: abc, def  | element 2: ghi
BRACKETED_SEQUENCE = rf"\[\s*{SEQUENCE_ELEMENT}" rf"(?:\s*,\s*{SEQUENCE_ELEMENT})*\s*\]"

# An element sequence can be:
#   abc                    -> element 1: abc
#   abc-def                -> element 1: abc-def
#   "abc def"              -> element 1: abc def
#   "abc, def"             -> element 1: abc, def
#   [abc]                  -> element 1: abc
#   [abc, def]             -> element 1: abc       | element 2: def
#   [abc def, ghi]         -> element 1: abc def   | element 2: ghi
#   ["abc", "def ghi"]     -> element 1: abc       | element 2: def ghi
#   ["abc, def", ghi]      -> element 1: abc, def  | element 2: ghi
ELEMENTS_SEQUENCE_PATTERN = (
    rf"(?:{QUOTED_ELEMENT}|{UNQUOTED_ELEMENT}|{BRACKETED_SEQUENCE}|{EMPTY_SEQUENCE})"
)


def parse_elements_sequence(value: str) -> list[str]:
    if re.fullmatch(ELEMENTS_SEQUENCE_PATTERN, value) is None:
        raise ValueError(f"Invalid elements sequence: {value!r}")
    return parse_seq(value)


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


def is_element_with_selector_visible_on_page(
    driver: WebDriver, css_selector: str
) -> bool:
    try:
        return bool(
            visibility_of_element_located((By.CSS_SELECTOR, css_selector))(driver)
        )
    except NoSuchElementException:
        return False


def get_web_elem_or_locator(
    web_elem_or_selector: WebElementOrSelector,
) -> WebElementOrCssLocator:
    match web_elem_or_selector:
        case WebElement():
            return web_elem_or_selector
        case str():
            return By.CSS_SELECTOR, web_elem_or_selector
    raise TypeError(f"Unsupported element or selector: {web_elem_or_selector!r}")


def get_visibility_condition(
    web_elem_or_locator: WebElementOrCssLocator,
) -> VisibilityCondition:
    match web_elem_or_locator:
        case WebElement() as element:
            return visibility_of(element)

        case (By.CSS_SELECTOR, str()) as locator:
            return visibility_of_element_located(locator)

        case unsupported:
            raise TypeError(f"Unsupported element or locator: {unsupported!r}")


def wait_for_visible_element_using_getter(
    driver: WebDriver,
    web_elem_getter: Callable[[WebDriver], WebElement],
    timeout: float = WAIT_FRONTEND,
) -> WebElement:
    # Wait until the getter returns a visible element.

    def is_element_visible_using_getter(
        driver: WebDriver, web_elem_getter: Callable[[WebDriver], WebElement]
    ) -> WebElement | None:
        web_elem = web_elem_getter(driver)
        return web_elem if visibility_of(web_elem)(driver) else None

    return WebDriverWait(driver, timeout=timeout).until(
        partial(is_element_visible_using_getter, web_elem_getter=web_elem_getter)
    )


def wait_for_file_to_download(
    driver: WebDriver,
    downloaded_file: LocalPath,
    file_name: str,
    timeout: float = WAIT_NORMAL_DOWNLOAD,
) -> None:
    WebDriverWait(driver, timeout).until(
        lambda _: downloaded_file.isfile(),
        message=f"File {file_name} did not finish downloading",
    )


def get_element_css_classes_when_visible(
    driver: WebDriver, web_elem: WebElement, timeout: float = WAIT_FRONTEND // 4
) -> list[str]:
    def get_element_classes(driver: WebDriver) -> list[str] | None:
        return (
            web_elem.get_attribute("class").split()
            if visibility_of(web_elem)(driver)
            else None
        )

    return WebDriverWait(
        driver,
        timeout=timeout,
        poll_frequency=0.05,
        ignored_exceptions=[
            ElementNotInteractableException,
            StaleElementReferenceException,
        ],
    ).until(get_element_classes)


def find_web_elem(
    web_elem_root: WebElemRoot,
    css_selector: str,
    error_message: str | Callable[[], str],
    scroll: bool = True,
) -> WebElement:
    try:
        if scroll:
            _scroll_to_css_selector(web_elem_root, css_selector)
        item = web_elem_root.find_element(By.CSS_SELECTOR, css_selector)
    except NoSuchElementException as exc:
        if callable(error_message):
            error_message = error_message()
        raise NoSuchElementException(error_message) from exc
    return item


def find_web_elem_with_text(
    web_elem_root: WebElemRoot,
    css_selector: str,
    text: str,
    error_message: str | Callable[[], str],
    scroll: bool = True,
) -> WebElement:
    items = web_elem_root.find_elements(By.CSS_SELECTOR, css_selector)
    if scroll:
        _scroll_to_css_selector(web_elem_root, css_selector)
    for item in items:
        if item.text.lower() == text.lower():
            return item
    if callable(error_message):
        error_message = error_message()
    raise NoSuchElementException(
        f'Css element with "{text}" text not found. {error_message}'
    )


def click_on_web_elem(
    driver: WebDriver,
    web_elem: WebElement,
    error_message: str | Callable[[], str],
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
        if callable(error_message):
            error_message = error_message()
        raise ElementNotInteractableException(error_message)


def _scroll_to_css_selector(web_elem_root: WebElemRoot, css_selector: str) -> None:
    driver = getattr(web_elem_root, "parent", web_elem_root)
    driver.execute_script(
        "var el = (typeof $ === 'function' ? "
        f"$('{css_selector}')[0] : "
        f"document.querySelector('{css_selector}')); "
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


def assert_each_event_is_gathered(
    events: list[str],
    gathered_events: list[str],
    option: str,
) -> None:
    for event in events:
        assert event in gathered_events, (
            f'No gathered event with {option} "{event}" was found. '
            f"Gathered {option}s: {gathered_events}"
        )


def are_events_gathered_together(
    first_event: str, second_event: str, gathered_events: list[str]
) -> bool:
    for gathered_event in gathered_events:
        if first_event in gathered_event and second_event in gathered_event:
            return True
    return False


def assert_events_are_gathered_with_event(
    events: list[str],
    other_event: str,
    gathered_events: list[str],
    option: str,
) -> None:
    for event in events:
        events_are_gathered_together = are_events_gathered_together(
            event, other_event, gathered_events
        )

        assert events_are_gathered_together, (
            f'No gathered event with {option} containing "{event}" '
            f'and event "{other_event}" was found. '
            f"Gathered {option}s: {gathered_events}"
        )


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


ListItemMainField = Literal["name", "description"]


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


class HostPattern(Enum):
    PROVIDER_PANEL = r"oneprovider-[0-9]+ provider panel"
    ZONE_PANEL = r"(?:onezone zone panel|[Oo]nezone panel)"
    ZONE = r"[Oo]nezone"
    ONEPANEL_EMERGENCY = r"emergency interface of Onepanel"
    ONEZONE_EMERGENCY = r"emergency interface of Onezone"
    PROVIDER_NODE = r"node[0-9]+ of oneprovider-[0-9]+ provider panel"
