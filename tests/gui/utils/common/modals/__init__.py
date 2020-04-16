"""Utils for operations on modals in GUI tests
"""

__author__ = "Bartosz Walkowicz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from .create_dir import CreateDir
from .add_storage import AddStorage
from tests.gui.utils.core.web_elements import WebItem
from tests.gui.utils.common.modals.create_group import CreateGroup
from tests.gui.utils.common.common import DropdownSelector

from .data_distribution import DataDistributionModal
from .data_row_menu import DataRowMenu
from .delete_modal import DeleteModal
from .login import LoginFormModal
from .deploying_cluster import ClusterDeploymentModal
from .metadata_modal import MetadataModal
from .menu_in_edit_permissions_modal import EditPermissionsRecordMenu
from .rename_modal import RenameModal
from .rename_share_modal import RenameShareModal
from .revoke_space_support import RevokeSpaceSupportModal
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
from .share_directory import ShareDirectory
from .shares_row_menu import SharesRowMenu


class Modals(object):
    add_storage = WebItem('.panel-onezone-modal.in', cls=AddStorage)
    data_distribution = WebItem('.modal-dialog', cls=DataDistributionModal)
    cluster_deployment = WebItem('.new-cluster-deploy-progress.modal-body',
                                 cls=ClusterDeploymentModal)
    revoke_space_support = WebItem('.modal.in .modal-dialog',
                                   cls=RevokeSpaceSupportModal)
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
    provider_popover = WebItem('.webui-popover .provider-place-drop',
                               cls=ProviderPopover)
    remove_member = WebItem('.remove-relation-modal.modal.in .modal-dialog',
                            cls=RemoveModal)
    remove_harvester = WebItem('.modal-dialog', cls=RemoveModal)
    modify_storage = WebItem('.modify-storage-modal.modal.in .modal-dialog',
                             cls=ModifyStorage)
    remove_storage = WebItem('.remove-storage-modal.modal.in .modal-dialog',
                             cls=RemoveModal)
    error = WebItem('.alert-global.modal.in .modal-dialog',
                    cls=ErrorModal)
    invite_using_token = WebItem('.invite-using-token-modal.modal.in '
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
    remove_space_from_harvester = WebItem('.modal-dialog', cls=RemoveModal)
    dropdown = DropdownSelector('.ember-basic-dropdown-content')
    data_row_menu = WebItem('.file-actions.dropdown-menu', cls=DataRowMenu)
    delete_modal = WebItem('.modal-dialog', cls=DeleteModal)
    rename_modal = WebItem('.modal-dialog', cls=RenameModal)
    file_metadata = WebItem('.modal-dialog', cls=MetadataModal)
    directory_metadata = WebItem('.modal-dialog', cls=MetadataModal)
    menu_in_edit_permissions = WebItem('.over-modals .webui-popover-content '
                                       '.one-webui-popover',
                                       cls=EditPermissionsRecordMenu)
    share_directory = WebItem('.modal-dialog', cls=ShareDirectory)
    shares_row_menu = WebItem('.share-actions.dropdown-menu', cls=SharesRowMenu)
    rename_share = WebItem('.modal-dialog', cls=RenameShareModal)
    remove_share = WebItem('.modal-dialog', cls=RemoveModal)

    def __init__(self, driver):
        self.driver = driver
        self.web_elem = driver

    def __str__(self):
        return 'modals'
