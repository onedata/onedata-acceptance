"""Utils and fixtures to facilitate operations on recall archive information
 modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Label


class ArchiveRecallInformation(Modal):
    status = Label('.recall-info-row-process-status .property-value')
    files_recalled = Label('.recall-info-row-files .property-value')
    data_recalled = Label('.recall-info-row-bytes .property-value')
    started_at = Label('.recall-info-row-started-at .property-value')
    finished_at = Label('.recall-info-row-finished-at .property-value')
    items_failed = Label('.recall-info-row-files-failed .property-value')
    last_error = Label('.recall-info-row-last-error .property-value')

    def __str__(self):
        return 'Archive recall information'
