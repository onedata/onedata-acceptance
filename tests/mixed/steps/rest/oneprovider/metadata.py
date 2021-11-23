"""Utils to facilitate metadata operations in Oneprovider using REST API.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import json


def assert_metadata_in_op_rest(user, users, host, hosts, cdmi, path, tab_name,
                               val):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    metadata = client.read_metadata(path)['metadata']
    if tab_name.lower() == 'basic':
        (attr, val) = val.split('=')
        assert attr in metadata, f'{path} has no {attr} {tab_name} metadata'
        assert val == metadata[attr], (f'{path} has no {attr} = {val} '
                                       f'{tab_name}')
    else:
        metadata = metadata[f'onedata_{tab_name.lower()}']
        if 'onedata_base64' in metadata:
            import base64
            metadata = metadata['onedata_base64']
            metadata = base64.b64decode(metadata.encode('ascii')).decode(
                'ascii')

        if tab_name.lower() == 'json':
            assert val == json.dumps(metadata), \
                (f'{path} has no {val} {tab_name} '
                f'metadata but "{metadata}"')
        else:
            assert val == metadata, (f'{path} has no {val} {tab_name} '
                                     f'metadata but "{metadata}"')


def set_metadata_in_op_rest(user, users, host, hosts, cdmi, path, tab_name,
                            val):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    if tab_name == 'basic':
        (attr, val) = val.split('=')
    else:
        attr = 'onedata_{}'.format(tab_name.lower())
        if tab_name.lower() == 'json':
            val = json.loads(val)
    client.write_metadata(path, {attr: val})


def remove_all_metadata_in_op_rest(user, users, host, hosts, cdmi, path):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    client.write_metadata(path, {})


def assert_no_such_metadata_in_op_rest(user, users, host, hosts, cdmi, path,
                                       tab_name, val):
    client = cdmi(hosts[host]['hostname'], users[user].token)
    metadata = client.read_metadata(path)['metadata']
    if tab_name == 'basic':
        attr, val = val.split('=')
    else:
        attr = 'onedata_{}'.format(tab_name.lower())
    try:
        metadata = metadata[attr]
    except KeyError:
        pass
    else:
        if tab_name.lower() == 'json':
            val = json.loads(val)
            for key in val:
                assert (key not in metadata or
                        metadata[key] != val[key]), ('There is {} {} metadata'
                                                     .format(val, tab_name))
        else:
            assert val != metadata, 'There is {} {} metadata'.format(val,
                                                                     tab_name)

