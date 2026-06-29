"""This module provides utility functions for test environment management"""

from __future__ import annotations

__author__ = "Jakub Kudzia, Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2016-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import re
import subprocess as sp
import time
from collections.abc import Mapping
from typing import Literal, Optional, TypedDict, cast, overload

import pytest
import requests
import urllib3
import yaml
from requests.exceptions import ConnectTimeout

# pylint: disable=import-error,no-name-in-module
from bamboos.docker.images_branch_config import resolve_image
from tests import OZ_REST_PORT, PANEL_REST_PORT
from tests.type_definitions import Hosts, JsonObject, Users
from tests.utils.http_exceptions import HTTPError
from tests.utils.luma_utils import (
    add_spaces_luma_mapping,
    add_user_luma_mapping,
    gen_gid,
    gen_uid,
    get_all_spaces_details,
    get_local_feed_luma_storages,
)
from tests.utils.onenv_utils import (
    OnenvError,
    client_alias_to_pod_mapping,
    init_helm,
    run_command,
    run_onenv_command,
    service_name_to_alias_mapping,
)
from tests.utils.rest_utils import get_zone_rest_path, http_get
from tests.utils.user_utils import User
from tests.utils.utils import repeat_failed

START_ENV_MAX_RETRIES = 3
ONE_ENV_CONTAINER_NAME = "one-env"
ENV_READY_TIMEOUT_SECONDS = 300

type StringMapping = Mapping[str, str]


PodConfig = TypedDict(
    "PodConfig",
    {
        "name": str,
        "ip": str,
        "domain": str,
        "hostname": str,
        "container_id": str,
        "service_type": str,
        "provider_host": str,
    },
    total=False,
)


class DeploymentStatus(TypedDict, total=False):
    ready: bool
    pods: dict[str, PodConfig]


class PatchUser(TypedDict, total=False):
    name: str
    password: str
    idps: dict[str, object]


PatchConfig = TypedDict(
    "PatchConfig",
    {"users": list[PatchUser], "global": dict[str, object]},
    total=False,
)


class KubernetesMetadata(TypedDict):
    name: str
    namespace: str
    labels: dict[str, str]


class KubernetesContainerStatus(TypedDict, total=False):
    containerID: str


class KubernetesStatus(TypedDict, total=False):
    podIP: str
    containerStatuses: list[KubernetesContainerStatus]


class KubernetesPod(TypedDict):
    metadata: KubernetesMetadata
    status: KubernetesStatus


class KubernetesPods(TypedDict):
    items: list[KubernetesPod]


def start_environment(
    scenario_path: str,
    request: pytest.FixtureRequest,
    hosts: Hosts,
    patch_path: Optional[str],
    users: Users,
    test_config: Optional[JsonObject],
) -> str | OnenvError:
    attempts = 0
    local = request.config.getoption("--local")
    up_args = parse_up_args(request, test_config)
    up_args.extend([f"{scenario_path}"])
    wait_args = parse_wait_args(request)
    patch_args = parse_patch_args(request, patch_path) if patch_path else []

    dep_status: DeploymentStatus = {}
    started = False
    while not started and attempts < START_ENV_MAX_RETRIES:
        try:
            maybe_setup_helm()
            run_onenv_command("init", cwd=None, onenv_path="one-env/onenv")
            run_onenv_command("up", up_args)
            run_onenv_command("wait", wait_args)
            dep_status = get_deployment_status()
            check_deployment(dep_status)

            if not local:
                update_etc_hosts()
            setup_hosts_cfg(hosts, request)
            zone_hostname = hosts["onezone"]["hostname"]
            users["admin"] = User(zone_hostname, "admin", "password")

            if patch_path and not request.config.getoption("--no-clean"):
                run_onenv_command("patch", patch_args)
                wait_args = parse_wait_args(request)
                run_onenv_command("wait", wait_args)
                dep_status = get_deployment_status()
                check_deployment(dep_status)

            if patch_path:
                with open(patch_path, "r") as patch_file:
                    patch_cfg = yaml.load(patch_file, yaml.Loader)
                setup_users(patch_cfg, users, zone_hostname)
                add_luma_mappings(patch_cfg, users, hosts)

            started = True

        except OnenvError as e:
            attempts += 1
            if attempts >= START_ENV_MAX_RETRIES:
                return e
            clean_env()

    configure_os(scenario_path, dep_status)
    return "ok"


