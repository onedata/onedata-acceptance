"""Utils for operations on modals in GUI tests
"""

__author__ = "Bartosz Walkowicz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from .change_privileges import ChangePrivilegesModal
from .clean_up_obsolete_tokens import CleanUpObsoleteTokensModal
from .create_dir import CreateDir
from .add_storage import AddStorage
from tests.gui.utils.core.web_elements import WebItem
from tests.gui.utils.common.modals.create_group import CreateGroup
from tests.gui.utils.common.common import (DropdownSelector,
                                           MigrateDropdownSelector)
from .data_distribution import DataDistributionModal
from .data_row_menu import DataRowMenu
from .archive_row_menu import ArchiveRowMenu
from .delete_modal import DeleteModal
from .file_details import FileDetailsModal
from .login import LoginFormModal
from .deploying_cluster import ClusterDeploymentModal
from .metadata_modal import MetadataModal
from .menu_in_edit_permissions_modal import EditPermissionsRecordMenu
from .qos import QualityOfServiceModal
from .rename_modal import RenameModal
from .rename_share_modal import RenameShareModal
from .cease_support_for_space import CeaseSupportForSpaceModal
from .edit_permissions import EditPermissionsModal
from .configure_web_cert import ConfigureWebCertModal
from .remove import RemoveModal
from .leave_space import LeaveSpaceModal
from .leave_parent import LeaveParentModal
from .error_modal import ErrorModal
from .invite_using_token import InviteUsingTokenModal
from .dns_configuration_warning import DNSConfigurationWarningModal
from .provider_popover import ProviderPopover
from .membership_relation_menu import MembershipRelationMenu
from .groups_hierarchy_menu import GroupHierarchyMenu
from .emergency_interface import EmergencyInterface
from .add_one_of_elements import AddOneOfElementsModal
from .leave_element import LeaveElementModal
from .modify_storage import ModifyStorage
from .rest_api_modal import RESTApiModal
from .share_directory import ShareDirectory
from .shares_row_menu import SharesRowMenu
from .delete_user_account import DeleteUserAccountModal
from .symbolic_link_details import SymbolicLinkDetailsModal
from .datasets_modal import DatasetsModal
from .create_archive import CreateArchive
from .remove_selected_dataset import RemoveSelectedDataset
from .detach_dataset import DetachDataset
from .write_protection import WriteProtection
from .purge_archive import PurgeArchive
from .reattach_dataset import ReattachDataset
from .upload_workflow import UploadWorkflow
from .create_new_store import CreateNewStore
from .create_new_lane import CreateNewLane


