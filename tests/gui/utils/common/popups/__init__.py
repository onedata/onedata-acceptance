"""Utils for operations on modals in GUI tests"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.common.common import DropdownSelector, MigrateDropdownSelector
from tests.gui.utils.core.web_elements import (
    Label,
    WebElementsSequence,
    WebItem,
    WebItemsSequence,
)
from tests.utils.utils import repeat_failed

from .archive_row_menu import ArchiveRowMenu
from .boolean_values import BooleanValues
from .chart_statistics import ChartStatistics
from .configure_columns_menu import ConfigureColumnsMenu
from .consumer_caveat import ConsumerCaveat
from .cookies import Cookies
from .data_distribution_popup import DataDistributionPopup
from .data_row_menu import DataRowMenu
from .delete_account_menu import UserDeleteAccountPopoverMenu
from .deregister_provider import DeregisterProvider
from .groups_hierarchy_menu import GroupHierarchyMenu
from .handle_service import HandleService
from .matching_storages import MatchingStoragesPopup
from .member_menu import MenuPopupWithText
from .membership_relation_menu import MembershipRelationMenu
from .menu_in_edit_permissions import EditPermissionsRecordMenu
from .menu_popup import MenuPopupWithLabel
from .metadata_type import MetadataType
from .options_selector import OptionsSelector
from .power_select import PowerSelect
from .provider_details import ProviderDetails, ProviderMapPopover
from .qos_delete import DeleteQosPopup
from .query_builder import ExpressionBuilderPopup
from .selector_popup import SelectorPopup
from .shares_row_menu import SharesRowMenu
from .spaces_tags import SpacesTags
from .toolbar import ToolbarPopup
from .upload_presenter import UploadPresenter
from .user_account_menu import UserAccountPopup
from .workflow_creation_alert import WorkflowCreationAlert
from .workflow_menu import WorkflowMenu


class Popups:
    toolbar = WebItem(".webui-popover.in ul.dropdown-menu", cls=ToolbarPopup)
    deregister_provider = WebItem(
        ".popover-deregister-provider", cls=DeregisterProvider
    )
    user_account_menu = WebItem(
        ".webui-popover-content .user-account-menu", cls=UserAccountPopup
    )
    upload_presenter = WebItemsSequence(
        ".hidden-xs .up-single-upload", cls=UploadPresenter
    )
    menu_popup = WebItem("#webuiPopover1", cls=MenuPopupWithLabel)
    menu_popup_with_label = WebItem(".webui-popover.in", cls=MenuPopupWithLabel)
    menu_popup_with_text = WebItem(".webui-popover.in", cls=MenuPopupWithText)
    selector_popup = WebItem(".webui-popover.in", cls=SelectorPopup)
    consumer_caveat_popup = WebItem(".webui-popover-tags-selector", cls=ConsumerCaveat)
    user_delete_account_popover_menu = WebItem(
        ".in .webui-popover-inner", cls=UserDeleteAccountPopoverMenu
    )
    query_builder_popups = WebItemsSequence(
        ".query-builder-block-selector", cls=ExpressionBuilderPopup
    )
    data_distribution_popup = WebItem(".webui-popover.in", cls=DataDistributionPopup)
    delete_qos_popup = WebItem(".webui-popover.in", cls=DeleteQosPopup)
    power_select = WebItem(".ember-power-select-dropdown", cls=PowerSelect)
    storages_matching_popover = WebItem(
        ".webui-popover-qos-expression-info-list", cls=MatchingStoragesPopup
    )
    cookies = WebItem(".cookies-consent", cls=Cookies)
    group_hierarchy_menu = WebItem(
        ".group-actions.one-webui-popover", cls=GroupHierarchyMenu
    )
    relation_menu = WebItem(".line-actions.one-webui-popover", cls=GroupHierarchyMenu)

    membership_relation_menu = WebItem(
        ".relation-actions.one-webui-popover", cls=MembershipRelationMenu
    )

    provider_details = WebItem(
        ".webui-popover-content .provider-info-content", cls=ProviderDetails
    )
    provider_map_popover = WebItem(
        ".webui-popover .provider-place-drop", cls=ProviderMapPopover
    )
    dropdown = DropdownSelector(".ember-basic-dropdown-content")
    migrate_dropdown = MigrateDropdownSelector(".ember-basic-dropdown-content")
    data_row_menu = WebItem(".file-actions.dropdown-menu", cls=DataRowMenu)
    dataset_row_menu = WebItem(
        ".left-bottom .file-actions.dropdown-menu", cls=DataRowMenu
    )
    archive_row_menu = WebItem(
        ".left-top .webui-popover-inner .file-actions.dropdown-menu",
        cls=ArchiveRowMenu,
    )
    workflow_menu = WebItem(".atm-workflow-execution-actions", cls=WorkflowMenu)
    menu_in_edit_permissions = WebItem(
        ".over-modals .webui-popover-content .one-webui-popover",
        cls=EditPermissionsRecordMenu,
    )

    shares_row_menu = WebItem(".share-actions.dropdown-menu", cls=SharesRowMenu)
    chart_statistics = WebItem(".chart-tooltip", cls=ChartStatistics)
    handle_service = WebItem(".ember-power-select-options", cls=HandleService)
    metadata_type = WebItem(".ember-power-select-options", cls=MetadataType)
    boolean_values = WebItem(".ember-power-select-options", cls=BooleanValues)
    time_resolutions_list = WebElementsSequence(
        ".time-resolutions-dropdown .ember-power-select-option"
    )
    workflow_initial_values = WebItem(
        ".in .file-value-editor-selector-actions", cls=MenuPopupWithLabel
    )
    workflow_dataset_initial_value = WebItem(
        ".in .dataset-value-editor-selector-actions", cls=MenuPopupWithLabel
    )
    workflow_group_initial_value = WebItem(
        ".in .group-value-editor-selector-actions", cls=MenuPopupWithLabel
    )
    run_info = Label(".tooltip-inner")
    spaces_tags = WebItem(".space-tags-selector", cls=SpacesTags)
    toggle_label = Label(".tooltip .tooltip-inner")
    configure_columns_menu = WebItem(
        ".webui-popover-columns-configuration", cls=ConfigureColumnsMenu
    )
    logging_level = WebItem(".logLevel-field-dropdown", cls=PowerSelect)
    options_selector = WebItem(".webui-popover.in", cls=OptionsSelector)
    workflow_creation_alert = WebItem(".alert.alert-success", cls=WorkflowCreationAlert)

    def __init__(self, driver):
        self.driver = self.web_elem = driver

    def __str__(self):
        return "popups"

    def is_upload_presenter(self):
        return len(self.upload_presenter) > 0

    @repeat_failed(timeout=10)
    def get_query_builder_not_hidden_popup(self):
        for popup in self.query_builder_popups:
            if popup.web_elem.is_displayed():
                return popup
        raise RuntimeError("No query builder popups visible")
