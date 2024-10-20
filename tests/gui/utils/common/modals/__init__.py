"""Utils for operations on modals in GUI tests"""

__author__ = "Bartosz Walkowicz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import WebItem

from .archives_modals.archive_audit_log import ArchiveAuditLog
from .archives_modals.archive_details import ArchiveDetails
from .archives_modals.archive_recall_information import ArchiveRecallInformation
from .archives_modals.audit_log_entry_details import AuditLogEntryDetails
from .archives_modals.cancel_archive import CancelArchive
from .archives_modals.cancel_recall import CancelRecall
from .archives_modals.create_archive import CreateArchive
from .archives_modals.delete_archive import DeleteArchive
from .archives_modals.recall_archive import RecallArchive
from .basic_modals.add_one_of_elements import AddOneOfElementsModal
from .basic_modals.create_group import CreateGroup
from .basic_modals.delete_modal import DeleteModal
from .basic_modals.leave_element import LeaveElementModal
from .basic_modals.login import LoginFormModal
from .basic_modals.remove import RemoveModal
from .basic_modals.rename_modal import RenameModal
from .basic_modals.there_are_unsaved_changes import ThereAreUnsavedChanges
from .configure_web_cert import ConfigureWebCertModal
from .datasets_modals.datasets_modal import DatasetsModal
from .datasets_modals.detach_dataset import DetachDataset
from .datasets_modals.reattach_dataset import ReattachDataset
from .files_modals.create_dir import CreateDir
from .files_modals.details_modal import DetailsModal
from .files_modals.disable_directory_statistics import DisableDirectoryStatistics
from .files_modals.enable_directory_statistics import EnableDirectoryStatistics
from .files_modals.external_symbolic_link import ExternalSymbolicLink
from .files_modals.share import Share
from .files_modals.symbolic_link_details import SymbolicLinkDetailsModal
from .files_modals.write_protection import WriteProtection
from .management_modals.cease_support_for_space import CeaseSupportForSpaceModal
from .management_modals.change_privileges import ChangePrivilegesModal
from .management_modals.delete_user_account import DeleteUserAccountModal
from .management_modals.deploying_cluster import ClusterDeploymentModal
from .marketplace_modals.advertise_space import AdvertiseSpace
from .marketplace_modals.advertise_space_in_the_marketplace import (
    AdvertiseSpaceInTheMarketplace,
)
from .rest_api_modal import RESTApiModal
from .storage_modals.add_storage import AddStorage
from .storage_modals.modify_storage import ModifyStorage
from .tokens_modals.clean_up_obsolete_tokens import CleanUpObsoleteTokensModal
from .tokens_modals.invite_using_token import InviteUsingTokenModal
from .troubles_modals.dns_configuration_warning import DNSConfigurationWarningModal
from .troubles_modals.emergency_interface import EmergencyInterface
from .troubles_modals.error_modal import ErrorModal
from .troubles_modals.warning_modal import WarningModal
from .workflows_modals.audit_log import AuditLog
from .workflows_modals.create_new_lane import CreateNewLane
from .workflows_modals.duplicate_revision import DuplicateRevision
from .workflows_modals.function_pods_activity import FunctionPodsActivity
from .workflows_modals.select_files_directories_symlink import SelectFiles
from .workflows_modals.select_groups import SelectGroups
from .workflows_modals.store_details import StoreDetails
from .workflows_modals.store_editor import StoreEditor
from .workflows_modals.task_time_series import TaskTimeSeries
from .workflows_modals.unlink_lambda import UnlinkLambda
from .workflows_modals.upload_workflow import UploadWorkflow


