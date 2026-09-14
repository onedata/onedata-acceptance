"""Generic definitions for Onedata homepage GUI tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

from tests.gui.utils.homepage.api import EndpointInfo

SPACE_ENDPOINTS: Final[dict[str, EndpointInfo]] = {
    "Get space details": EndpointInfo.space("GET", "Get space details"),
    "List all space privileges": EndpointInfo.space("GET", "List all space privileges"),
    "List direct space users": EndpointInfo.space("GET", "List space users"),
    "List effective space users": EndpointInfo.space(
        "GET", "List effective space users"
    ),
    "Get effective space user details": EndpointInfo.space(
        "GET", "Get effective space user details"
    ),
    "List user's direct space privileges": EndpointInfo.space(
        "GET", "List user's space privileges"
    ),
    "List user's effective space privileges": EndpointInfo.space(
        "GET", "List effective user's space privileges"
    ),
    "Update user's space privileges": EndpointInfo.space(
        "PATCH", "Update user's space privileges"
    ),
    "List direct space groups": EndpointInfo.space("GET", "List space groups"),
    "List effective space groups": EndpointInfo.space(
        "GET", "List effective space groups"
    ),
    "Get effective space group details": EndpointInfo.space(
        "GET", "Get effective space group details"
    ),
    "List group's direct space privileges": EndpointInfo.space(
        "GET", "List group's space privileges"
    ),
    "List group's effective space privileges": EndpointInfo.space(
        "GET", "List effective group's space privileges"
    ),
    "Update group's space privileges": EndpointInfo.space(
        "PATCH",
        "Update group privileges to space",
    ),
    "List space shares": EndpointInfo.space("GET", "List space shares"),
}

FILE_DETAILS_ENDPOINTS: Final[dict[str, EndpointInfo]] = {
    "Download directory (tar)": EndpointInfo.file_details(
        "GET", "Download file content", "Basic File Operations"
    ),
    "List directory files and subdirectories": EndpointInfo.file_details(
        "GET", "List directory files and subdirectories", "Basic File Operations"
    ),
    "Create file in directory": EndpointInfo.file_details(
        "POST", "Create file in directory", "Basic File Operations"
    ),
    "Remove file": EndpointInfo.file_details(
        "DELETE", "Remove file", "Basic File Operations"
    ),
    "Get attributes": EndpointInfo.file_details(
        "GET", "Get file attributes", "Basic File Operations"
    ),
    "Get JSON metadata": EndpointInfo.file_details(
        "GET", "Get file JSON metadata", "Custom File Metadata"
    ),
    "Set JSON metadata": EndpointInfo.file_details(
        "PUT", "Set file JSON metadata", "Custom File Metadata"
    ),
    "Remove JSON metadata": EndpointInfo.file_details(
        "DELETE", "Remove file JSON metadata", "Custom File Metadata"
    ),
    "Get RDF metadata": EndpointInfo.file_details(
        "GET", "Get file RDF metadata", "Custom File Metadata"
    ),
    "Set RDF metadata": EndpointInfo.file_details(
        "PUT", "Set file RDF metadata", "Custom File Metadata"
    ),
    "Remove RDF metadata": EndpointInfo.file_details(
        "DELETE", "Remove file RDF metadata", "Custom File Metadata"
    ),
    "Get extended attributes (xattrs)": EndpointInfo.file_details(
        "GET", "Get file extended attributes", "Custom File Metadata"
    ),
    "Set extended attribute (xattr)": EndpointInfo.file_details(
        "PUT", "Set file extended attribute", "Custom File Metadata"
    ),
    "Remove extended attributes (xattrs)": EndpointInfo.file_details(
        "DELETE", "Remove file extended attributes", "Custom File Metadata"
    ),
    "Get data distribution": EndpointInfo.file_details(
        "GET", "Get data distribution", "Data Distribution"
    ),
}