def maybe_setup_helm() -> None:
    is_helm_v2 = False
    try:
        helm_version_proc = sp.run(["helm", "version"], stdout=sp.PIPE, check=False)
        version_string = str(helm_version_proc.stdout)
        version2_match = re.search(r"Server:.*v2", version_string)
        if version2_match:
            is_helm_v2 = True
    except FileNotFoundError:
        is_helm_v2 = False

    if is_helm_v2:
        print("Helm version 2.x is used - invoking init helm...")
        init_helm()


def update_etc_hosts() -> None:
    """
    The 'onenv hosts' command updates entries in /etc/hosts file present in
    one-env container. This file is a docker volume mounted from host machine.
    As some tests modifies entries in /etc/hosts file, it is undesired to make
    this volume available also in test-runner container. Thus this function
    firstly updates /etc/hosts entries using the 'onenv hosts' command and then
    copies modified /etc/hosts from one-env container to test-runner container.
    """

    run_onenv_command("hosts")
    etc_hosts_path = "/etc/hosts"
    tmp_hosts_path = "/tmp/hosts"
    sp.call(
        [
            "docker",
            "cp",
            f"{ONE_ENV_CONTAINER_NAME}:{etc_hosts_path}",
            tmp_hosts_path,
        ]
    )
    sp.call(["sudo", "cp", tmp_hosts_path, etc_hosts_path])


def configure_os(scenario_path: str, dep_status: DeploymentStatus) -> None:
    """
    Function responsible for creating system users and groups in containers for
    Onezone / Oneprovider / Oneclient.

    os_configs parameter corresponds to 'os-config' section in environment
    configuration file that was generated by merging command-line arguments
    and config file passed by user to onenv_up script.
    """
    check_deployment(dep_status)
    pods_cfg = dep_status.get("pods")

    with open(scenario_path, "r") as env_file:
        env_cfg = yaml.load(env_file, yaml.Loader)
    os_configs = env_cfg.get("os-config")
    if not os_configs:
        return

    if not pods_cfg:
        return

    for pod_name, pod_cfg in pods_cfg.items():
        service_type = pod_cfg["service_type"]
        if service_type in ["onezone", "oneprovider"]:
            alias = service_name_to_alias_mapping(pod_name)
            os_config = os_configs.get("services").get(alias)
            if os_config:
                create_users_in_pod(pod_name, os_config.get("users"))
                create_groups_in_pod(pod_name, os_config.get("groups"))
        if service_type == "oneclient":
            os_config = os_configs.get("services").get("oneclient")
            if os_config:
                create_users_in_pod(pod_name, os_config.get("users"))
                create_groups_in_pod(pod_name, os_config.get("groups"))


def setup_hosts_cfg(hosts: Hosts, request: pytest.FixtureRequest) -> None:
    pods_cfg = get_pods_config()
    for pod_name, pod_cfg in pods_cfg.items():
        service_type = pod_cfg["service_type"]
        if service_type in ["onezone", "oneprovider"]:
            parse_oz_op_cfg(
                pod_name,
                pod_cfg,
                service_type,
                request.config.getoption("--add-test-domain"),
                hosts,
            )

        elif service_type == "oneclient":
            parse_client_cfg(pod_name, pod_cfg, hosts)
        elif service_type == "elasticsearch":
            parse_elasticsearch_cfg(pod_cfg, hosts)


def setup_users(patch_cfg: PatchConfig, users: Users, zone_hostname: str) -> None:
    for user_cfg in patch_cfg.get("users", []):
        user_name = user_cfg.get("name")
        if user_name is None:
            raise ValueError("Patch user must have a name")
        password = user_cfg.get("password")
        new_user = User(
            username=user_name, zone_hostname=zone_hostname, password=password
        )
        users[user_name] = new_user
        idps = user_cfg.get("idps", {})
        for idp_type in idps:
            new_user.idps.append(idp_type)
            if idp_type == "keycloak":
                global_cfg = patch_cfg.get("global")
                if global_cfg:
                    keycloak_cfg = cast(
                        Mapping[str, str], global_cfg.get("keycloakInstance", {})
                    )
                    keycloak_suffix = keycloak_cfg.get("idpName")
                    new_user.keycloak_name = f"keycloak-{keycloak_suffix}"


