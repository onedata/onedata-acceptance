"""Utils for operations on modals in GUI tests
"""

__author__ = "Bartosz Walkowicz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.onezone.data_page import ProviderPopover
from .data_distribution import DataDistributionModal
from .add_storage import AddStorage
from tests.gui.utils.core.web_elements import WebItem
from tests.gui.utils.common.modals.create_group import CreateGroup

from .data_distribution import DataDistributionModal
from .login import LoginFormModal
from .deploying_cluster import ClusterDeploymentModal
from .revoke_space_support import RevokeSpaceSupportModal
from .edit_permissions import EditPermissionsModal
from .configure_web_cert import ConfigureWebCertModal
from .remove import RemoveModal
from .leave_group import LeaveGroupModal
from .leave_space import LeaveSpaceModal
from .leave_parent import LeaveParentModal
from .error_modal import ErrorModal
from .invite_using_token import InviteUsingTokenModal
from .dns_configuration_warning import DNSConfigurationWarningModal
from .groups_hierarchy_menu import GroupHierarchyMenu


class Modals(object):
    add_storage = WebItem('.panel-onezone-modal.in', cls=AddStorage)
    data_distribution = WebItem('#file-chunks-modal', cls=DataDistributionModal)
    cluster_deployment = WebItem('#cluster-deploy-progress-modal',
                                 cls=ClusterDeploymentModal)
    revoke_space_support = WebItem('.modal.in .modal-dialog',
                                   cls=RevokeSpaceSupportModal)
    login = WebItem('#login-form-modal', cls=LoginFormModal)
    edit_permissions = WebItem('#edit-permissions-modal',
                               cls=EditPermissionsModal)
    configure_web_cert = WebItem('#configure-web-cert-modal',
                                 cls=ConfigureWebCertModal)
    dns_configuration_warning = WebItem('.new-cluster-dns-proceed-modal.modal',
                                        cls=DNSConfigurationWarningModal)
    remove_group = WebItem('.group-remove-modal.modal.in .modal-dialog',
                           cls=RemoveModal)
    leave_group = WebItem('.leave-modal.modal.in .modal-dialog',
                          cls=LeaveGroupModal)
    leave_parent = WebItem('.leave-parent-modal.modal.in .modal-dialog',
                           cls=LeaveParentModal)
    leave_space = WebItem('.modal-dialog',
                          cls=LeaveSpaceModal)
    provider_popover = WebItem('.webui-popover .provider-place-drop',
                               cls=ProviderPopover)
    remove_member = WebItem('.remove-relation-modal.modal.in .modal-dialog',
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

    def __init__(self, driver):
        self.driver = driver
        self.web_elem = driver

    def __str__(self):
        return 'modals'
