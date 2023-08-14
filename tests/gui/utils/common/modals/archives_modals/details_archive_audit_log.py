"""Utils and fixtures to facilitate operations on archive audit log modal.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Input, Label, Button


class DetailsArchiveAuditLog(Modal):
    event_message = Label('.event-message')
    relative_location = Input('.entry-info-row-relative-location '
                              '.clipboard-input')
    start_time = Label('.entry-info-row-start-time .property-value')
    end_time = Label('.entry-info-row-end-time .property-value')
    time_taken = Label('.entry-info-row-event .time-taken-text')
    item_type = Label('.entry-info-row-archived-item-link .property-name')
    archived_item_absolute_location = Input('.entry-info-row-archived-item-'
                                            'absolute-location .clipboard-'
                                            'input')
    file_id = Input('.entry-info-row-archived-item-file-id .clipboard-input')
    source_item_absolute_location = Input('.entry-info-row-source-item-absolute'
                                          '-location .clipboard-input')
    close = Button('.close-details')

    def __str__(self):
        return 'Details archive audit log'
