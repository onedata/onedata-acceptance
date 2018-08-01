"""Utils for operations on modals in GUI tests
"""

from .data_distribution import DataDistributionModal
from .add_storage import AddStorage
from tests.gui.utils.core.web_elements import WebItem

from .data_distribution import DataDistributionModal
from .login import LoginFormModal
from .deploying_cluster import ClusterDeploymentModal
from .revoke_space_support import RevokeSpaceSupportModal
from .edit_permissions import EditPermissionsModal
from .remove import RemoveModal
from .leave_group import LeaveGroupModal
from .leave_parent import LeaveParentModal
from .error_modal import ErrorModal

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


class Modals(object):
    add_storage = WebItem('.panel-onezone-modal.in', cls=AddStorage)
    data_distribution = WebItem('#file-chunks-modal', cls=DataDistributionModal)
    cluster_deployment = WebItem('#cluster-deploy-progress-modal',
                                 cls=ClusterDeploymentModal)
    revoke_space_support = WebItem('.modal.in .modal-dialog',
                                   cls=RevokeSpaceSupportModal)
    login = WebItem('#login-form-modal', cls=LoginFormModal)
    edit_permissions = WebItem('#edit-permissions-modal', cls=EditPermissionsModal)

    remove_group = WebItem('.remove-group-modal', cls=RemoveModal)
    leave_group = WebItem('.leave-group-modal', cls=LeaveGroupModal)
    leave_parent = WebItem('.leave-parent-modal', cls=LeaveParentModal)
    remove_user = WebItem('.remove-user-modal', cls=RemoveModal)
    error = WebItem('.alert-global', cls=ErrorModal)

    def __init__(self, driver):
        self.driver = driver
        self.web_elem = driver

    def __str__(self):
        return 'modals'
