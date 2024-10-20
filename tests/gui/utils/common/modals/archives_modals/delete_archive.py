"""Utils and fixtures to facilitate operations on delete archive modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.core.web_elements import Input, NamedButton

from ..modal import Modal


class DeleteArchive(Modal):
    confirmation_input = Input(".form-control")
    delete_archive = NamedButton(".btn-danger", text="Delete archive")

    def __str__(self):
        return "Delete archive"
