"""Module implements utility functions for managing users in onedata via REST."""

__author__ = "Jakub Kudzia, Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2016-2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import hashlib
import json
import os
from collections.abc import Mapping
from typing import Optional, cast

import rpyc  # pylint: disable=import-error

from tests import HTTP_PORT, OZ_REST_PORT
from tests.utils import ONECLIENT_LOGS_DIR, ONECLIENT_MOUNT_DIR, RPYC_LOGS_DIR
from tests.utils.client_utils import Client, RpycConnectionLike, get_client_conf
from tests.utils.docker_utils import run_cmd as docker_run_cmd
from tests.utils.onenv_utils import get_ip, match_pods, run_onenv_command
from tests.utils.rest_utils import (
    get_token_dispenser_rest_path,
    get_zone_rest_path,
    http_get,
    http_post,
)
from tests.utils.utils import repeat_failed

RPYC_DEFAULT_PORT = 18812
BAD_TOKEN = "bad token"
CORRECT_TOKEN = "token"


class User:  # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        zone_hostname: str,
        username: str,
        password: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> None:
        self.username = username
        self.password = password
        self._user_id = user_id
        self._token: Optional[str] = None
        self.idps: list[str] = []
        self.keycloak_name = ""
        self.zone_hostname = zone_hostname

        self.last_operation_failed = False
        self.clients: dict[str, Client] = {}
        self._rpyc_connections: dict[str, RpycConnectionLike] = {}

    @property
    def token(self) -> str:
        if self._token:
            return self._token
        self._token = self._create_token()
        return self._token

    @property
    def user_id(self) -> str:
        if self._user_id:
            return self._user_id
        self._user_id = self._retrieve_onedata_id()
        return self._user_id

    def get_rpyc_connection(
        self, client_host_dict: Mapping[str, str]
    ) -> RpycConnectionLike:
        client_host = client_host_dict["pod_name"]
        if self._rpyc_connections.get(client_host, None):
            return self._rpyc_connections[client_host]
        self._rpyc_connections[client_host] = self._create_rpyc_connection(
            client_host_dict
        )
        return self._rpyc_connections[client_host]

    def mark_last_operation_failed(self) -> None:
        self.last_operation_failed = True

    def mark_last_operation_succeeded(self) -> None:
        self.last_operation_failed = False

    def mount_client(
        self,
        client_host_alias: str,
        client_id: str,
        hosts: Mapping[str, Mapping[str, str]],
        env_desc: Mapping[str, object],
        token: str = CORRECT_TOKEN,
        opts: Optional[list[str]] = None,
    ) -> Optional[Client]:
        rpyc_connection = self.get_rpyc_connection(hosts[client_host_alias])
        client_conf = get_client_conf(client_id, client_host_alias, env_desc)
        client_key = str(client_conf["id"])
        provider_key = str(client_conf["provider"])

        client = Client(rpyc_connection, timeout=client_conf.get("default timeout"))
        self.clients[client_key] = client

        token = self.token if token == CORRECT_TOKEN else token

        rpyc_connection.modules.os.environ["ONECLIENT_ACCESS_TOKEN"] = token
        rpyc_connection.modules.os.environ["ONECLIENT_PROVIDER_HOST"] = hosts[
            provider_key
        ]["hostname"]

        ret = client.mount(client_conf.get("mode"), additional_opts=opts)
        if ret == 0:
            self.mark_last_operation_succeeded()
            return client
        self.mark_last_operation_failed()
        del self.clients[client_key]
        return None

    @repeat_failed(attempts=5)
    def _create_token(self) -> str:
        if "keycloak" in self.idps:
            token_dispenser_pod = match_pods("token-dispenser")[0]
            token_dispenser_ip = get_ip(token_dispenser_pod)
            response = http_get(
                ip=token_dispenser_ip,
                port=HTTP_PORT,
                path=get_token_dispenser_rest_path("token", self.keycloak_name),
                auth=(self.username, self.password),
                default_headers=False,
                use_ssl=False,
            )
            return response.content.decode()
        response = http_post(
            ip=self.zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("user", "client_tokens"),
            auth=(self.username, self.password),
        )
        return json.loads(response.content)["token"]

    @repeat_failed(attempts=5)
    def _retrieve_onedata_id(self) -> str:
        response = http_get(
            ip=self.zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("user"),
            auth=(self.username, self.password),
        )
        return json.loads(response.content)["userId"]

    def _create_rpyc_connection(
        self, client_host_dict: Mapping[str, str]
    ) -> RpycConnectionLike:
        client_host = client_host_dict["pod_name"]
        client_host_ip = client_host_dict["ip"]
        cointainer_id = client_host_dict["container_id"]
        port = gen_port_number(self.username)
        create_required_dirs(client_host)
        cmd = (
            f"python3 `which rpyc_classic.py` --host 0.0.0.0 --port {port} --logfile"
            f" {os.path.join(RPYC_LOGS_DIR, self.username)}"
        )

        print(
            f"\n\nstarting rpyc server for user '{self.username}' on client host"
            f" '{client_host}'"
        )

        docker_run_cmd(self.username, cointainer_id, cmd, detach=True)
        rpyc_connection = self._connect_to_rpyc(client_host_ip, port)

        # change timeout for rpyc to avoid AsyncResultTimeout in performance tests on bamboo
        # pylint: disable=protected-access
        rpyc_connection._config["sync_request_timeout"] = 300

        print(
            f"rpyc server for user '{self.username}' on client host '{client_host}'"
            " successfully started"
        )

        return rpyc_connection

    @repeat_failed(attempts=10, interval=1, exceptions=ConnectionRefusedError)
    def _connect_to_rpyc(self, ip: str, port: int) -> RpycConnectionLike:
        return cast(RpycConnectionLike, rpyc.classic.connect(ip, port=port))


def create_required_dirs(pod: str) -> None:
    create_dir(pod, ONECLIENT_MOUNT_DIR)
    create_dir(pod, RPYC_LOGS_DIR)
    create_dir(pod, ONECLIENT_LOGS_DIR)


def create_dir(pod: str, log_dir_path: str) -> None:
    cmd = [pod, "--", "mkdir", "-p", "-m 777", log_dir_path]
    run_onenv_command("exec", cmd)


def gen_port_number(username: str) -> int:
    return (
        int(hashlib.sha1(username.encode("utf-8")).hexdigest(), 16) % 10000
        + RPYC_DEFAULT_PORT
    )
