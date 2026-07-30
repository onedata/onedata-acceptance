"""Generic definitions for alert popups in GUI tests."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from enum import Enum


class AlertPopup(Enum):
    AUTHENTICATION_SUCCEEDED = "Authentication succeeded!"
    STORAGE_IMPORT_SCAN_STARTED = "Storage import scan has started"
    TOKEN_CREATED = "Token has been created successfully."
    SUCCESSFULLY_JOINED = r".*joined.*"
    SUCCESSFULLY_COPIED = r".*copied.*"
    PASSWORD_CHANGED = r".*[Pp]assword.*changed.*successfully.*"
    PROVIDER_DATA_MODIFIED = r".*[Pp]rovider.*data.*modified.*"
    PROVIDER_DEREGISTERED = r".*[Pp]rovider.*deregistered.*"
    ADDED_SPACE_SUPPORT = r".*[Aa]dded.*support.*space.*"
    CONFIGURATION_SPACE_SUPPORT_CHANGED = (
        r".*[Cc]onfiguration.*space.*support.*changed.*"
    )
    CEASED_SUPPORT = r"Ceased.*[Ss]upport.*"
    STORAGE_ADDED = r".*[Ss]torage.*added.*"


ALERT_POPUP_ALIASES: dict[str, AlertPopup] = {
    popup.name.lower().replace("_", " "): popup for popup in AlertPopup
}


ALERT_POPUPS_WITH_CSS_CLASS_INFO: list[AlertPopup] = [
    AlertPopup.AUTHENTICATION_SUCCEEDED,
    AlertPopup.STORAGE_IMPORT_SCAN_STARTED,
    AlertPopup.SUCCESSFULLY_COPIED,
    AlertPopup.PASSWORD_CHANGED,
    AlertPopup.PROVIDER_DATA_MODIFIED,
    AlertPopup.PROVIDER_DEREGISTERED,
    AlertPopup.CONFIGURATION_SPACE_SUPPORT_CHANGED,
    AlertPopup.CEASED_SUPPORT,
    AlertPopup.STORAGE_ADDED,
]

ALERT_POPUPS_WITH_CSS_CLASS_SUCCESS: list[AlertPopup] = [
    AlertPopup.SUCCESSFULLY_JOINED,
    AlertPopup.TOKEN_CREATED,
]

ALERT_POPUPS_WITH_CSS_CLASS_DEFAULT: list[AlertPopup] = [AlertPopup.ADDED_SPACE_SUPPORT]


class AlertPopupCssClass(Enum):
    SUCCESS = "success"
    ALERT_INFO = "alert-info"
    DEFAULT = "ember-notify-default"


ALERT_POPUP_CSS_CLASS_ALIASES: dict[str, AlertPopupCssClass] = {
    "success": AlertPopupCssClass.SUCCESS,
    "info": AlertPopupCssClass.ALERT_INFO,
    "default": AlertPopupCssClass.DEFAULT,
}


def parse_alert_popup(value: str) -> AlertPopup:
    value = value.strip().lower()
    try:
        return ALERT_POPUP_ALIASES[value]
    except KeyError as exc:
        raise ValueError(f"Unknown alert popup: {value!r}") from exc


def parse_alert_popup_css_class(value: str) -> AlertPopupCssClass:
    value = value.strip().lower()
    try:
        return ALERT_POPUP_CSS_CLASS_ALIASES[value]
    except KeyError as exc:
        raise ValueError(f"Unknown alert popup CSS class: {value!r}") from exc