class Modals:
    # basic modals
    remove_modal = WebItem(".modal-dialog", cls=RemoveModal)
    leave_modal = WebItem(".modal-dialog", cls=LeaveElementModal)
    add_one_of_elements = WebItem(".modal-dialog", cls=AddOneOfElementsModal)
    delete_modal = WebItem(".modal-dialog", cls=DeleteModal)
    rename_modal = WebItem(".modal-dialog", cls=RenameModal)
    login = WebItem("#login-form-modal", cls=LoginFormModal)
    create_group = WebItem(".modal-dialog", cls=CreateGroup)

    # storage modals
    add_storage = WebItem(".panel-onezone-modal.in", cls=AddStorage)
    modify_storage = WebItem(".modal-dialog .modal-content", cls=ModifyStorage)

    # files modals
    create_dir = WebItem(".modal-dialog", cls=CreateDir)
    share = WebItem(".share-modal .modal-dialog", cls=Share)
    write_protection = WebItem(".modal-dialog", cls=WriteProtection)
    details_modal = WebItem(".modal-dialog", cls=DetailsModal)
    symbolic_link_details = WebItem(".modal-dialog", cls=SymbolicLinkDetailsModal)
    external_symbolic_link = WebItem(".modal-dialog", cls=ExternalSymbolicLink)

    # troubles modals
    emergency_interface = WebItem(".modal-dialog", cls=EmergencyInterface)
    dns_configuration_warning = WebItem(
        ".new-cluster-dns-proceed-modal.modal", cls=DNSConfigurationWarningModal
    )
    error = WebItem(".alert-global.modal.in .modal-dialog", cls=ErrorModal)
    warning = WebItem(".question-modal", cls=WarningModal)

    # tokens modals
    invite_using_token = WebItem(
        ".generate-invite-token-modal.modal.in .modal-dialog",
        cls=InviteUsingTokenModal,
    )
    clean_up_obsolete_tokens = WebItem(".modal-dialog", cls=CleanUpObsoleteTokensModal)

    # archives modals
    create_archive = WebItem(".modal-dialog", cls=CreateArchive)
    recall_archive = WebItem(".modal-dialog", cls=RecallArchive)
    archive_recall_information = WebItem(".modal-dialog", cls=ArchiveRecallInformation)
    delete_archive = WebItem(".modal-dialog", cls=DeleteArchive)
    cancel_recall = WebItem(".cancel-recall-modal .modal-dialog", cls=CancelRecall)
    archive_details = WebItem(".modal-dialog", cls=ArchiveDetails)
    archive_audit_log = WebItem(".modal-dialog", cls=ArchiveAuditLog)
    audit_log_entry_details = WebItem(
        ".details-container.visible", cls=AuditLogEntryDetails
    )
    cancel_archive = WebItem(".modal-content", cls=CancelArchive)

    # datasets modals
    datasets = WebItem(".modal-dialog", cls=DatasetsModal)
    detach_dataset = WebItem(".modal-dialog", cls=DetachDataset)
    reattach_dataset = WebItem(".modal-dialog", cls=ReattachDataset)
    select_dataset = WebItem(".modal-dialog", cls=SelectFiles)

    # workflows modals
    upload_workflow = WebItem(".modal-dialog", cls=UploadWorkflow)
    create_new_store = WebItem(".modal-dialog", cls=StoreEditor)
    modify_store = WebItem(".modal-dialog", cls=StoreEditor)
    create_new_lane = WebItem(".modal-dialog", cls=CreateNewLane)
    duplicate_revision = WebItem(".modal-dialog", cls=DuplicateRevision)
    select_files = WebItem(".modal-dialog", cls=SelectFiles)
    select_groups = WebItem(".modal-dialog", cls=SelectGroups)
    function_pods_activity = WebItem(".modal-dialog", cls=FunctionPodsActivity)
    task_time_series = WebItem(".modal-dialog", cls=TaskTimeSeries)
    store_details = WebItem(".modal-dialog", cls=StoreDetails)
    audit_log = WebItem(".modal-dialog", cls=AuditLog)
    unlink_lambda = WebItem(".modal-dialog", cls=UnlinkLambda)

    # management modals
    change_privileges = WebItem(".modal-dialog", cls=ChangePrivilegesModal)
    delete_user_account = WebItem(".modal-dialog", cls=DeleteUserAccountModal)
    cluster_deployment = WebItem(
        ".new-cluster-deploy-progress.modal-body", cls=ClusterDeploymentModal
    )
    cease_support_for_space = WebItem(
        ".modal.in .modal-dialog", cls=CeaseSupportForSpaceModal
    )

    rest_api_modal = WebItem(".modal-dialog", cls=RESTApiModal)
    configure_web_cert = WebItem("#configure-web-cert-modal", cls=ConfigureWebCertModal)
    enable_directory_statistics = WebItem(
        ".modal-dialog", cls=EnableDirectoryStatistics
    )
    disable_directory_statistics = WebItem(
        ".modal-dialog", cls=DisableDirectoryStatistics
    )

    # marketplace modals
    advertise_space = WebItem(".modal-dialog", cls=AdvertiseSpace)
    advertise_space_in_the_marketplace = WebItem(
        ".modal-dialog", cls=AdvertiseSpaceInTheMarketplace
    )
    there_are_unsaved_changes = WebItem(".modal-dialog", cls=ThereAreUnsavedChanges)

    def __init__(self, driver):
        self.driver = driver
        self.web_elem = driver

    def __str__(self):
        return "modals"
