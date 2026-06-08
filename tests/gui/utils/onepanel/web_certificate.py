"""Utils to facilitate web certificate operations in panel GUI."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata.org"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Any

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label


class WebCertificate(PageObject):
    use_lets_encrypt = Toggle(".letsEncrypt-field .one-way-toggle")
    dns_names = Label(".dnsNames-field .static-list-field-item")
    issuer = Label(".issuer-field .static-text-field")
    certificate_path = Label(".certPath-field .static-text-field")
    key_path = Label(".keyPath-field .static-text-field")
    certificate_chain_path = Label(".chainPath-field .static-text-field")

    warning_info = Label(".alert-warning.alert-simple-info")
    dns_names_warning = Label(".dnsNames-field .warning-item-container")

    def __str__(self) -> Any:
        return "Web certificate"
