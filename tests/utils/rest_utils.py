"""This module contains rest utility functions for acceptance tests."""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
import traceback
from collections.abc import Callable, Mapping
from itertools import chain
from typing import Optional

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


type PathPart = str | int
Headers = Optional[Mapping[str, str]]
Params = Optional[Mapping[str, Optional[str | int | list[str]]]]
RequestData = Optional[str | bytes]
Certificate = Optional[str | tuple[str, str]]
Auth = Optional[tuple[str, Optional[str]]]
HttpMethod = Callable[..., requests.Response]


def get_zone_rest_path(*args: PathPart) -> str:
    return "/".join(chain([OZ_REST_PATH_PREFIX], map(str, args)))


def get_panel_rest_path(*args: PathPart) -> str:
    return "/".join(chain([PANEL_REST_PATH_PREFIX], map(str, args)))


def get_provider_rest_path(*args: PathPart) -> str:
    return "/".join(chain([PROVIDER_REST_PATH_PREFIX], map(str, args)))


def get_luma_rest_path(*args: PathPart) -> str:
    return "/".join(chain([LUMA_REST_PATH_PREFIX], map(str, args)))


def get_token_dispenser_rest_path(*args: PathPart) -> str:
    return "/".join(chain([TOKEN_DISPENSER_PATH_PREFIX], map(str, args)))


def http_get(
    ip: str,
    port: int,
    path: str,
    use_ssl: bool = True,
    data: RequestData = None,
    headers: Headers = None,
    verify: bool = False,
    cert: Certificate = None,
    auth: Auth = None,
    default_headers: bool = True,
    params: Params = None,
) -> requests.Response:
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
        data,
        default_headers=default_headers,
        params=params,
    )


def http_put(
    ip: str,
    port: int,
    path: str,
    use_ssl: bool = True,
    data: RequestData = None,
    headers: Headers = None,
    verify: bool = False,
    cert: Certificate = None,
    auth: Auth = None,
    default_headers: bool = True,
    params: Params = None,
) -> requests.Response:
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
    ip: str,
    port: int,
    path: str,
    use_ssl: bool = True,
    data: RequestData = None,
    headers: Headers = None,
    verify: bool = False,
    cert: Certificate = None,
    auth: Auth = None,
    default_headers: bool = True,
    params: Params = None,
    stream: bool = False,
) -> requests.Response:
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
    ip: str,
    port: int,
    path: str,
    use_ssl: bool = True,
    headers: Headers = None,
    verify: bool = False,
    cert: Certificate = None,
    auth: Auth = None,
    default_headers: bool = True,
    params: Params = None,
    data: RequestData = None,
) -> requests.Response:
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
    ip: str,
    port: int,
    path: str,
    use_ssl: bool = True,
    data: RequestData = None,
    headers: Headers = None,
    verify: bool = False,
    cert: Certificate = None,
    auth: Auth = None,
    default_headers: bool = True,
    params: Params = None,
) -> requests.Response:
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
    http_method: HttpMethod,
    ip: str,
    port: int,
    path: str,
    use_ssl: bool = True,
    headers: Headers = None,
    verify: bool = False,
    cert: Certificate = None,
    auth: Auth = None,
    data: RequestData = None,
    default_headers: bool = True,
    params: Params = None,
    stream: bool = False,
    retries: int = 5,
) -> requests.Response:
    protocol = "https" if use_ssl else "http"
    request_headers: dict[str, str] = dict(DEFAULT_HEADERS) if default_headers else {}
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
    raise RuntimeError("HTTP request was not attempted")
