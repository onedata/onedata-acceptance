"""This file contains utility functions for operation using onenv tool."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import collections
import os
import re
import subprocess as sp
import sys
from typing import Literal, Optional, cast, overload

import urllib3
import yaml
from kubernetes import client, config  # pylint: disable=import-error

type Command = list[str]
type CommandResult = str | int
type YamlValue = Optional[
    str | int | float | bool | list["YamlValue"] | dict[str, "YamlValue"]
]
type YamlObject = dict[str, YamlValue]


class OnenvError(BaseException):
    """Raised when one of one-env commands fails"""


@overload
def run_onenv_command(
    command: str,
    args: Optional[list[str]] = None,
    fail_with_error: bool = True,
    sudo: bool = False,
    return_output: Literal[True] = True,
    cwd: Optional[str] = "one-env",
    onenv_path: str = "./onenv",
) -> str: ...


@overload
def run_onenv_command(
    command: str,
    args: Optional[list[str]] = None,
    fail_with_error: bool = True,
    sudo: bool = False,
    return_output: Literal[False] = False,
    cwd: Optional[str] = "one-env",
    onenv_path: str = "./onenv",
) -> int: ...


@overload
def run_onenv_command(
    command: str,
    args: Optional[list[str]] = None,
    fail_with_error: bool = True,
    sudo: bool = False,
    return_output: bool = True,
    cwd: Optional[str] = "one-env",
    onenv_path: str = "./onenv",
) -> CommandResult: ...


def run_onenv_command(
    command: str,
    args: Optional[list[str]] = None,
    fail_with_error: bool = True,
    sudo: bool = False,
    return_output: bool = True,
    cwd: Optional[str] = "one-env",
    onenv_path: str = "./onenv",
) -> CommandResult:
    if sudo:
        cmd = ["sudo", onenv_path, command]
    else:
        cmd = [onenv_path, command]

    if args:
        cmd.extend(args)
    return run_command(
        cmd, fail_with_error=fail_with_error, return_output=return_output, cwd=cwd
    )


@overload
def run_command(
    cmd: Command,
    fail_with_error: bool = True,
    return_output: Literal[True] = True,
    cwd: Optional[str] = None,
    verbose: bool = True,
) -> str: ...


@overload
def run_command(
    cmd: Command,
    fail_with_error: bool = True,
    return_output: Literal[False] = False,
    cwd: Optional[str] = None,
    verbose: bool = True,
) -> int: ...


@overload
def run_command(
    cmd: Command,
    fail_with_error: bool = True,
    return_output: bool = True,
    cwd: Optional[str] = None,
    verbose: bool = True,
) -> CommandResult: ...


def run_command(
    cmd: Command,
    fail_with_error: bool = True,
    return_output: bool = True,
    cwd: Optional[str] = None,
    verbose: bool = True,
) -> CommandResult:
    if verbose:
        print(f"Running command: {cmd}")
    with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, cwd=cwd) as proc:
        output, err = proc.communicate()

    decoded_output = output.decode("utf-8", errors="replace").strip() + "\n"
    decoded_err = err.decode("utf-8", errors="replace").strip() + "\n"

    should_throw = proc.returncode != 0 and fail_with_error

    if decoded_err != "\n":
        sys.stderr.write(decoded_err)

    if verbose or should_throw:
        sys.stdout.write(decoded_output)

    if should_throw:
        raise OnenvError(f"Environment error.\nCommand: {cmd} failed.")

    return decoded_output if return_output else proc.returncode


# TODO: After resolving VFS-4820 all this function can be imported from
# one-env submodule
def client_alias_to_pod_mapping() -> dict[str, str]:
    prov_clients_mapping = collections.defaultdict(list)
    client_alias_mapping = {}
    pods_list = list_pods()
    clients_pods = [pod for pod in pods_list if get_service_type(pod) == "oneclient"]
    for client_pod in clients_pods:
        provider = get_client_provider_host(client_pod)
        if provider is None:
            continue
        provider_alias = service_name_to_alias_mapping(provider)
        prov_clients_mapping[provider_alias].append(client_pod)

    i = 1
    for prov_alias in sorted(list(prov_clients_mapping.keys())):
        client_pods = sorted(prov_clients_mapping[prov_alias], key=get_name)
        for pod in client_pods:
            key = f"oneclient-{i}"
            client_alias_mapping[key] = get_name(pod)
            client_alias_mapping[get_name(pod)] = key
            i += 1
    return client_alias_mapping


def service_name_to_alias_mapping(name: str) -> str:
    return [
        val
        for key, val in {
            "oneprovider-krakow": "oneprovider-1",
            "oneprovider-paris": "oneprovider-2",
            "oneprovider-lisbon": "oneprovider-3",
            "onezone": "onezone",
        }.items()
        if key.lower() in name
    ][0]


def get_service_type(pod: client.V1Pod) -> Optional[str]:
    # returns SERVICE_ONEZONE | SERVICE_ONEPROVIDER
    return pod.metadata.labels.get("component")


def get_client_provider_host(pod: client.V1Pod) -> Optional[str]:
    return get_env_variable(pod, "ONECLIENT_PROVIDER_HOST")


def get_env_variable(pod: client.V1Pod, env_name: str) -> Optional[str]:
    envs = get_env_variables(pod)
    for env in envs:
        if env.name == env_name:
            return env.value
    return None


def get_env_variables(pod: client.V1Pod) -> list[client.V1EnvVar]:
    return pod.spec.containers[0].env


def init_helm() -> None:
    sp.call(helm_init_cmd(client_only=True))


def helm_init_cmd(client_only: Optional[bool] = None) -> Command:
    cmd = ["helm", "init"]

    if client_only:
        cmd.append("--client-only")

    return cmd


def get_kube_client() -> client.CoreV1Api:
    urllib3.disable_warnings()
    config.load_kube_config(
        config_file=os.path.join(os.path.expanduser("~"), ".kube", "config")
    )
    kube = client.CoreV1Api()
    return kube


def list_pods_and_jobs() -> list[client.V1Pod]:
    kube = get_kube_client()
    namespace = get_current_namespace()
    return kube.list_namespaced_pod(namespace).items


def cmd_exec(
    pod: str,
    command: str | list[str],
    interactive: bool = False,
    tty: bool = False,
    container: Optional[str] = None,
) -> Command:
    cmd = ["kubectl", "--namespace", get_current_namespace(), "exec"]

    if interactive:
        cmd.append("-i")
    if tty:
        cmd.append("-t")
    cmd.append(pod)

    if container:
        cmd.extend(["-c", container])

    if isinstance(command, list):
        cmd.append("--")
        cmd += command
    else:
        cmd.extend(["--", command])

    return cmd


def get_name(component: client.V1Pod) -> str:
    return component.metadata.name


def get_ip(pod: client.V1Pod) -> str:
    return pod.status.pod_ip


def is_pod(pod: client.V1Pod) -> bool:
    if pod.metadata.owner_references:
        return pod.metadata.owner_references[0].kind != "Job"
    return False


def list_pods() -> list[client.V1Pod]:
    return list(filter(is_pod, list_pods_and_jobs()))


def match_pods(substring: str) -> list[client.V1Pod]:
    pods_list = list_pods()
    # Accept dashes as wildcard characters
    pattern = f".*{substring.replace("-", ".*")}.*"
    return list(filter(lambda pod: re.match(pattern, get_name(pod)), pods_list))


def get_current_namespace() -> str:
    namespace = get("currentNamespace")
    if not isinstance(namespace, str):
        raise TypeError("currentNamespace must be a string")
    return namespace


def get(key: str) -> YamlValue:
    loaded_config = load_yaml(user_config_path())
    return loaded_config[key]


def load_yaml(path: str) -> YamlObject:
    with open(path) as f:
        return cast(YamlObject, yaml.load(f, yaml.Loader))


def user_config_path() -> str:
    return os.path.join(one_env_directory(), "config.yaml")


def one_env_directory() -> str:
    return os.path.join(host_home(), ".one-env")


def host_home() -> str:
    return os.path.expanduser("~")


def deployments_directory() -> str:
    return os.path.join(one_env_directory(), "deployments")


def current_deployment_dir() -> str:
    all_deployments = os.listdir(deployments_directory())
    all_deployments.sort()
    if len(all_deployments) == 0:
        print("There are no deployments")
        sys.exit(1)
    else:
        return os.path.join(deployments_directory(), all_deployments[-1])


def deployment_data_path() -> str:
    return os.path.join(current_deployment_dir(), "deployment_data.yml")