def add_luma_mappings(patch_cfg: PatchConfig, users: Users, hosts: Hosts) -> None:
    admin_user = users["admin"]

    spaces = get_all_spaces_details(
        admin_user, cast(Mapping[str, Mapping[str, str]], hosts)
    )
    local_feed_luma_storages = get_local_feed_luma_storages(
        admin_user, cast(Mapping[str, Mapping[str, str]], hosts)
    )

    for user_cfg in patch_cfg.get("users", []):
        user_name = user_cfg.get("name")
        if user_name is None:
            raise ValueError("Patch user must have a name")
        new_user = users[user_name]
        add_user_luma_mapping(admin_user, new_user, local_feed_luma_storages)

    add_spaces_luma_mapping(admin_user, local_feed_luma_storages, spaces)


def get_deployment_status() -> DeploymentStatus:
    status = yaml.load(run_onenv_command("status"), yaml.Loader)
    if isinstance(status, dict):
        pods = status.get("pods")
        if isinstance(pods, dict):
            status["pods"] = {
                pod_name: _normalize_pod_config(pod_cfg)
                for pod_name, pod_cfg in pods.items()
                if isinstance(pod_cfg, Mapping)
            }
    return cast(DeploymentStatus, status)


def _normalize_pod_config(pod_cfg: Mapping[str, object]) -> dict[str, object]:
    normalized = dict(pod_cfg)
    for raw_key, normalized_key in {
        "container-id": "container_id",
        "service-type": "service_type",
        "provider-host": "provider_host",
    }.items():
        if normalized_key not in normalized and raw_key in normalized:
            normalized[normalized_key] = normalized[raw_key]
    return normalized


def check_deployment(deployment_status: DeploymentStatus) -> None:
    env_ready = deployment_status.get("ready")

    if not env_ready:
        raise OnenvError(
            "Environment error: timeout while waiting for deployment to be ready."
        )


def parse_patch_args(request: pytest.FixtureRequest, patch_path: str) -> list[str]:
    patch_args = []
    local_charts_path = request.config.getoption("--local-charts-path")

    if local_charts_path:
        patch_args.extend(["-lcp", local_charts_path])

    patch_args.extend(["--patch", patch_path])
    return patch_args


def parse_wait_args(request: pytest.FixtureRequest) -> list[str]:
    wait_args = []

    timeout = request.config.getoption("--timeout")
    if timeout:
        wait_args.extend(["--timeout", timeout])
    return wait_args


def parse_up_args(
    request: pytest.FixtureRequest, test_config: Optional[JsonObject]
) -> list[str]:
    up_args = []

    option_values = [
        ("-zi", request.config.getoption("--oz-image")),
        ("-pi", request.config.getoption("--op-image")),
        ("-ci", request.config.getoption("--oc-image")),
        ("-ri", request.config.getoption("--rest-cli-image")),
        (
            "-mi",
            request.config.getoption("--openfaas-pod-status-monitor-image"),
        ),
        (
            "-si",
            request.config.getoption("--openfaas-lambda-result-streamer-image"),
        ),
    ]
    sources = request.config.getoption("--sources")
    timeout = request.config.getoption("--timeout")
    local_charts_path = request.config.getoption("--local-charts-path")
    gui_pkg_verification = request.config.getoption("--gui-pkg-verification")

    for option, value in option_values:
        if value:
            up_args.extend([option, value])
    if sources:
        up_args.append("-s")
    if local_charts_path:
        up_args.extend(["-lcp", local_charts_path])
    if timeout:
        up_args.extend(["--timeout", timeout])
    if gui_pkg_verification:
        up_args.append("--gui-pkg-verification")

    if test_config:
        for image_value, option, service_name in [
            (request.config.getoption("--oz-image"), "-zi", "onezone"),
            (request.config.getoption("--op-image"), "-pi", "oneprovider"),
            (request.config.getoption("--oc-image"), "-ci", "oneclient"),
        ]:
            if not image_value:
                initial_versions = cast(
                    Mapping[str, str],
                    cast(Mapping[str, object], test_config).get("initialVersions", {}),
                )
                version_val = initial_versions.get(service_name)
                up_args.extend(
                    [
                        option,
                        config_image_spec_to_image(
                            service_name, cast(str, version_val)
                        ),
                    ]
                )

    return up_args


