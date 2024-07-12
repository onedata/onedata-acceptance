"""Utils to facilitate qos operations in Oneprovider using REST API.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.mixed.utils.common import *
from tests.mixed.oneprovider_client import QoSApi
from tests.mixed.steps.rest.oneprovider.data import _lookup_file_id


def create_qos_requirement_in_op_rest(user, users, hosts, host, expression,
                                      space_name, file_name):
    path = f'{space_name}/{file_name}'
    client = login_to_provider(user, users, hosts[host]['hostname'])
    file_id = _lookup_file_id(path, client)
    create_qos_requirement_in_op_by_id_rest(user, users, hosts, host,
                                            expression, file_id)


def create_qos_requirement_in_op_by_id_rest(user, users, hosts, host,
                                            expression, file_id):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    qos_api = QoSApi(client)
    data = {
            "fileId": file_id,
            "expression": expression
            }
    qos_api.add_qos_requirement(data)


def assert_qos_file_status_in_op_rest(user, users, hosts, host, space_name,
                                      file_name, option):
    path = f'{space_name}/{file_name}'
    client = login_to_provider(user, users, hosts[host]['hostname'])
    qo_s_api = QoSApi(client)
    file_id = _lookup_file_id(path, client)
    qos = qo_s_api.get_file_qos_summary(file_id).to_dict()['requirements']
    if not qos and option == 'has some':
        raise Exception('there is no qos file status for "{file_name}" in space'
                        ' "{space_name}"')
    elif qos and option == 'has not':
        raise Exception('there is qos file status for "{file_name}" in space'
                        ' "{space_name}"')


def delete_qos_requirement_in_op_rest(user, users, hosts, host, space_name,
                                      file_name):
    path = f'{space_name}/{file_name}'
    client = login_to_provider(user, users, hosts[host]['hostname'])
    qo_s_api = QoSApi(client)
    file_id = _lookup_file_id(path, client)
    qos = qo_s_api.get_file_qos_summary(file_id).to_dict()['requirements']
    for qos_id in qos:
        qo_s_api.remove_qos_requirement(qos_id)

