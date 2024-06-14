"""Utils to facilitate operations on atm workflows using REST API.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from functools import partial
import json
import os

from tests import OP_REST_PORT
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import upload_workflow_path
from tests.mixed.utils.common import *
from tests.mixed.oneprovider_client.api.workflow_execution_api import WorkflowExecutionApi
from tests.utils.rest_utils import (http_post, http_get, get_zone_rest_path, get_provider_rest_path)
from tests.mixed.utils.example_workflow_executions import ExampleWorkflowExecutionInitialStoreContent
from tests.mixed.steps.rest.oneprovider.data import _lookup_file_id, upload_file_rest


ATM_WORKFLOW_EXECUTION_ID = []
ALL_WORKFLOW_WITHOUT_INPUT_FILES = []
ALL_WORKFLOW_WITH_INPUT_FILES = []


@wt(parsers.parse('using REST, {user} uploads all workflows from '
                  'automation-examples to inventory "{inventory}" in '
                  '"{zone_name}" Onezone service'))
def upload_all_workflows_from_automation_examples_rest(
        hosts, zone_name, users, user, inventory, inventories, workflows):
    global ALL_WORKFLOW_WITHOUT_INPUT_FILES, ALL_WORKFLOW_WITH_INPUT_FILES
    for f in os.listdir(upload_workflow_path()):
        if os.path.isdir(upload_workflow_path(f)):
            ALL_WORKFLOW_WITH_INPUT_FILES.append(f.split('.')[0])
        else:
            ALL_WORKFLOW_WITHOUT_INPUT_FILES.append(f.split('.')[0])

    for workflow_name in ALL_WORKFLOW_WITHOUT_INPUT_FILES:
        upload_workflow_rest(hosts, zone_name, users, user, inventory,
                             inventories, workflow_name,
                             upload_workflow_path(workflow_name + '.json'), workflows)
    for workflow_name in ALL_WORKFLOW_WITH_INPUT_FILES:
        path = f'{upload_workflow_path(workflow_name)}/{workflow_name}.json'
        upload_workflow_rest(hosts, zone_name, users, user, inventory,
                             inventories, workflow_name, path, workflows)


def upload_workflow_rest(hosts, zone_name, users, user, inventory_name,
                         inventories, workflow_name, path, workflows):
    zone_hostname = hosts[zone_name]['hostname']
    owner = users[user]

    with open(path) as f:
        workflow_dump = json.load(f)['revision']

    _upload_workflow_rest(zone_hostname, owner, inventories[inventory_name],
                          workflow_name, workflow_dump, workflows)


def _upload_workflow_rest(zone_hostname, owner, inventory_id, workflow_name,
                          workflow_dump, workflows):
    workflow_schema_details = json.dumps(
        {"atmInventoryId": inventory_id,
         "name": workflow_name,
         "revision": workflow_dump}
    )
    response = http_post(ip=zone_hostname, port=OZ_REST_PORT,
                         path=get_zone_rest_path('atm_workflow_schemas'),
                         auth=(owner.username, owner.password),
                         data=workflow_schema_details)

    workflow_location = response.headers['location']
    workflows[workflow_name] = workflow_location.split('/')[-1]


def get_store_schema_id_of_workflow(store_name, workflow_name):
    with open(upload_workflow_path(workflow_name + '.json')) as f:
        data = json.load(f)
    stores = data["revision"]["atmWorkflowSchemaRevision"]["_data"]["stores"]
    for store in stores:
        if store["_data"]["name"] == store_name:
            return store["_data"]["id"]
    raise Exception(f'did not find store {store_name} in workflow '
                    f'dump {workflow_name}')


def get_revision_num_of_workflow(workflow_name):
    with open(upload_workflow_path(workflow_name + '.json')) as f:
        data = json.load(f)
        return data['revision']['originalRevisionNumber']


@wt(parsers.parse('using REST, {user} executes all workflows with example '
                  'input files on space "{space}" in {host}'))
def execute_all_workflows(user, users, hosts, host, spaces, space, workflows,
                          groups):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    example_execution = ExampleWorkflowExecutionInitialStoreContent(
        partial(_lookup_file_id, user_client_op=client),
        partial(upload_file_rest, users, user, hosts, host,
                parent_id=spaces[space]),
        partial(get_group_id, groups))
    for workflow in workflows:
        path = workflow + '/' + workflow if workflow in ALL_WORKFLOW_WITH_INPUT_FILES else workflow
        if workflow == 'bagit-uploader' or workflow == 'download-files':
            continue
        if hasattr(example_execution, workflow.replace('-', '_')):
            store_content = getattr(example_execution, workflow.replace('-', '_'))()
            for content in store_content:
                # map store name into store_id
                content = {get_store_schema_id_of_workflow(key, path):
                           content[key] for key in content}
                rev_num = get_revision_num_of_workflow(path)
                execute_workflow_rest(
                    user, users, hosts, host, spaces, space, workflow, content,
                    workflows, rev_number=rev_num, loglevel='info')
        else:
            raise Exception(f'Example execution of workflow {workflow} is '
                            f'not implemented')


def execute_workflow_rest(
        user, users, hosts, host, spaces, space_name, workflow_name,
        stores_content, workflows, rev_number=1, loglevel="info"):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    workflow_execution_api = WorkflowExecutionApi(client)
    data = {"spaceId": spaces[space_name],
            "atmWorkflowSchemaId": workflows[workflow_name],
            "atmWorkflowSchemaRevisionNumber": rev_number,
            "storeInitialContentOverlay": stores_content,
            "loglevel": loglevel}
    ATM_WORKFLOW_EXECUTION_ID.append(
        (workflow_name, workflow_execution_api.schedule_workflow_execution(
            data).atm_workflow_execution_id))


def get_group_id(groups, group):
    return groups[group]


@wt(parsers.parse('using REST, {user} waits for all workflow executions '
                  'to finish on space "{space}" in {host}'))
@repeat_failed(interval=4, timeout=620)
def wait_for_workflow_executions(user, users, host, hosts, space, spaces):
    assert_all_workflow_execution_finished(user, users, host, hosts, space,
                                           spaces)


def assert_all_workflow_execution_finished(user, users, host, hosts, space,
                                           spaces):
    executions_waiting = list_workflow_executions(
        user, users, host, hosts, space, spaces, phase='waiting')
    executions_ongoing = list_workflow_executions(
        user, users, host, hosts, space, spaces, phase='ongoing')
    if any(executions_waiting):
        raise RuntimeError(
            f'workflows with ids {executions_waiting} are in waiting state')
    if any(executions_ongoing):
        raise RuntimeError(
            f'workflows with ids {executions_ongoing} are in ongoing state')


@wt(parsers.parse('using REST, {user} sees successful execution of all '
                  'workflows in {host}'))
def assert_successful_workflow_executions(user, users, host, hosts):
    states = {}
    for (_, wid) in ATM_WORKFLOW_EXECUTION_ID:
        mes = get_workflow_execution_details(user, users, host, hosts,
                                             wid, details=['name', 'status'])
        if mes['state'] != 'finished':
            states[f'{mes["name"]}@{wid}'] = mes['state']
    if any(states):
        raise Exception(f'workflows: {states} did not finish successfully')


def list_workflow_executions(user, users, host, hosts, space, spaces,
                             phase='ongoing', limit=50):
    client = login_to_provider(user, users, hosts[host]['hostname'])
    workflow_execution_api = WorkflowExecutionApi(client)
    response = workflow_execution_api.list_workflow_executions(
        spaces[space], phase=phase, limit=limit)
    return response.atm_workflow_executions


def get_workflow_execution_details(user, users, host, hosts,
                                   workflow_execution_id, details=None):
    provider_hostname = hosts[host]['hostname']
    # calling using swagger api does not work, because
    # 'originRunNumber' can be of value None
    response = http_get(
        ip=provider_hostname, port=OP_REST_PORT, path=get_provider_rest_path(
            'automation', 'execution', 'workflows', workflow_execution_id),
        headers={'X-Auth-Token': users[user].token}).json()

    if details:
        return {detail: response[detail] for detail in details}
    return response