def config_image_spec_to_image(service: str, version: str) -> str:
    if version == "default":
        return resolve_image(service)
    return f"docker.onedata.org/{service}-dev:{version}"


def create_users_in_pod(pod_name: str, users: list[str]) -> None:
    """Creates system users on pod specified by 'pod_name'."""

    def _user_exists(user: str, pod_name: str) -> bool:
        cmd = [pod_name, "--", "id", "-u", user]
        ret = run_kubectl_command(
            "exec", cmd, fail_with_error=False, return_output=False
        )
        return ret == 0

    for username in users:
        if _user_exists(username, pod_name):
            print(
                f"Skipping creation of user {username} - user already exists in"
                f" {pod_name}."
            )
        else:
            uid = str(gen_uid(username))
            command = [
                pod_name,
                "--",
                "adduser",
                "--disabled-password",
                "--gecos",
                '""',
                "--uid",
                uid,
                username,
            ]
            run_kubectl_command("exec", command)


def create_groups_in_pod(pod_name: str, groups: dict[str, list[str]]) -> None:
    """Creates system groups on pod specified by 'pod_name'."""

    def _group_exists(group: str, pod_name: str) -> bool:
        cmd = [pod_name, "--", "grep", "-q", group, "/etc/group"]
        ret = run_kubectl_command(
            "exec", cmd, fail_with_error=False, return_output=False
        )
        return ret == 0

    for group, users in groups.items():
        if _group_exists(group, pod_name):
            print(
                f"Skipping creation of group {group} - group already exists in"
                f" {pod_name}."
            )
        else:
            gid = str(gen_gid(group))
            command = [pod_name, "--", "groupadd", "-g", gid, group]
            run_kubectl_command("exec", command)
            for user in users:
                command = [pod_name, "--", "usermod", "-a", "-G", group, user]
                run_kubectl_command("exec", command)


def get_pods_config() -> dict[str, PodConfig]:
    pods_json = get_pods_with_kubectl()["items"]
    pods: dict[str, PodConfig] = {}
    for pod in pods_json:
        pod_data = pod["metadata"]
        pod_title = pod_data["name"]
        pod_name = pod_data["labels"].get("app", None)
        pod_service_type = pod_data["labels"].get("component", None)
        pod_service_name = pod_data["labels"].get("chart", None)
        pod_namespace = pod_data["namespace"]
        pod_ip = pod["status"].get("podIP", None)
        pod_container_id = pod["status"]["containerStatuses"][0].get(
            "containerID", None
        )
        if pod_container_id:
            pod_container_id = pod_container_id.replace("docker://", "")

        pods[pod_title] = cast(
            PodConfig,
            {
                "name": pod_name,
                "ip": pod_ip,
                "container_id": pod_container_id,
            },
        )

        pod_domain = f"{pod_name}.{pod_namespace}.svc.cluster.local"
        pod_hostname = f"{pod_title}.{pod_domain}"

        pods[pod_title]["domain"] = pod_domain
        pods[pod_title]["hostname"] = pod_hostname

        pods[pod_title]["service_type"] = cast(
            str, pod_service_type if pod_service_type else pod_service_name
        )

    return pods


def get_pods_with_kubectl() -> KubernetesPods:
    cmd = ["pods", "-o", "json"]
    output = run_kubectl_command("get", cmd, verbose=False)
    return cast(KubernetesPods, json.loads(output))


def parse_oz_op_cfg(
    pod_name: str,
    pod_cfg: PodConfig,
    service_type: str,
    add_test_domain: bool,
    hosts: Hosts,
) -> None:
    alias = service_name_to_alias_mapping(pod_name)
    name, hostname, ip, container_id = (
        pod_cfg.get("name"),
        pod_cfg.get("domain"),
        pod_cfg.get("ip"),
        pod_cfg.get("container_id"),
    )

    hosts[alias] = {
        "pod_name": pod_name,
        "service_type": service_type,
        "name": cast(str, name),
        "hostname": cast(str, hostname),
        "ip": cast(str, ip),
        "container_id": cast(str, container_id),
        "panel": {"hostname": f"{hostname}:{PANEL_REST_PORT}"},
    }
    if add_test_domain and service_type == "oneprovider":
        add_etc_hosts_entries(cast(str, ip), f"{hostname}.test")


