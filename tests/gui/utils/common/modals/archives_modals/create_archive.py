"""Utils and fixtures to facilitate operations on create archive modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.web_elements import Button, Input, Label, NamedButton

from ..modal import Modal


class CreateArchive(Modal):
    create = NamedButton(".btn-primary", text="Create")
    description = Input(".textarea-field .form-control")
    bagit = Button(".option-bagit .one-way-radio-control")
    create_nested_archives = Toggle(".createNestedArchives-field .one-way-toggle-track")
    incremental = Toggle(".incremental-field .one-way-toggle-track")
    include_dip = Toggle(".includeDip-field .one-way-toggle-track")
    follow_symbolic_links = Toggle(".followSymlinks-field .one-way-toggle-track")
    base_archive = Label(".field-component.static-text-field")

    def __str__(self):
        return "Create archive"
