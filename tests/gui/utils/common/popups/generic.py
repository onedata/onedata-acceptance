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
    ) -> None:
        self.message = message
        self.category = category
        self.css_sel = f".ember-notify-cn .alert-{category.lower()}"


class AlertPopup(AlertPopupBase, Enum):
    AUTHENTICATION_SUCCEEDED = (
        "Authentication succeeded!",
        "Success",
    )
    STORAGE_IMPORT_SCAN_STARTED = (
        "Storage import scan has started",
        "Info",
    )
    TOKEN_CREATED = (
        "Token has been created successfully.",
        "Success",
    )
    SUCCESSFULLY_JOINED = (r".*joined.*", "Success")
    SUCCESSFULLY_COPIED = (r".*copied.*", "Info")
    PASSWORD_CHANGED = (
        r".*[Pp]assword.*changed.*successfully.*",
        "Success",
    )
    PROVIDER_DATA_MODIFIED = (
        r".*[Pp]rovider.*data.*modified.*",
        "Info",
    )
    PROVIDER_DEREGISTERED = (
        r".*[Pp]rovider.*deregistered.*",
        "Info",
    )
    ADDED_SPACE_SUPPORT = (
        r".*[Aa]dded.*support.*space.*",
        "Success",
    )
    CONFIGURATION_SPACE_SUPPORT_CHANGED = (
        r".*[Cc]onfiguration.*space.*support.*changed.*",
        "Info",
    )
    CEASED_SUPPORT = (r"Ceased.*[Ss]upport.*", "Info")
    STORAGE_ADDED = (r".*[Ss]torage.*added.*", "Success")
    MEMBER_ADDED = (r".*[Mm]ember.*added.*", "Success")
    GROUP_REMOVED_FROM_CLUSTER = (
        r".*[Gg]roup.*removed.*from.*cluster.*",
        "Success",
    )
    PRIVILEGES_SAVED = (
        r".*[Pp]rivileges.*saved.*successfully.*",
        "Success",
    )


class CreatedItemAlertPopup(AlertPopupBase, Enum):
    SPACE = "space"
    GROUP = "group"
    HARVESTER = "harvester"
    AUTOMATION_INVENTORY = "automation inventory"

    def __init__(
        self,
        item_type: CreatedItemType,
    ) -> None:
        self.item_type = item_type
        super().__init__(
            rf"New {item_type} created successfully",
            "Success",
        )


AlertPopupType = AlertPopup | CreatedItemAlertPopup
ALL_ALERT_POPUPS: tuple[AlertPopupType, ...] = (
    *AlertPopup,
    *CreatedItemAlertPopup,
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
