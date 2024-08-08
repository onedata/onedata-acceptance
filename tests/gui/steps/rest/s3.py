"""Steps for amazon s3 buckets usage.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import requests
import hashlib
import hmac
from datetime import datetime

from requests.exceptions import HTTPError

from tests.gui.conftest import WAIT_BACKEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


# HOST_URL = 'volume-s3.dev-volume-s3-krakow.default:9000'
HOST_URL = 'dev-volume-s3-krakow.default:9000'

ACCESS_KEY = 'accessKey'
SECRET_KEY = 'verySecretKey'


@wt(parsers.parse('using REST, user creates s3 bucket "{bucket_name}"'))
def create_s3_bucket_rest(bucket_name):
    try:
        create_bucket(bucket_name)
    except HTTPError as e:
        # if bucket already exists do not throw exception
        if e.response.status_code == 409:
            pass
        else:
            raise e


@wt(parsers.parse('using REST, user of {browser_id} copies item with '
                  'recently copied path from "{src_bucket}" bucket into '
                  '"{dst_bucket}" bucket'))
def copy_item_s3_bucket(browser_id, dst_bucket, src_bucket, clipboard, displays):
    path = clipboard.paste(display=displays[browser_id])
    copy_item_between_buckets(dst_bucket, f'{src_bucket}{path}/999999',
                              f'{path[1::]}/999999')


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def get_signature_key(key, date_stamp):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, 'eu-central-1')
    k_service = sign(k_region, 's3')
    k_signing = sign(k_service, 'aws4_request')
    return k_signing


def create_canonical_request(method, uri, query_string, headers,
                             signed_headers, payload_hash):
    canonical_headers = ''.join(f'{k}:{v}\n' for k, v in sorted(headers.items()))
    return (f"{method}\n"
            f"{uri}\n"
            f"{query_string}\n"
            f"{canonical_headers}\n"
            f"{signed_headers}\n"
            f"{payload_hash}")


def create_string_to_sign(date_stamp, credential_scope,
                          hashed_canonical_request):
    return (f"AWS4-HMAC-SHA256\n"
            f"{date_stamp}\n"
            f"{credential_scope}\n"
            f"{hashed_canonical_request}")


def create_authorization_header(access_key, credential_scope, signed_headers,
                                signature):
    return (f"AWS4-HMAC-SHA256 Credential={access_key}/{credential_scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}")


def s3_authorization(headers, canonical_uri, canonical_querystring, payload_hash,
                     date_stamp, amz_date):
    signed_headers = ';'.join(headers.keys())
    canonical_request = create_canonical_request('PUT', canonical_uri,
                                                 canonical_querystring, headers,
                                                 signed_headers, payload_hash)
    hashed_canonical_request = hashlib.sha256(
        canonical_request.encode('utf-8')).hexdigest()
    credential_scope = f'{date_stamp}/eu-central-1/s3/aws4_request'
    string_to_sign = create_string_to_sign(amz_date, credential_scope,
                                           hashed_canonical_request)
    signing_key = get_signature_key(SECRET_KEY, date_stamp)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'),
                         hashlib.sha256).hexdigest()

    authorization_header = create_authorization_header(
        ACCESS_KEY, credential_scope, signed_headers, signature)
    return authorization_header


def create_bucket(bucket_name):
    amz_date = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    date_stamp = datetime.utcnow().strftime('%Y%m%d')
    payload_hash = 'UNSIGNED-PAYLOAD'
    canonical_uri = f'/{bucket_name}'
    canonical_querystring = ''
    headers = {
        'host': HOST_URL,
        'x-amz-content-sha256': payload_hash,
        'x-amz-date': amz_date,
    }

    authorization_header = s3_authorization(
        headers, canonical_uri, canonical_querystring, payload_hash, date_stamp,
        amz_date)

    headers['Authorization'] = authorization_header

    url = f'http://{HOST_URL}{canonical_uri}'
    response = requests.put(url, headers=headers)

    response.raise_for_status()


def copy_item_between_buckets(dst_bucket, src, dst):
    amz_date = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    date_stamp = datetime.utcnow().strftime('%Y%m%d')
    payload_hash = 'UNSIGNED-PAYLOAD'
    canonical_uri = f'/{dst_bucket}/{dst}'
    canonical_querystring = ''

    headers = {
        'host': f'{dst_bucket}.s3.amazonaws.com',
        'x-amz-content-sha256': payload_hash,
        'x-amz-copy-source': f'/{src}',
        'x-amz-date': amz_date,
    }
    authorization_header = s3_authorization(
        headers, canonical_uri, canonical_querystring, payload_hash, date_stamp,
        amz_date)

    headers['Authorization'] = authorization_header

    url = f'http://{HOST_URL}{canonical_uri}'
    response = requests.put(url, headers=headers)

    response.raise_for_status()