def parse_client_cfg(pod_name: str, pod_cfg: PodConfig, hosts: Hosts) -> None:
    ip, container_id, provider_host = (
        pod_cfg.get("ip"),
        pod_cfg.get("container_id"),
        pod_cfg.get("provider_host"),
    )

    client_alias = client_alias_to_pod_mapping().get(pod_name)
    if client_alias is None:
        raise ValueError(f"Missing client alias for pod {pod_name}")
    hosts[client_alias] = {
        "ip": cast(str, ip),
        "container_id": cast(str, container_id),
        "pod_name": pod_name,
        "provider_host": cast(str, provider_host),
    }


def parse_elasticsearch_cfg(pod_cfg: PodConfig, hosts: Hosts) -> None:
    ip, container_id, name, hostname = (
        pod_cfg.get("ip"),
        pod_cfg.get("container_id"),
        pod_cfg.get("name"),
        pod_cfg.get("hostname"),
    )
    hosts["elasticsearch"] = {
        "ip": cast(str, ip),
        "container_id": cast(str, container_id),
        "name": cast(str, name),
        "hostname": cast(str, hostname),
    }


def add_etc_hosts_entries(service_ip: str, service_host: str) -> None:
    sp.call(
        f'sudo bash -c "echo {service_ip} {service_host} >> /etc/hosts"',
        shell=True,
    )


@overload
def run_kubectl_command(
    command: str,
    args: Optional[list[str]] = None,
    fail_with_error: bool = True,
    return_output: Literal[True] = True,
    verbose: bool = True,
) -> str: ...


@overload
def run_kubectl_command(
    command: str,
    args: Optional[list[str]] = None,
    fail_with_error: bool = True,
    return_output: Literal[False] = False,
    verbose: bool = True,
) -> int: ...


def run_kubectl_command(
    command: str,
    args: Optional[list[str]] = None,
    fail_with_error: bool = True,
    return_output: bool = True,
    verbose: bool = True,
) -> str | int:
    cmd = ["kubectl", command]
    if args:
        cmd.extend(args)
    return run_command(
        cmd,
        fail_with_error=fail_with_error,
        return_output=return_output,
        verbose=verbose,
    )


def clean_env() -> None:
    run_onenv_command("clean", ["-a", "-s", "-d", "-v"])


def verify_env_ready(admin_user: User, hosts: Mapping[str, object]) -> None:
    zone = cast(Mapping[str, str], hosts["onezone"])
    zone_hostname = zone["hostname"]
    ready = False
    start = time.time()
    while not ready:
        if time.time() - start > 2 * ENV_READY_TIMEOUT_SECONDS:
            raise RuntimeError("Environment not ready after upgrade")
        time.sleep(1)
        try:
            providers = get_providers_list(admin_user, zone_hostname)
            ready = all(
                is_provider_online(admin_user, zone_hostname, p) for p in providers
            )
        except (
            HTTPError,
            ConnectTimeout,
            ConnectionRefusedError,
            urllib3.exceptions.NewConnectionError,
            requests.exceptions.ConnectionError,
        ):
            # ignore those errors as they are normal when Onezone is starting
            pass


def get_providers_list(admin_user: User, zone_hostname: str) -> list[str]:
    response = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("providers"),
        headers={"X-Auth-Token": admin_user.token, "Content-Type": "application/json"},
    )
    return cast(list[str], json.loads(response.content)["providers"])


def is_provider_online(admin_user: User, zone_hostname: str, provider: str) -> bool:
    response = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("providers", provider),
        headers={"X-Auth-Token": admin_user.token, "Content-Type": "application/json"},
    )
    return cast(bool, json.loads(response.content)["online"])


@repeat_failed(timeout=60 * 4)
def wait_for_pod_running_phase(pod_name: str) -> None:
    out = run_kubectl_command(
        "get", ["pod", pod_name, "--no-headers", "-o", "json"], verbose=False
    )
    out = json.loads(out)
    assert out["status"]["phase"] == "Running"


@repeat_failed(timeout=60 * 4)
def wait_for_pod_to_stop(pod_name: str) -> None:
    try:
        _ = run_kubectl_command("get", ["pod", pod_name], verbose=False)
        raise AssertionError(f"pod: {pod_name} is still visible")
    except OnenvError:
        pass
