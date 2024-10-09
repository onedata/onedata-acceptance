"""Utils for managing REST API for CDMI service"""

import json

from tests import OP_REST_PORT
from tests.utils.rest_utils import http_get, http_put

__author__ = "Bartosz Walkowicz, Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


CONTAINER_TYPE = "container"
OBJECT_TYPE = "object"


def get_item_type(item_path):
    return (
        "container" if item_path.split("/")[-1].startswith("dir") else "object"
    )


def get_content_type(item_type):
    return "application/cdmi-{}".format(item_type)


def parse_path(path, item_type, add_cdmi_prefix=False):
    if item_type == "container" and path[-1] != "/":
        parsed_path = "{}/".format(path)
    else:
        parsed_path = path

    if path[0] != "/":
        parsed_path = "/{}".format(parsed_path)

    if add_cdmi_prefix:
        parsed_path = "/cdmi{}".format(parsed_path)

    return parsed_path


class CDMIClient(object):
    def __init__(
        self, provider_ip, auth, cdmi_version="1.1.1", port=OP_REST_PORT
    ):
        self.ip = provider_ip
        # We use token header to authenticate
        self.auth_header = {"X-Auth-Token": auth}
        self.cdmi_version = cdmi_version
        self.port = port

    def create_file(self, path, text=""):
        item_type = get_item_type(path)
        parsed_path = parse_path(path, item_type, add_cdmi_prefix=True)
        headers = {
            "X-CDMI-Specification-Version": self.cdmi_version,
            "content-type": get_content_type(item_type),
        }
        headers.update(self.auth_header)
        data = {"value": text}
        return http_put(
            self.ip,
            self.port,
            parsed_path,
            headers=headers,
            data=json.dumps(data),
            default_headers=False,
        )

    def write_to_file(self, path, text, offset=0):
        start = offset
        end = start + len(text) - 1
        item_type = get_item_type(path)
        parsed_path = parse_path(path, item_type, add_cdmi_prefix=True)
        headers = {
            "Content-Type": "application/binary",
            "content-range": "bytes {start}-{end}/*".format(
                start=start, end=end
            ),
        }
        headers.update(self.auth_header)
        return http_put(
            self.ip,
            self.port,
            parsed_path,
            headers=headers,
            data=text,
            default_headers=False,
        )

    def read_from_file(self, path, read_range=None):
        item_type = get_item_type(path)
        parsed_path = parse_path(path, item_type, add_cdmi_prefix=True)
        headers = {}
        if read_range:
            headers["Range"] = "bytes={start}-{end}".format(
                start=read_range[0], end=read_range[1]
            )
        headers.update(self.auth_header)
        return http_get(
            self.ip,
            self.port,
            parsed_path,
            headers=headers,
            default_headers=False,
        ).content

    def read_metadata(self, path, metadata=""):
        item_type = get_item_type(path)
        parsed_path = parse_path(path, item_type, add_cdmi_prefix=True)
        parsed_path = "{path}?metadata:{metadata}".format(
            path=parsed_path, metadata=metadata
        )
        headers = {"X-CDMI-Specification-Version": self.cdmi_version}
        headers.update(self.auth_header)
        return http_get(
            self.ip,
            self.port,
            parsed_path,
            headers=headers,
            default_headers=False,
        ).json()

    def write_metadata(self, path, metadata):
        item_type = get_item_type(path)
        parsed_path = parse_path(path, item_type, add_cdmi_prefix=True)

        headers = {
            "Content-Type": get_content_type(item_type),
            "X-CDMI-Specification-Version": self.cdmi_version,
        }
        headers.update(self.auth_header)
        data = {"metadata": metadata}
        return http_put(
            self.ip,
            self.port,
            parsed_path,
            headers=headers,
            data=json.dumps(data),
            default_headers=False,
        )

    def move_item(self, src_path, dst_path):
        item_type = get_item_type(src_path)
        parsed_src_path = parse_path(src_path, item_type)
        parsed_dst_path = parse_path(dst_path, item_type, add_cdmi_prefix=True)
        headers = {
            "Content-Type": get_content_type(item_type),
            "X-CDMI-Specification-Version": self.cdmi_version,
        }
        headers.update(self.auth_header)
        data = {"move": parsed_src_path}
        return http_put(
            self.ip,
            self.port,
            parsed_dst_path,
            headers=headers,
            data=json.dumps(data),
            default_headers=False,
        )

    def move_item_by_id(self, src_id, dst_path):
        item_type = "container"
        parsed_src_path = f"/cdmi/cdmi_objectid/{src_id}"
        parsed_dst_path = parse_path(dst_path, item_type, add_cdmi_prefix=True)
        headers = {
            "Content-Type": get_content_type(item_type),
            "X-CDMI-Specification-Version": self.cdmi_version,
        }
        headers.update(self.auth_header)
        data = {"move": parsed_src_path}
        return http_put(
            self.ip,
            self.port,
            parsed_dst_path,
            headers=headers,
            data=json.dumps(data),
            default_headers=False,
        )

    def copy_item(self, src_path, dst_path):
        item_type = get_item_type(src_path)
        parsed_src_path = parse_path(src_path, item_type)
        parsed_dst_path = parse_path(dst_path, item_type, add_cdmi_prefix=True)

        headers = {
            "Content-Type": get_content_type(item_type),
            "X-CDMI-Specification-Version": self.cdmi_version,
        }
        headers.update(self.auth_header)
        data = {"copy": parsed_src_path}
        return http_put(
            self.ip,
            self.port,
            parsed_dst_path,
            headers=headers,
            data=json.dumps(data),
            default_headers=False,
        )