class Modals(object):
    add_storage = WebItem('.panel-onezone-modal.in', cls=AddStorage)
    data_distribution = WebItem('.modal-dialog', cls=DataDistributionModal)
    cluster_deployment = WebItem('.new-cluster-deploy-progress.modal-body',
                                 cls=ClusterDeploymentModal)
    cease_support_for_space = WebItem('.modal.in .modal-dialog',
                                      cls=CeaseSupportForSpaceModal)
    login = WebItem('#login-form-modal', cls=LoginFormModal)
    edit_permissions = WebItem('.modal-dialog',
                               cls=EditPermissionsModal)
    configure_web_cert = WebItem('#configure-web-cert-modal',
                                 cls=ConfigureWebCertModal)
    dns_configuration_warning = WebItem('.new-cluster-dns-proceed-modal.modal',
                                        cls=DNSConfigurationWarningModal)
    remove_group = WebItem('.group-remove-modal.modal.in .modal-dialog',
                           cls=RemoveModal)
    leave_group = WebItem('.leave-modal.modal.in .modal-dialog',
                          cls=LeaveElementModal)
    leave_parent = WebItem('.leave-parent-modal.modal.in .modal-dialog',
                           cls=LeaveParentModal)
    leave_space = WebItem('.modal-dialog',
                          cls=LeaveSpaceModal)
    leave_harvester = WebItem('.modal-dialog', cls=LeaveElementModal)
    leave_inventory = WebItem('.modal-dialog', cls=LeaveElementModal)
    provider_popover = WebItem('.webui-popover .provider-place-drop',
                               cls=ProviderPopover)
    remove_member = WebItem('.remove-relation-modal.modal.in .modal-dialog',
                            cls=RemoveModal)
    modify_storage = WebItem('.modify-storage-modal.modal.in .modal-dialog',
                             cls=ModifyStorage)
    remove_storage = WebItem('.remove-storage-modal.modal.in .modal-dialog',
                             cls=RemoveModal)
    error = WebItem('.alert-global.modal.in .modal-dialog',
                    cls=ErrorModal)
    invite_using_token = WebItem('.generate-invite-token-modal.modal.in '
                                 '.modal-dialog',
                                 cls=InviteUsingTokenModal)
    group_hierarchy_menu = WebItem('.group-actions.one-webui-popover',
                                   cls=GroupHierarchyMenu)
    relation_menu = WebItem('.line-actions.one-webui-popover',
                            cls=GroupHierarchyMenu)
    create_group = WebItem('.modal-dialog', cls=CreateGroup)
    create_dir = WebItem('.modal-dialog', cls=CreateDir)
    membership_relation_menu = WebItem('.relation-actions.one-webui-popover',
                                       cls=MembershipRelationMenu)
    emergency_interface = WebItem('.modal-dialog', cls=EmergencyInterface)
    add_one_of_groups = WebItem('.modal-dialog', cls=AddOneOfElementsModal)
    add_one_of_spaces = WebItem('.modal-dialog', cls=AddOneOfElementsModal)
    add_one_of_harvesters = WebItem('.modal-dialog', cls=AddOneOfElementsModal)
    remove_space_from_harvester = WebItem('.modal-dialog', cls=RemoveModal)
    dropdown = DropdownSelector('.ember-basic-dropdown-content')
    migrate_dropdown = MigrateDropdownSelector('.ember-basic-dropdown-content')
    data_row_menu = WebItem('.file-actions.dropdown-menu',
                            cls=DataRowMenu)
    dataset_row_menu = WebItem('.left-bottom .file-actions.dropdown-menu',
                               cls=DataRowMenu)
    archive_row_menu = WebItem('.left-top .webui-popover-inner '
                               '.file-actions.dropdown-menu',
                               cls=ArchiveRowMenu)
    delete_modal = WebItem('.modal-dialog', cls=DeleteModal)
    rename_modal = WebItem('.modal-dialog', cls=RenameModal)
    metadata = WebItem('.modal-dialog', cls=MetadataModal)
    menu_in_edit_permissions = WebItem('.over-modals .webui-popover-content '
                                       '.one-webui-popover',
                                       cls=EditPermissionsRecordMenu)
    share_directory = WebItem('.modal-dialog', cls=ShareDirectory)
    shares_row_menu = WebItem('.share-actions.dropdown-menu', cls=SharesRowMenu)
    rename_share = WebItem('.modal-dialog', cls=RenameShareModal)
    remove_share = WebItem('.modal-dialog', cls=RemoveModal)
    remove_token = WebItem('.modal-dialog', cls=RemoveModal)
    remove_harvester = WebItem('.modal-dialog', cls=RemoveModal)
    remove_space = WebItem('.modal-dialog', cls=RemoveModal)
    remove_inventory = WebItem('.modal-dialog', cls=RemoveModal)
    rest_api_modal = WebItem('.modal-dialog', cls=RESTApiModal)
    clean_up_obsolete_tokens = WebItem('.modal-dialog',
                                       cls=CleanUpObsoleteTokensModal)
    quality_of_service = WebItem('.modal-dialog', cls=QualityOfServiceModal)
    change_privileges = WebItem('.modal-dialog', cls=ChangePrivilegesModal)

    delete_user_account = WebItem('.modal-dialog', cls=DeleteUserAccountModal)
    file_details = WebItem('.modal-dialog', cls=FileDetailsModal)
    directory_details = WebItem('.modal-dialog', cls=FileDetailsModal)
    symbolic_link_details = WebItem('.modal-dialog',
                                    cls=SymbolicLinkDetailsModal)
    datasets = WebItem('.modal-dialog', cls=DatasetsModal)
    create_archive = WebItem('.modal-dialog', cls=CreateArchive)
    remove_selected_dataset = WebItem('.modal-dialog',
                                      cls=RemoveSelectedDataset)
    detach_dataset = WebItem('.modal-dialog', cls=DetachDataset)
    write_protection = WebItem('.modal-dialog', cls=WriteProtection)
    purge_archive = WebItem('.modal-dialog', cls=PurgeArchive)
    reattach_dataset = WebItem('.modal-dialog', cls=ReattachDataset)
    create_new_store = WebItem('.modal-dialog', cls=CreateNewStore)
    create_new_lane = WebItem('.modal-dialog', cls=CreateNewLane)


    def __init__(self, driver):
        self.driver = driver
        self.web_elem = driver

    def __str__(self):
        return 'modals'
