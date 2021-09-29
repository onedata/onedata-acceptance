"""This module contains steps for operations on tokens in Onezone
using REST.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

import yaml
import base64

from tests.mixed.onezone_client import TokenApi
from tests.mixed.utils.common import login_to_oz
from tests.utils.bdd_utils import wt, parsers


def create_token_with_config_rest(user, config, users, tokens, hosts,
                                  tmp_memory, groups, spaces):
    """Create token according to given config.

        Config format given in yaml is as follow:

                name: token_name
                type: access/identity/invite
                invite type: type_of_invite
                invite target: target of invite        ---> optional
                usage limit: number > 0 or infinity    ---> optional, default:
                                                                      infinity
                caveats:                               ---> optional
                    caveat_type_1:
                        caveat config:
                ...

        Example configuration:

              type: invite
              invite type: Invite harvester to space
              invite target: space1
              usage limit: infinity
              caveats:
                expiration:
                    after: count (in minutes)
                region:
                    allow: True/False, default True
                    region codes:
                        - Europe
                        - Asia
                IP:
                  - 127.0.0.1
                consumer:
                  - type: group
                    by: id
                    consumer name: group2
                  - type: user
                    by: name
                    consumer name: user1

        """
    _create_token_with_config(user, config, users, hosts, tmp_memory,
                              tokens, groups, spaces, zone_name='onezone')


translation_dict = {
    'Invite user to space': {'type': 'userJoinSpace', 'target': 'spaceId'}
}


def _create_token_with_config(user, config, users, hosts, tmp_memory, tokens,
                              groups, spaces, zone_name):
    data = yaml.load(config)
    name = data['name']
    token_type = data['type']
    usage_limit = data.get('usage limit', False)
    caveats = data.get('caveats', False)

    token_config = {"name": name, "type": {f"{token_type}Token": {}}}

    if token_type == 'invite':
        invite_type = data.get('invite type')
        invite_target = data.get('invite target', None)

        invite_type_rest = translation_dict[invite_type]['type']

        token_config['type']['inviteToken']['inviteType'] = invite_type_rest
        if invite_target:
            target = translation_dict[invite_type]['target']
            if 'space' in invite_target:
                invite_target = spaces[invite_target]
            token_config['type']['inviteToken'][target] = invite_target

    if usage_limit:
        token_config['usageLimit'] = usage_limit
    if caveats:
        parse_token_caveats(caveats, token_config, groups, users, spaces,
                            tmp_memory)

    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    token_api = TokenApi(user_client)
    response = token_api.create_named_token_for_current_user(
        data=token_config)
    token = response.token
    token_id = response.token_id
    tmp_memory[user]['token'] = token
    tokens[name] = {'token_id': token_id, 'token': token}


def parse_token_caveats(caveats, token_config, groups, users, spaces,
                        tmp_memory):
    token_config['caveats'] = []
    expiration = caveats.get('expiration', False)
    region = caveats.get('region', False)
    country = caveats.get('country', False)
    asn = caveats.get('ASN', False)
    ip = caveats.get('IP', False)
    consumer = caveats.get('consumer', False)
    service = caveats.get('service', False)
    interface = caveats.get('interface', False)
    readonly = caveats.get('read only', False)
    path = caveats.get('path', False)
    object_id = caveats.get('object ID', False)

    if expiration:
        set_expiration_caveat(token_config, expiration, tmp_memory)
    if region:
        set_geo_caveat(token_config, region, 'region')
    if country:
        set_geo_caveat(token_config, country, 'country')
    if asn:
        set_address_caveat(token_config, asn, 'ASN')
    if ip:
        set_address_caveat(token_config, ip, 'IP')
    if consumer:
        set_consumer_caveat(token_config, consumer, groups, users)
    if service:
        set_service_caveat(token_config, service)
    if interface:
        set_interface_caveat(token_config, interface)
    if readonly:
        set_readonly_caveat(token_config)
    if path:
        set_path_caveat(token_config, path, spaces)
    if object_id:
        set_object_id_caveat(token_config, object_id)


def set_expiration_caveat(token_config, expiration, tmp_memory):
    time_to = int(time.time()) + expiration['after'] * 60
    token_config['caveats'].append({"type": "time", "validUntil": time_to})
    tmp_memory['expire_time'] = time.strftime('%Y/%m/%d %-H:%M', time.localtime(
        time_to))


def set_geo_caveat(token_config, caveat, geo_type):
    regions = caveat.get(f'{geo_type} codes', [])
    if caveat.get('allow', False):
        token_config['caveats'].append({"type": f"geo.{geo_type}",
                                        "filter": "whitelist",
                                        "list": regions})
    else:
        token_config['caveats'].append(
            {"type": f"geo.{geo_type}", "filter": "blacklist", "list": regions})


def set_address_caveat(token_config, caveat, address_type):
    token_config['caveats'].append({"type": address_type.lower(),
                                    "whitelist": caveat})


def set_consumer_caveat(token_config, caveat, groups, users):
    consumer_list = []
    for consumer in caveat:
        consumer_list.append(set_consumer_in_consumer_caveat(consumer, groups,
                             users))
    token_config['caveats'].append({"type": "consumer", "whitelist":
                                    consumer_list})


def set_consumer_in_consumer_caveat(consumer, groups, users):
    cons_type = consumer.get('type', 'user')
    cons_name = consumer.get('consumer name')
    if cons_type == 'user':
        value = (
            'usr-*' if 'any' in cons_name else f'usr-{users[cons_name].id}')
    elif cons_type == 'group':
        value = ('grp-*' if 'any' in cons_name else f'grp-{groups[cons_name]}')
    else:
        value = 'prv-*'
    return value


def set_service_caveat(token_config, given_service):
    services_list = []
    service = given_service.get('Service', False)
    op_service = given_service.get('Service Onepanel', False)
    if service:
        for curr_service in service:
            if curr_service == 'Any Oneprovider':
                services_list.append('opw-*')
            else:
                if curr_service == 'dev-onezone':
                    curr_service = 'onezone'
                services_list.append(f'ozw-{curr_service}')
    if op_service:
        for curr_service in op_service:
            if 'onezone' in curr_service.lower():
                services_list.append('ozp-onezone')
            if 'oneprovider onepanel' in curr_service.lower():
                services_list.append('opp-*')
            elif 'oneprovider' in curr_service.lower():
                services_list.append(f'opw-{curr_service}')

    token_config['caveats'].append({"type": "service", "whitelist":
                                    services_list})


def set_interface_caveat(token_config, service):
    token_config['caveats'].append({"type": "interface",
                                    "interface": service.lower()})


def set_readonly_caveat(token_config):
    token_config['caveats'].append({"type": "data.readonly"})


def set_path_caveat(token_config, paths, spaces):
    whitelist = []
    for path in paths:
        whitelist.append(decode_path(path, spaces))
    token_config['caveats'].append({"type": "data.path",
                                    "whitelist": whitelist})


def decode_path(path, spaces):
    space = spaces[path['space']]
    path = path['path']
    path = '' if path == '/' else path
    can_path = f'/{space}{path}'
    encoded = base64.b64encode(can_path.encode('ascii'))
    return encoded.decode('ascii')


def set_object_id_caveat(token_config, object_ids):
    whitelist = [o_id for o_id in object_ids]
    token_config['caveats'].append({"type": "data.objectid",
                                    "whitelist": whitelist})


def revoke_token_rest(user, users, hosts, zone_name, tokens, token_name):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    token_api = TokenApi(user_client)

    token = tokens.get(token_name, None)
    if token:
        token_id = token['token_id']
    else:
        token_id = token_api.get_named_token_of_current_user_by_name(
            token_name).id
    token_config = {"revoked": True}
    token_api.modify_named_token(id=token_id, data=token_config)


def assert_token_with_config_rest(user, config, users, hosts,
                                  tmp_memory, groups, spaces,
                                  zone_name='onezone'):
    data = yaml.load(config)

    name = data['name']
    token_type = data['type']
    invite_type = data.get('invite type', False)
    privileges = data.get('privileges', False)
    caveats = data.get('caveats', False)

    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    token_api = TokenApi(user_client)
    response = token_api.get_named_token_of_current_user_by_name(name)

    assert_token_type(token_type.lower(), response)
    if invite_type:
        assert_invite_type(invite_type, response)
    if caveats:
        assert_token_caveats(caveats, response, groups, users, spaces,
                             tmp_memory)
    if privileges:
        assert_token_privileges(privileges, response)


def assert_token_type(token_type, token):
    assert getattr(token.type, f'{token_type}_token') is not None, (
        f'token is not {token_type}')


def assert_invite_type(invite_type, token):
    actual = token.type.invite_token.invite_type
    expected = translation_dict[invite_type]['type']
    assert actual == expected, (f'Invite token invite type {actual} is not as ' 
                                f'expected {expected}')


def get_caveat(caveat_name, caveats):
    caveat = [cav for cav in caveats if cav['type'] == caveat_name][0]
    assert len(caveat), f'Caveat {caveat_name} not in token configuration'
    return caveat


def assert_token_caveats(caveats, token, groups, users, spaces, tmp_memory):
    expiration = caveats.get('expiration', False)
    region = caveats.get('region', False)
    country = caveats.get('country', False)
    asn = caveats.get('ASN', False)
    ip = caveats.get('IP', False)
    consumer = caveats.get('consumer', False)
    service = caveats.get('service', False)
    interface = caveats.get('interface', False)
    readonly = caveats.get('read only', False)
    path = caveats.get('path', False)
    object_id = caveats.get('object ID', False)

    if expiration:
        assert_expiration_caveat(get_caveat('time', token.caveats),
                                 expiration, tmp_memory)
    if region:
        assert_geo_caveat(get_caveat('geo.region', token.caveats), region,
                          'region')
    if country:
        assert_geo_caveat(get_caveat('geo.country', token.caveats), country,
                          'country')
    if asn:
        assert_address_caveat(get_caveat('asn', token.caveats), asn, 'ASN')
    if ip:
        assert_address_caveat(get_caveat('ip', token.caveats), ip, 'IP')
    if consumer:
        assert_consumer_caveat(get_caveat('consumer', token.caveats), consumer,
                               groups, users)
    if service:
        assert_service_caveat(get_caveat('service', token.caveats), service)
    if interface:
        assert_interface_caveat(get_caveat('interface', token.caveats),
                                interface)
    if readonly:
        get_caveat('data.readonly', token.caveats)
    if path:
        assert_path_caveat(get_caveat('data.path', token.caveats), path, spaces)
    if object_id:
        assert_object_id_caveat(get_caveat('data.objectid', token.caveats),
                             object_id)


def assert_expiration_caveat(token_caveat, expiration, tmp_memory):
    if expiration['set']:
        exp_time = tmp_memory['expire_time']
        if '/' in exp_time:
            str_time = time.strptime(exp_time, '%Y/%m/%d %H:%M')
            exp_time = time.mktime(str_time)
        assert token_caveat['validUntil'] == exp_time, (
            f'Wrong expiration time caveat: exp: {exp_time}, '
            f'given: {token_caveat}')


def assert_geo_caveat(token_caveat, expected_caveat, geo_type):
    regions = expected_caveat.get(f'{geo_type} codes', [])
    if expected_caveat.get('allow', False):
        assert token_caveat['filter'] == 'whitelist', (f'{geo_type} caveat is '
                                                       'blacklisted '
                                                       'while should be '
                                                       'whitelisted')
    else:
        assert token_caveat['filter'] == 'blacklist', (f'{geo_type} caveat is '
                                                       'whitelisted '
                                                       'while should be '
                                                       'blacklisted')
    token_list = token_caveat['list']
    assert len(token_list) == len(regions), (
        f'Token {geo_type} list {token_list} is not as long as expected '
        f'{regions}')
    for region in regions:
        assert region in token_list, (
            f'{geo_type} {region} not in token caveat')


def assert_address_caveat(token_caveat, expected_caveat, address_type):
    assert len(token_caveat['whitelist']) == len(expected_caveat), (
        f'Expected {address_type} caveat list {expected_caveat} is '
        'not as long as actual token_caveat whitelist '
        f'{token_caveat["whitelist"]}')
    for address in expected_caveat:
        assert address in token_caveat['whitelist'], (
            f'{address}  {address_type} address not in token caveat')


def assert_consumer_caveat(token_caveat, expected_caveat, groups, users):
    token_list = token_caveat['whitelist']
    assert len(token_list) == len(expected_caveat), (
        f'Expected consumer caveat list {expected_caveat} is '
        f'not as long as actual token caveat whitelist {token_list}')

    for consumer in expected_caveat:
        assert_consumer_in_consumer_caveat(consumer, token_list, groups, users)


def assert_consumer_in_consumer_caveat(consumer, token_list, groups, users):
    value = set_consumer_in_consumer_caveat(consumer, groups, users)
    assert value in token_list, f'{consumer} not in consumer token caveat'


def assert_service_caveat(token_caveat, expected_caveat):
    services_list = []
    token_list = token_caveat['whitelist']
    services = [service for service in expected_caveat if 'Onepanel' not in
                service]
    op_service = [service for service in expected_caveat if 'Onepanel' in
                  service]

    for curr_service in services:
        if curr_service == 'Any Oneprovider':
            services_list.append('opw-*')
        else:
            services_list.append(f'ozw-{curr_service}')
    for curr_service in op_service:
        if 'onezone' in curr_service.lower():
            services_list.append('ozp-onezone')
        if 'oneprovider onepanel'in curr_service.lower():
            services_list.append('opp-*')
        elif 'oneprovider' in curr_service.lower():
            services_list.append(f'opw-{curr_service}')

    assert len(token_list) == len(services_list), (
        f'Expected {services_list} and actual {token_list} '
        'services lists have different length')

    for service in services_list:
        assert service in token_list, (f'Expected service {service} not in' 
                                       f' {token_list}')


def assert_interface_caveat(token_caveat, expected_caveat):
    assert token_caveat['interface'] == expected_caveat.lower(), (
        f'Interface {expected_caveat} not set in token caveat')


def assert_path_caveat(token_caveat, expected_caveat, spaces):
    token_list = token_caveat['whitelist']
    whitelist = []
    for path in expected_caveat:
        decoded_path = decode_path(path, spaces)
        whitelist.append(decoded_path)

        assert decoded_path in token_list, (f'Path {path} not in '
                                            f'{token_list}')

    assert len(token_list) == len(whitelist), (
        f'Expected {whitelist} and actual {token_list} '
        'paths lists have different length')


def assert_object_id_caveat(token_caveat, expected_caveat):
    token_list = token_caveat['whitelist']
    assert len(token_list) == len(expected_caveat), (
        f'Expected objectID caveat list {expected_caveat} is '
        f'not as long as actual token caveat whitelist {token_list}')

    for object_id in expected_caveat:
        assert object_id in token_list, f'Object id {object_id} not in token'


privileges_translation = {
    'Space management': {
        'View space': 'space_view',
        },
    'Data management': {
        'Read files': 'space_read_data',
        'Write files': 'space_write_data',
    },
    'Transfer management': {
        'View transfers': 'space_view_transfers'
    }
}


def assert_token_privileges(privileges, response):
    actual_privs = response.metadata.privileges
    expected_privs = []
    for (priv_group, priv_group_items) in privileges.items():
        sub_privs = priv_group_items['privilege subtypes']
        for priv in sub_privs:
            if sub_privs[priv]:
                expected_privs.append(privileges_translation[priv_group][priv])

    for priv in expected_privs:
        assert priv in actual_privs, f'{priv} not in {actual_privs}'
    assert len(expected_privs) == len(actual_privs), ('Expected and actual '
                                                      'privileges lists are '
                                                      'not equal')
