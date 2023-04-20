"""This module contains rest utility functions for acceptance tests.
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from itertools import chain
import time
import traceback

import requests
import urllib3

from tests import (OZ_REST_PATH_PREFIX, PANEL_REST_PATH_PREFIX, DEFAULT_HEADERS,
                   PROVIDER_REST_PATH_PREFIX, LUMA_REST_PATH_PREFIX,
                   TOKEN_DISPENSER_PATH_PREFIX)
from .http_exceptions import raise_http_exception
from requests import ConnectTimeout, ReadTimeout

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_zone_rest_path(*args):
    return '/'.join(chain([OZ_REST_PATH_PREFIX], args))


def get_panel_rest_path(*args):
    return '/'.join(chain([PANEL_REST_PATH_PREFIX], args))


def get_provider_rest_path(*args):
    return '/'.join(chain([PROVIDER_REST_PATH_PREFIX], args))


def get_luma_rest_path(*args):
    return '/'.join(chain([LUMA_REST_PATH_PREFIX], args))


def get_token_dispenser_rest_path(*args):
    return '/'.join(chain([TOKEN_DISPENSER_PATH_PREFIX], args))


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
                 default_headers=True, retries=5):
    protocol = 'https' if use_ssl else 'http'
    request_headers = DEFAULT_HEADERS.copy() if default_headers else {}
    if headers:
        request_headers.update(headers)
    try:
        response = http_method('{0}://{1}:{2}{3}'.format(protocol, ip, port, path),
                               verify=verify, headers=request_headers, timeout=40,
                               cert=cert, auth=auth, data=data)
        if 200 <= response.status_code < 300:
            return response
        else:
            raise_http_exception(response)
    except (ConnectTimeout, ReadTimeout) as t:
        print("""
         _    _ _______ _______ _____           _____          _      _              _    _ _    _ _   _  _____    _ _ _ 
        | |  | |__   __|__   __|  __ \         / ____|   /\   | |    | |            | |  | | |  | | \ | |/ ____|  | | | |
        | |__| |  | |     | |  | |__) |       | |       /  \  | |    | |            | |__| | |  | |  \| | |  __   | | | |
        |  __  |  | |     | |  |  ___/        | |      / /\ \ | |    | |            |  __  | |  | | . ` | | |_ |  | | | |
        | |  | |  | |     | |  | |            | |____ / ____ \| |____| |____        | |  | | |__| | |\  | |__| |  |_|_|_|
        |_|  |_|  |_|     |_|  |_|             \_____/_/    \_\______|______|       |_|  |_|\____/|_| \_|\_____/  (_|_|_)
        """)
        traceback.print_stack()
        print("Test will freeze for 24h to allow debuging!")
        time.sleep(24*60*60)

        if retries > 0:
            return http_request(http_method, ip, port, path, use_ssl, headers, verify, cert,
                                auth, data, default_headers, retries=retries - 1)
        raise t
