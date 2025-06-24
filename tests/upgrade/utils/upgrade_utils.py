"""This module contains utility functions used in tests of upgrade procedure."""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time
import traceback

# pylint: disable=import-error,no-name-in-module
from bamboos.docker.environment.docker import pull_image_with_retries
from bamboos.docker.images_branch_config import resolve_image

from tests.conftest import export_logs
from tests.upgrade.utils.rest_utils import get_provider_configuration
from tests.utils.environment_utils import (
    configure_os,
    get_deployment_status,
    setup_hosts_cfg,
    update_etc_hosts,
    verify_env_ready,
)
from tests.utils.onenv_utils import run_onenv_command


class UpgradeTest:
    def __init__(self, name, setup, verify, min_prov_version=None):
        self.__name = name
        self.__setup = setup  # function executed before any upgrade is performed
        self.__verify = verify  # function executed after all upgrades are performed
        self.__min_prov_version = min_prov_version

    def get_name(self):
        return self.__name

    def get_required_min_prov_version(self):
        return self.__min_prov_version

    def run_setup(self, *args, **kwargs):
        print(f'\nRunning setup for test "{self.__name}"\n')
        self.__setup(*args, **kwargs)
        print(f'\nSetup for test "{self.__name}" finished\n')

    def run_verify(self, *args, **kwargs):
        print(f'\nRunning verify for test "{self.__name}"\n')
        self.__verify(*args, **kwargs)
        print(f'\nVerify for test "{self.__name}" finished\n')


# pylint: disable=too-many-instance-attributes,broad-exception-caught
class UpgradeTestsController:
    def __init__(
        self,
        test_config,
        hosts,
        clients,
        request,
        users,
        env_desc,
        scenario_abs_path,
        env_description_abs_path,
    ):
        self.__tests_list = []
        self.__test_results = {}
        self.test_config = test_config
        self.env = {
            "env_desc": env_desc,
            "scenario_abs_path": scenario_abs_path,
            "env_description_abs_path": env_description_abs_path,
        }
        self.hosts = hosts
        self.clients = clients
        self.request = request
        self.users = users
        self.user_clients = {}
        self.initial_prov_version = ""

    def add_test(self, test):
        req_prov_version = test.get_required_min_prov_version()
        if req_prov_version is not None:
            if req_prov_version <= get_major_prov_version(
                self.hosts["oneprovider-1"]["hostname"]
            ):
                self.__tests_list.append(test)
        else:
            self.__tests_list.append(test)

    def add_tests(self, tests):
        for test in tests:
            self.add_test(test)

    def mount_client(self, username, client_host_alias, client_instance):
        client = self.users[username].mount_client(
            client_host_alias,
            client_instance,
            self.hosts,
            self.env["env_desc"],
            opts=[],
        )
        if client:
            return client
        raise RuntimeError("Error when mounting oneclient")

    def get_client(self, username, client_host_alias, client_instance):
        client_info = (
            username,
            client_host_alias,
            client_instance,
        )
        if client_info in self.user_clients:
            return self.user_clients[client_info]
        client = self.mount_client(*client_info)
        self.user_clients[client_info] = client
        return client

    def run_tests(self):
        admin_user = self.users["admin"]
        self.initial_prov_version = get_prov_version(
            self.hosts["oneprovider-1"]["hostname"]
        )
        for test in self.__tests_list:
            try:
                self.__run_setup(test)
            except Exception:
                self.__test_results[test.get_name()] = format_failed_test_results(
                    "SETUP", traceback.format_exc(), test
                )
                print("FAILED")
        # sleep is necessary as events are processed asynchronously and there is possible race
        # between client unmounting (which is done after the setup) and processing all its events
        # by provider.
        time.sleep(10)
        self.__unmount_clients()
        for service_name in ["onezone", "oneprovider", "oneclient"]:
            if service_name in self.test_config["targetVersions"].keys():
                upgrade_service(
                    service_name,
                    admin_user,
                    self.hosts,
                    self.test_config["targetVersions"][service_name],
                )

        setup_hosts_cfg(self.hosts, self.request)
        configure_os(self.env["scenario_abs_path"], get_deployment_status())
        for test in self.__tests_list:
            # test failed on setup
            if test.get_name() in self.__test_results:
                continue
            try:
                self.__run_verify(test)
            except Exception:
                self.__test_results[test.get_name()] = format_failed_test_results(
                    "VERIFY", traceback.format_exc(), test
                )
                print("FAILED")
            else:
                self.__test_results[test.get_name()] = format_succeed_test_results(test)
        self.__unmount_clients()
        self.print_tests_results()
        assert not self.tests_failed(), f"FAILED TESTS {self.get_failed_tests()}"

    def __run_setup(self, test):
        test.run_setup()
        export_logs(
            self.request, self.env["env_description_abs_path"], "before_upgrade"
        )

    def __run_verify(self, test):
        test.run_verify()

    def __unmount_clients(self):
        for user in self.users.values():
            for client in user.clients.values():
                client.unmount()
            user.clients.clear()
        self.user_clients = {}

    def get_failed_tests(self):
        return [
            test_name
            for test_name, test_result in self.__test_results.items()
            if "FAILED" in test_result
        ]

    def tests_failed(self):
        return any(self.get_failed_tests())

    def print_tests_results(self):
        print("TESTS RESULTS")
        for test_result in self.__test_results.values():
            print(test_result)


def upgrade_service(service_name, admin_user, hosts, version):
    for service in hosts.keys():
        if service.startswith(service_name):
            pod_name = hosts[service]["pod-name"]
            run_upgrade_command(pod_name, service_name, version)

    # etc hosts update needed so it is possible to connect
    update_etc_hosts()
    verify_env_ready(admin_user, hosts)


def run_upgrade_command(pod_name, service, version):
    cmd = [pod_name]
    if isinstance(version, str):
        cmd.extend(prepare_image_upgrade_command(service, version))
        run_onenv_command("upgrade", cmd)
    else:
        cmd.extend(prepare_sources_upgrade_command(service, version))
        run_onenv_command("upgrade", cmd)


def prepare_image_upgrade_command(service, version):
    if version == "default":
        image = resolve_image(service)
    else:
        image = f"docker.onedata.org/{service}-dev:{version}"
    pull_image_with_retries(image)
    return ["-i", image]


def prepare_sources_upgrade_command(service, version):
    image = f"docker.onedata.org/{service}-dev:{version["sources"]["baseImage"]}"
    pull_image_with_retries(image)
    components = []
    for component in version["sources"]["components"]:
        components.append(f"--{component}")
    cmd = ["-i", image, "--sources-path", "."]
    cmd.extend(components)
    return cmd


def get_major_prov_version(provider_host):
    return int(get_prov_version(provider_host).split(".")[0])


def get_prov_version(provider_host):
    return get_provider_configuration(provider_host)["version"]


def is_prov_version_lower_than(actual_version, reference_version):
    actual_version_split = [int(s) for s in actual_version.split("-")[0].split(".")]
    reference_version_split = [
        int(s) for s in reference_version.split("-")[0].split(".")
    ]
    if actual_version_split[0] < reference_version_split[0]:
        return True
    if actual_version_split[0] == reference_version_split[0]:
        if actual_version_split[1] < reference_version_split[1]:
            return True
        if actual_version_split[1] == reference_version_split[1]:
            return actual_version_split[2] < reference_version_split[2]
    return False


def format_failed_test_results(when, exception, test):
    return f"TEST {test.get_name()} FAILED ON {when} ERROR:\n {exception}"


def format_succeed_test_results(test):
    return f"TEST OK: {test.get_name()}"
