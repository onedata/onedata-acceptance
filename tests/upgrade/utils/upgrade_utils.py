"""This module contains utility functions used in tests of upgrade procedure."""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from bamboos.docker.environment.docker import pull_image_with_retries
from bamboos.docker.images_branch_config import resolve_image

from tests.conftest import export_logs
from tests.utils.environment_utils import (
    configure_os,
    get_deployment_status,
    setup_hosts_cfg,
    update_etc_hosts,
    verify_env_ready,
)
from tests.utils.onenv_utils import run_onenv_command


class UpgradeTest:
    def __init__(self, name, setup, verify):
        self.__name = name
        self.__setup = setup  # function executed before any upgrade is performed
        self.__verify = verify  # function executed after all upgrades are performed

    def run_setup(self, *args, **kwargs):
        print(f'\nRunning setup for test "{self.__name}"\n')
        self.__setup(*args, **kwargs)
        print(f'\nSetup for test "{self.__name}" finished\n')

    def run_verify(self, *args, **kwargs):
        print(f'\nRunning verify for test "{self.__name}"\n')
        self.__verify(*args, **kwargs)
        print(f'\nVerify for test "{self.__name}" finished\n')


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

    def add_test(self, test):
        self.__tests_list.append(test)

    def add_tests(self, tests):
        self.__tests_list.extend(tests)

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

    def run_tests(self):
        admin_user = self.users["admin"]
        _ = [self.__run_setup(test) for test in self.__tests_list]
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
        _ = [self.__run_verify(test) for test in self.__tests_list]
        self.__unmount_clients()

    def __run_setup(self, test):
        test.run_setup()
        self.__unmount_clients()
        export_logs(
            self.request, self.env["env_description_abs_path"], "before_upgrade"
        )

    def __run_verify(self, test):
        test.run_verify()
        self.__unmount_clients()

    def __unmount_clients(self):
        for user in self.users.values():
            for client in user.clients.values():
                client.unmount()
            user.clients.clear()


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
