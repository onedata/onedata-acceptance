"""Utils to facilitate operations on atm workflows using REST API."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import os
from functools import partial

from tests import OP_REST_PORT, OZ_REST_PORT
from tests.gui.utils.generic import upload_workflow_path
from tests.mixed.oneprovider_client.api.workflow_execution_api import (
    WorkflowExecutionApi,
)
from tests.mixed.steps.rest.oneprovider.data import _lookup_file_id, upload_file_rest
from tests.mixed.utils.common import login_to_provider
from tests.mixed.utils.example_workflow_executions import (
    ExampleWorkflowExecutionInitialStoreContent,
)
from tests.utils.bdd_utils import parsers, wt
from tests.utils.rest_utils import (
    get_provider_rest_path,
    get_zone_rest_path,
    http_get,
    http_post,
)
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "using REST, {user} uploads all workflows from "
        'automation-examples to inventory "{inventory}" in '
        '"{zone_name}" Onezone service'
    )
)
def upload_all_workflows_from_automation_examples_rest(
    hosts, zone_name, users, user, inventory, inventories, workflows, tmp_memory
):
    tmp_memory["workflows_with_input_files"] = []
    tmp_memory["workflows_without_input_files"] = []
    for f in os.listdir(upload_workflow_path()):
        workflow_name = f.split(".")[0]
        if os.path.isdir(upload_workflow_path(f)):
            tmp_memory["workflows_with_input_files"].append(workflow_name)
            dump_path = f"{upload_workflow_path(workflow_name)}/{workflow_name}.json"
        else:
            tmp_memory["workflows_without_input_files"].append(workflow_name)
            dump_path = upload_workflow_path(workflow_name + ".json")
        upload_workflow_rest(
            hosts,
            zone_name,
            users,
            user,
            inventory,
            inventories,
            workflow_name,
            dump_path,
            workflows,
        )


def upload_workflow_rest(
    hosts,
    zone_name,
    users,
    user,
    inventory_name,
    inventories,
    workflow_name,
    path,
    workflows,
):
    zone_hostname = hosts[zone_name]["hostname"]
    owner = users[user]

    with open(path) as f:
        workflow_dump = json.load(f)["revision"]

    _upload_workflow_rest(
        zone_hostname,
        owner,
        inventories[inventory_name],
        workflow_name,
        workflow_dump,
        workflows,
    )


def _upload_workflow_rest(
    zone_hostname, owner, inventory_id, workflow_name, workflow_dump, workflows
):
    workflow_schema_details = json.dumps(
        {
            "atmInventoryId": inventory_id,
            "name": workflow_name,
            "revision": workflow_dump,
        }
    )
    response = http_post(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("atm_workflow_schemas"),
        auth=(owner.username, owner.password),
        data=workflow_schema_details,
    )

    workflow_location = response.headers["location"]
    workflows[workflow_name] = workflow_location.split("/")[-1]


def get_store_schema_id_of_workflow(store_name, workflow_name):
    with open(upload_workflow_path(workflow_name + ".json")) as f:
        data = json.load(f)
    stores = data["revision"]["atmWorkflowSchemaRevision"]["_data"]["stores"]
    for store in stores:
        if store["_data"]["name"] == store_name:
            return store["_data"]["id"]
    raise RuntimeError(
        f"did not find store {store_name} in workflow dump {workflow_name}"
    )


def get_revision_num_of_workflow(workflow_name):
    with open(upload_workflow_path(workflow_name + ".json")) as f:
        data = json.load(f)
        return data["revision"]["originalRevisionNumber"]


@wt(
    parsers.parse(
        "using REST, {user} executes all workflows with example "
        'input files on space "{space}" in {host}'
    )
)
def execute_all_workflows(
    user,
    users,
    hosts,
    host,
    spaces,
    space,
    workflows,
    groups,
    workflow_executions,
    tmp_memory,
):
    client = login_to_provider(user, users, hosts[host]["hostname"])
    example_execution = ExampleWorkflowExecutionInitialStoreContent(
        partial(_lookup_file_id, user_client_op=client),
        partial(upload_file_rest, users, user, hosts, host, parent_id=spaces[space]),
        partial(get_group_id, groups),
    )
    for workflow in workflows:
        path = (
            f"{workflow}/{workflow}"
            if workflow in tmp_memory["workflows_with_input_files"]
            else workflow
        )
        if hasattr(example_execution, workflow.replace("-", "_")):
            example_initial_store_content, input_files = getattr(
                example_execution, workflow.replace("-", "_")
            )()
            for file, content in zip(input_files, example_initial_store_content):
                # map store name into store_id
                content = {
                    get_store_schema_id_of_workflow(key, path): content[key]
                    for key in content
                }
                rev_num = get_revision_num_of_workflow(path)
                wid = execute_workflow_rest(
                    user,
                    users,
                    hosts,
                    host,
                    spaces,
                    space,
                    workflow,
                    content,
                    workflows,
                    rev_number=rev_num,
                    loglevel="info",
                )
                workflow_executions[wid] = {workflow: file}
        else:
            raise AssertionError(
                f"Example execution of workflow {workflow} is not implemented"
            )


def execute_workflow_rest(
    user,
    users,
    hosts,
    host,
    spaces,
    space_name,
    workflow_name,
    stores_content,
    workflows,
    rev_number=1,
    loglevel="info",
):
    client = login_to_provider(user, users, hosts[host]["hostname"])
    workflow_execution_api = WorkflowExecutionApi(client)
    data = {
        "spaceId": spaces[space_name],
        "atmWorkflowSchemaId": workflows[workflow_name],
        "atmWorkflowSchemaRevisionNumber": rev_number,
        "storeInitialContentOverlay": stores_content,
        "loglevel": loglevel,
    }
    wid = workflow_execution_api.schedule_workflow_execution(
        data
    ).atm_workflow_execution_id
    return wid


def get_group_id(groups, group):
    return groups[group]


@wt(
    parsers.parse(
        "using REST, {user} waits for all workflow executions "
        'to finish on space "{space}" in {host}'
    )
)
@repeat_failed(interval=4, timeout=620)
def wait_for_workflow_executions(
    user, users, host, hosts, space, spaces, workflow_executions
):
    assert_all_workflow_execution_finished(
        user, users, host, hosts, space, spaces, workflow_executions
    )


def assert_all_workflow_execution_finished(
    user, users, host, hosts, space, spaces, workflow_executions
):
    assert_empty_workflow_phase(
        user, users, host, hosts, space, spaces, workflow_executions, "waiting"
    )
    assert_empty_workflow_phase(
        user, users, host, hosts, space, spaces, workflow_executions, "ongoing"
    )


def assert_empty_workflow_phase(
    user, users, host, hosts, space, spaces, workflow_executions, phase
):
    executions = list_workflow_executions(
        user, users, host, hosts, space, spaces, phase=phase
    )
    if any(executions):
        raise RuntimeError(
            f"workflows {[workflow_executions[wid] for wid in executions]} "
            f"are in {phase} state"
        )


@wt(
    parsers.parse(
        "using REST, {user} sees successful execution of all workflows in {host}"
    )
)
def assert_successful_workflow_executions(
    user, users, host, hosts, workflow_executions
):
    err_msgs = []
    for wid in workflow_executions.keys():
        mes = get_workflow_execution_details(
            user, users, host, hosts, wid, details=["name", "status"]
        )
        if mes["status"] != "finished":
            err_msgs.append((workflow_executions[wid], mes["status"]))
    if any(err_msgs):
        raise RuntimeError(f"workflows: {err_msgs} did not finish successfully")


def list_workflow_executions(
    user, users, host, hosts, space, spaces, phase="ongoing", limit=50
):
    client = login_to_provider(user, users, hosts[host]["hostname"])
    workflow_execution_api = WorkflowExecutionApi(client)
    response = workflow_execution_api.list_workflow_executions(
        spaces[space], phase=phase, limit=limit
    )
    return response.atm_workflow_executions


def get_workflow_execution_details(
    user, users, host, hosts, workflow_execution_id, details=None
):
    provider_hostname = hosts[host]["hostname"]
    # calling using swagger api does not work, because
    # 'originRunNumber' can be of value None
    response = http_get(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path(
            "automation", "execution", "workflows", workflow_execution_id
        ),
        headers={"X-Auth-Token": users[user].token},
    ).json()

    if details:
        return {detail: response[detail] for detail in details}
    return response
