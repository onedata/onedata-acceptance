"""Utils to facilitate dns setup operations in panel GUI."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebElement


class DNSSetup(PageObject):
    documentation_link = WebElement(".documentation-link")

    # Subdomain Delegation
    subdomain_delegation_documentation_link = WebElement(
        ".subheader-text  .documentation-link"
    )
