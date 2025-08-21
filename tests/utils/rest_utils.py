"""This module contains rest utility functions for acceptance tests."""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
import traceback
from itertools import chain

import requests
import urllib3
from requests import ConnectTimeout, ReadTimeout

from tests import (
    DEFAULT_HEADERS,
    LUMA_REST_PATH_PREFIX,
    OZ_REST_PATH_PREFIX,
    PANEL_REST_PATH_PREFIX,
    PROVIDER_REST_PATH_PREFIX,
    TOKEN_DISPENSER_PATH_PREFIX,
)

from .http_exceptions import HTTPServiceUnavailable, raise_http_exception

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_zone_rest_path(*args):
    return "/".join(chain([OZ_REST_PATH_PREFIX], args))


def get_panel_rest_path(*args):
    return "/".join(chain([PANEL_REST_PATH_PREFIX], args))


def get_provider_rest_path(*args):
    return "/".join(chain([PROVIDER_REST_PATH_PREFIX], args))


def get_luma_rest_path(*args):
    return "/".join(chain([LUMA_REST_PATH_PREFIX], args))


def get_token_dispenser_rest_path(*args):
    return "/".join(chain([TOKEN_DISPENSER_PATH_PREFIX], args))


def http_get(
    ip,
    port,
    path,
    use_ssl=True,
    headers=None,
    verify=False,
    cert=None,
    auth=None,
    default_headers=True,
    params=None,
):
    return http_request(
        requests.get,
        ip,
        port,
        path,
        use_ssl,
        headers,
        verify,
        cert,
        auth,
        default_headers=default_headers,
        params=params,
    )


def http_put(
    ip,
    port,
    path,
    use_ssl=True,
    data=None,
    headers=None,
    verify=False,
    cert=None,
    auth=None,
    default_headers=True,
    params=None,
):
    return http_request(
        requests.put,
        ip,
        port,
        path,
        use_ssl,
        headers,
        verify,
        cert,
        auth,
        data,
        default_headers=default_headers,
        params=params,
    )


def http_post(
    ip,
    port,
    path,
    use_ssl=True,
    data=None,
    headers=None,
    verify=False,
    cert=None,
    auth=None,
    default_headers=True,
    params=None,
    stream=False,
):
    return http_request(
        requests.post,
        ip,
        port,
        path,
        use_ssl,
        headers,
        verify,
        cert,
        auth,
        data,
        default_headers=default_headers,
        params=params,
        stream=stream,
    )


def http_delete(
    ip,
    port,
    path,
    use_ssl=True,
    headers=None,
    verify=False,
    cert=None,
    auth=None,
    default_headers=True,
    params=None,
    data=None,
):
    return http_request(
        requests.delete,
        ip,
        port,
        path,
        use_ssl,
        headers,
        verify,
        cert,
        auth,
        default_headers=default_headers,
        params=params,
        data=data,
    )


def http_patch(
    ip,
    port,
    path,
    use_ssl=True,
    data=None,
    headers=None,
    verify=False,
    cert=None,
    auth=None,
    default_headers=True,
    params=None,
):
    return http_request(
        requests.patch,
        ip,
        port,
        path,
        use_ssl,
        headers,
        verify,
        cert,
        auth,
        data,
        default_headers=default_headers,
        params=params,
    )


def http_request(  # pylint: disable=inconsistent-return-statements
    http_method,
    ip,
    port,
    path,
    use_ssl=True,
    headers=None,
    verify=False,
    cert=None,
    auth=None,
    data=None,
    default_headers=True,
    params=None,
    stream=False,
    retries=5,
):
    protocol = "https" if use_ssl else "http"
    request_headers = DEFAULT_HEADERS.copy() if default_headers else {}
    if headers:
        request_headers.update(headers)
    for i in range(retries):
        try:
            response = http_method(
                f"{protocol}://{ip}:{port}{path}",
                verify=verify,
                headers=request_headers,
                timeout=40,
                cert=cert,
                auth=auth,
                data=data,
                params=params,
                stream=stream,
            )
            if 200 <= response.status_code < 300:
                return response
            raise_http_exception(response)
        except HTTPServiceUnavailable as e:
            if i == retries - 1:
                raise e
            time.sleep(5.0)
        # pylint: disable=line-too-long,duplicate-except
        except (ConnectTimeout, ReadTimeout, HTTPServiceUnavailable):
            print(
                r"""
             _    _ _______ _______ _____           _____          _      _              _    _ _    _ _   _  _____    _ _ _ 
            | |  | |__   __|__   __|  __ \         / ____|   /\   | |    | |            | |  | | |  | | \ | |/ ____|  | | | |
            | |__| |  | |     | |  | |__) |       | |       /  \  | |    | |            | |__| | |  | |  \| | |  __   | | | |
            |  __  |  | |     | |  |  ___/        | |      / /\ \ | |    | |            |  __  | |  | | . ` | | |_ |  | | | |
            | |  | |  | |     | |  | |            | |____ / ____ \| |____| |____        | |  | | |__| | |\  | |__| |  |_|_|_|
            |_|  |_|  |_|     |_|  |_|             \_____/_/    \_\______|______|       |_|  |_|\____/|_| \_|\_____/  (_|_|_)
            """
            )
            traceback.print_stack()
            print("Test will freeze to allow debugging!")
            while True:
                time.sleep(365 * 24 * 60 * 60)
