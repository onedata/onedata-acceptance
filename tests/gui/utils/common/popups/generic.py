"""Generic definitions for alert popups in GUI tests."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from enum import Enum
from typing import Literal

AlertPopupCategory = Literal["Success", "Info", "Warning", "Fail"]
CreatedItemType = Literal["space", "group", "harvester", "automation inventory"]


class AlertPopupBase:
    def __init__(
        self,
        message: str,
        category: AlertPopupCategory,
        css_sel: str,
    ) -> None:
        self.message = message
        self.category = category
        self.css_sel = css_sel


class AlertPopup(AlertPopupBase, Enum):
    AUTHENTICATION_SUCCEEDED = (
        "Authentication succeeded!",
        "Success",
        ".alert-info",
    )
    STORAGE_IMPORT_SCAN_STARTED = (
        "Storage import scan has started",
        "Info",
        ".alert-info",
    )
    TOKEN_CREATED = (
        "Token has been created successfully.",
        "Success",
        ".ember-notify-cn",
    )
    SUCCESSFULLY_JOINED = (r".*joined.*", "Success", ".ember-notify-cn")
    SUCCESSFULLY_COPIED = (r".*copied.*", "Info", ".alert-info")
    PASSWORD_CHANGED = (
        r".*[Pp]assword.*changed.*successfully.*",
        "Success",
        ".alert-info",
    )
    PROVIDER_DATA_MODIFIED = (
        r".*[Pp]rovider.*data.*modified.*",
        "Info",
        ".alert-info",
    )
    PROVIDER_DEREGISTERED = (
        r".*[Pp]rovider.*deregistered.*",
        "Info",
        ".alert-info",
    )
    ADDED_SPACE_SUPPORT = (
        r".*[Aa]dded.*support.*space.*",
        "Success",
        ".ember-notify-cn",
    )
    CONFIGURATION_SPACE_SUPPORT_CHANGED = (
        r".*[Cc]onfiguration.*space.*support.*changed.*",
        "Info",
        ".alert-info",
    )
    CEASED_SUPPORT = (r"Ceased.*[Ss]upport.*", "Info", ".alert-info")
    STORAGE_ADDED = (r".*[Ss]torage.*added.*", "Success", ".alert-info")


class ItemCreatedAlertPopup(AlertPopupBase, Enum):
    SPACE_CREATED = "space"
    GROUP_CREATED = "group"
    HARVESTER_CREATED = "harvester"
    AUTOMATION_INVENTORY_CREATED = "automation inventory"

    def __init__(
        self,
        item_type: CreatedItemType,
    ) -> None:
        self.item_type = item_type
        super().__init__(
            rf"New {item_type} created successfully",
            "Success",
            ".alert-info",
        )


AlertPopupType = AlertPopup | ItemCreatedAlertPopup


ALL_ALERT_POPUPS: tuple[AlertPopupType, ...] = (
    *AlertPopup,
    *ItemCreatedAlertPopup,
)


ALERT_POPUP_ALIASES: dict[str, AlertPopupBase] = {
    popup.name.lower().replace("_", " "): popup for popup in ALL_ALERT_POPUPS
}


def parse_alert_popup(value: str) -> AlertPopupBase:
    value = value.strip().lower()
    try:
        return ALERT_POPUP_ALIASES[value]
    except KeyError as exc:
        raise ValueError(f"Unknown alert popup: {value!r}") from exc
