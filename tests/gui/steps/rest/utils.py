"""This module contains rest utility functions for gui acceptance tests.
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from itertools import chain

import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from tests import (OZ_REST_PATH_PREFIX, PANEL_REST_PATH_PREFIX, DEFAULT_HEADERS,
                   PROVIDER_REST_PATH_PREFIX)
from .exceptions import raise_http_exception


def get_zone_rest_path(*args):
    return '/'.join(chain([OZ_REST_PATH_PREFIX], args))


def get_panel_rest_path(*args):
    return '/'.join(chain([PANEL_REST_PATH_PREFIX], args))


def get_provider_rest_path(*args):
    return '/'.join(chain([PROVIDER_REST_PATH_PREFIX], args))


def http_get(ip, port, path, use_ssl=True, headers=None, verify=False,
             cert=None, auth=None, default_headers=True):
    return http_request(requests.get, ip, port, path, use_ssl, headers,
                        verify, cert, auth, default_headers=default_headers)


def http_put(ip, port, path, use_ssl=True, data=None, headers=None,
             verify=False, cert=None, auth=None, default_headers=True):
    return http_request(requests.put, ip, port, path, use_ssl, headers,
                        verify, cert, auth, data, default_headers=default_headers)


def http_post(ip, port, path, use_ssl=True, data=None, headers=None,
              verify=False, cert=None, auth=None, default_headers=True):
    return http_request(requests.post, ip, port, path, use_ssl, headers,
                        verify, cert, auth, data, default_headers=default_headers)


def http_delete(ip, port, path, use_ssl=True, headers=None, verify=False,
                cert=None, auth=None, default_headers=True):
    return http_request(requests.delete, ip, port, path, use_ssl, headers,
                        verify, cert, auth, default_headers=default_headers)


def http_patch(ip, port, path, use_ssl=True, data=None, headers=None,
               verify=False, cert=None, auth=None, default_headers=True):
    return http_request(requests.patch, ip, port, path, use_ssl, headers,
                        verify, cert, auth, data, default_headers=default_headers)


def http_request(http_method, ip, port, path, use_ssl=True, headers=None,
                 verify=False, cert=None, auth=None, data=None, 
                 default_headers=True):
    protocol = 'https' if use_ssl else 'http'
    request_headers = DEFAULT_HEADERS.copy() if default_headers else {}
    if headers:
        request_headers.update(headers)
    response = http_method('{0}://{1}:{2}{3}'.format(protocol, ip, port, path),
                           verify=verify, headers=request_headers, timeout=20,
                           cert=cert, auth=auth, data=data)
    if 200 <= response.status_code < 300:
        return response
    else:
        raise_http_exception(response)
