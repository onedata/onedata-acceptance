"""Utils for managing REST API for CDMI service
"""

import json

from tests import OP_REST_PORT
from tests.utils.rest_utils import (http_get, http_put)

__author__ = "Bartosz Walkowicz, Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


class CDMIClient(object):
    def __init__(self, provider_ip, auth, cdmi_version = '1.1.1', 
                 port = OP_REST_PORT):
        self.ip = provider_ip
        # We use token header to authenticate
        self.auth_header={'X-Auth-Token' : auth}
        self.cdmi_version = cdmi_version
        self.port = port


    def create_file(self, path, text=''):
        path='/cdmi{}'.format(path)
        headers = {'X-CDMI-Specification-Version': self.cdmi_version,
                   'content-type': 'application/cdmi-object'}
        headers.update(self.auth_header)
        return http_put(self.ip, self.port, path, headers=headers,
                        json={"value": text}, default_headers=False)


    def write_to_file(self, path, text, offset=0):
        start = offset
        end = start + len(text) - 1
        path = '/cdmi{}'.format(path)
        headers = {'Content-Type': 'application/binary',
                   'content-range': 'bytes {start}-{end}/*'.format(start=start,
                                                                   end=end)}
        headers.update(self.auth_header)
        return http_put(self.ip, self.port, path, headers=headers,
                        data=text, default_headers=False)


    def read_from_file(self, path, read_range=None):
        path = '/cdmi{}'.format(path)
        headers = {}
        if read_range:
            headers['Range'] = 'bytes={start}-{end}'.format(start=read_range[0],
                                                            end=read_range[1])
        headers.update(self.auth_header)
        return http_get(self.ip, self.port, path, headers=headers,
                        default_headers=False).content


    def read_metadata(self, path, metadata=""):
        path = '/cdmi{path}?metadata:{metadata}'.format(path = path, 
                                                        metadata = metadata)
        headers = {'X-CDMI-Specification-Version': self.cdmi_version}
        headers.update(self.auth_header)
        return http_get(self.ip, self.port, path, headers=headers,
                        default_headers=False).json()


    def write_metadata(self, path, metadata, content_type):
        path = '/cdmi{}'.format(path)
        headers = {'Content-Type': content_type,
                   'X-CDMI-Specification-Version': self.cdmi_version}
        headers.update(self.auth_header)
        data = {'metadata': metadata}
        return http_put(self.ip, self.port, path, headers=headers,
                        data = json.dumps(data), default_headers=False)
