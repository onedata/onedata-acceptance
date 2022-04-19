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

    @staticmethod
    def parse_progress(progress_text_content):
        """Parses recall progress values in format: <current_value>/<target_value>,
        eg. "1 B / 3 B" to tuple containing two strings: (current_value, target_value).
        """
        [progress_info, total_info] = progress_text_content.split('/')
        progress_info = progress_info.strip()
        total_info = total_info.strip()
        return (progress_info, total_info)

    def __str__(self):
        return 'Archive recall information'

    def get_progress_info(self, type):
        """Returns a tuple with (currnet_value, total_value) for progress info.
        Return values are in string, because they can contain size with units, eg.
        ("3 B", "40 KiB").

        :param str type: one of values that are in "<current> / <total>" format,
                         eg. "files_recalled" or "data_recalled"
        """
        return ArchiveRecallInformation.parse_progress(getattr(self, type))
