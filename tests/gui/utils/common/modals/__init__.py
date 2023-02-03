"""Utils for operations on modals in GUI tests
"""

__author__ = "Bartosz Walkowicz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from .archives_modals.archive_details import ArchiveDetails
from .archives_modals.archive_recall_information import ArchiveRecallInformation
from .archives_modals.cancel_recall import CancelRecall
from .files_modals.disable_directory_statistics import (
    DisableDirectoryStatistics)
from .files_modals.enable_directory_statistics import EnableDirectoryStatistics
from .files_modals.external_symbolic_link import ExternalSymbolicLink
from .management_modals.change_privileges import ChangePrivilegesModal
from .tokens_modals.clean_up_obsolete_tokens import CleanUpObsoleteTokensModal
from .files_modals.create_dir import CreateDir
from .storage_modals.add_storage import AddStorage
from tests.gui.utils.core.web_elements import WebItem
from .basic_modals.create_group import CreateGroup
from .basic_modals.delete_modal import DeleteModal
from .files_modals.details_modal import DetailsModal
from .basic_modals.login import LoginFormModal
from .management_modals.deploying_cluster import ClusterDeploymentModal
from .archives_modals.recall_archive import RecallArchive
from .basic_modals.rename_modal import RenameModal
from .management_modals.cease_support_for_space import (
    CeaseSupportForSpaceModal)
from .configure_web_cert import ConfigureWebCertModal
from .basic_modals.remove import RemoveModal
from .troubles_modals.error_modal import ErrorModal
from .tokens_modals.invite_using_token import InviteUsingTokenModal
from .troubles_modals.dns_configuration_warning import (
    DNSConfigurationWarningModal)
from .troubles_modals.emergency_interface import EmergencyInterface
from .basic_modals.add_one_of_elements import AddOneOfElementsModal
from .basic_modals.leave_element import LeaveElementModal
from .storage_modals.modify_storage import ModifyStorage
from .rest_api_modal import RESTApiModal
from .files_modals.tabs_in_details_modal.share_directory import ShareDirectory
from .management_modals.delete_user_account import DeleteUserAccountModal
from .files_modals.symbolic_link_details import SymbolicLinkDetailsModal
from .datasets_modals.datasets_modal import DatasetsModal
from .archives_modals.create_archive import CreateArchive
from .datasets_modals.detach_dataset import DetachDataset
from .files_modals.write_protection import WriteProtection
from .archives_modals.delete_archive import DeleteArchive
from .datasets_modals.reattach_dataset import ReattachDataset
from .workflows_modals.store_details import StoreDetails
from .workflows_modals.task_time_series import TaskTimeSeries
from .workflows_modals.upload_workflow import UploadWorkflow
from .workflows_modals.create_new_store import CreateNewStore
from .workflows_modals.create_new_lane import CreateNewLane
from .workflows_modals.duplicate_revision import DuplicateRevision
from .workflows_modals.select_files_directories_symlink import SelectFiles
from .workflows_modals.function_pods_activity import FunctionPodsActivity


class Modals(object):

    # basic modals
    remove_modal = WebItem('.modal-dialog', cls=RemoveModal)
    leave_modal = WebItem('.modal-dialog', cls=LeaveElementModal)
    add_one_of_elements = WebItem('.modal-dialog', cls=AddOneOfElementsModal)
    delete_modal = WebItem('.modal-dialog', cls=DeleteModal)
    rename_modal = WebItem('.modal-dialog', cls=RenameModal)
    login = WebItem('#login-form-modal', cls=LoginFormModal)
    create_group = WebItem('.modal-dialog', cls=CreateGroup)

    # storage modals
    add_storage = WebItem('.panel-onezone-modal.in', cls=AddStorage)
    modify_storage = WebItem('.modify-storage-modal.modal.in .modal-dialog',
                             cls=ModifyStorage)

    # files modals
    create_dir = WebItem('.modal-dialog', cls=CreateDir)
    share_directory = WebItem('.share-modal .modal-dialog', cls=ShareDirectory)
    write_protection = WebItem('.modal-dialog', cls=WriteProtection)
    details_modal = WebItem('.modal-dialog', cls=DetailsModal)
    symbolic_link_details = WebItem('.modal-dialog',
                                    cls=SymbolicLinkDetailsModal)
    external_symbolic_link = WebItem('.modal-dialog',
                                     cls=ExternalSymbolicLink)

    # troubles modals
    emergency_interface = WebItem('.modal-dialog', cls=EmergencyInterface)
    dns_configuration_warning = WebItem('.new-cluster-dns-proceed-modal.modal',
                                        cls=DNSConfigurationWarningModal)
    error = WebItem('.alert-global.modal.in .modal-dialog',
                    cls=ErrorModal)

    # tokens modals
    invite_using_token = WebItem('.generate-invite-token-modal.modal.in '
                                 '.modal-dialog', cls=InviteUsingTokenModal)
    clean_up_obsolete_tokens = WebItem('.modal-dialog',
                                       cls=CleanUpObsoleteTokensModal)

    # archives modals
    create_archive = WebItem('.modal-dialog', cls=CreateArchive)
    recall_archive = WebItem('.modal-dialog', cls=RecallArchive)
    archive_recall_information = WebItem('.modal-dialog',
                                         cls=ArchiveRecallInformation)
    delete_archive = WebItem('.modal-dialog', cls=DeleteArchive)
    cancel_recall = WebItem('.cancel-recall-modal .modal-dialog',
                            cls=CancelRecall)
    archive_details = WebItem('.modal-dialog', cls=ArchiveDetails)

    # datasets modals
    datasets = WebItem('.modal-dialog', cls=DatasetsModal)
    detach_dataset = WebItem('.modal-dialog', cls=DetachDataset)
    reattach_dataset = WebItem('.modal-dialog', cls=ReattachDataset)

    # workflows modals
    upload_workflow = WebItem('.modal-dialog', cls=UploadWorkflow)
    create_new_store = WebItem('.modal-dialog', cls=CreateNewStore)
    create_new_lane = WebItem('.modal-dialog', cls=CreateNewLane)
    duplicate_revision = WebItem('.modal-dialog', cls=DuplicateRevision)
    select_files = WebItem('.modal-dialog', cls=SelectFiles)
    function_pods_activity = WebItem('.modal-dialog', cls=FunctionPodsActivity)
    task_time_series = WebItem('.modal-dialog', cls=TaskTimeSeries)
    store_details = WebItem('.modal-dialog', cls=StoreDetails)

    # management modals
    change_privileges = WebItem('.modal-dialog', cls=ChangePrivilegesModal)
    delete_user_account = WebItem('.modal-dialog', cls=DeleteUserAccountModal)
    cluster_deployment = WebItem('.new-cluster-deploy-progress.modal-body',
                                 cls=ClusterDeploymentModal)
    cease_support_for_space = WebItem('.modal.in .modal-dialog',
                                      cls=CeaseSupportForSpaceModal)

    rest_api_modal = WebItem('.modal-dialog', cls=RESTApiModal)
    configure_web_cert = WebItem('#configure-web-cert-modal',
                                 cls=ConfigureWebCertModal)
    enable_directory_statistics = WebItem('.modal-dialog',
                                          cls=EnableDirectoryStatistics)
    disable_directory_statistics = WebItem('.modal-dialog',
                                           cls=DisableDirectoryStatistics)

    def __init__(self, driver):
        self.driver = driver
        self.web_elem = driver

    def __str__(self):
        return 'modals'
