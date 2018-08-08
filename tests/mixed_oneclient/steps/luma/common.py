"""This module contains gherkin steps for operations on LUMA.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import yaml
from pytest_bdd import parsers, given
from tests.gui.steps.rest.utils import http_put, http_post, get_luma_rest_path
from tests import LUMA_REST_PORT

from tests.utils.acceptance_utils import *


@given(parsers.re('created LUMA mappings:\n(?P<config>(.|\s)+)'))
def create_luma_mappings(config, users, spaces):
    config = yaml.load(config)
    [(spacename, gid)] = config['space_gid'].items()
    space_id = spaces[spacename]
    luma_ip = get_pod_ip(get_pod_names_matching_regexp('luma')[0])
    storage_name = config['storage_name']
    storage_type = config['storage_type']
    http_put(ip=luma_ip, port=LUMA_REST_PORT,
             path=get_luma_rest_path('admin', 'spaces',
                                     space_id, 'default_group'),
             data=json.dumps([{'gid': gid,
                              'storageName': storage_name}]),
             use_ssl=False)
    for username, uid in config['users'].items():
        r = http_post(ip=luma_ip, port=LUMA_REST_PORT,
                      path=get_luma_rest_path('admin', 'users'),
                      data=json.dumps({'id': users[username].id}),
                      use_ssl=False)
        _, luma_id = r.headers['Location'].rsplit('/', 1)
        http_put(ip=luma_ip, port=LUMA_REST_PORT,
                 path=get_luma_rest_path('admin', 'users', luma_id,
                                         'credentials'),
                 data=json.dumps([{'storageName': storage_name,
                                   'type': storage_type,
                                   'uid': uid,
                                   'gid': uid}]),
                 use_ssl=False)
