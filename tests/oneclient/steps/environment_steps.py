"""This module contains tests steps concerning environments operations
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import time
from tests.utils.bdd_utils import when, then, wt, parsers
from tests.utils.environment_utils import verify_env_ready, run_kubectl_command
from tests.utils.onenv_utils import (run_onenv_command,
                                     service_name_to_alias_mapping)


@wt(parsers.re('(?P<user>\w+) restarts oneprovider (?P<name>.*)'))
def restart_provider(name, users, hosts):
    run_onenv_command('exec', [name, '--', 'op_worker', 'stop'])
    verify_env_ready(users['admin'], hosts)


# NOTE: because of underlying escript implementation this step currently works
# only for krakow oneprovider (TODO VFS-11324)
@wt(parsers.re('(?P<user>\w+) stops network on oneprovider (?P<name>.*) for '
               '(?P<stop_time>.*) seconds'))
def restart_network(name, stop_time, hosts):
    pod_name = hosts[service_name_to_alias_mapping(name)]['pod-name']
    # TODO VFS-11325 do not copy escripts for each function invocation
    run_kubectl_command('cp', ['tests/utils/escripts/escript_utils.erl',
                               f'{pod_name}:/tmp/escript_utils.erl'])
    run_kubectl_command('cp', ['tests/utils/escripts/https_restart.escript',
                               f'{pod_name}:/tmp/https_restart.escript'])
    run_kubectl_command('exec', [pod_name, '--', '/tmp/https_restart.escript',
                                 stop_time])
    time.sleep(int(stop_time))


# NOTE: because of underlying escript implementation this step currently works
# only for krakow oneprovider (TODO VFS-11324)
@wt(parsers.re('user mocks archive verifiction on (?P<name>.*) Oneprovider '
               'to fail'))
def mock_archive_verification(name, hosts, run_unmock):
    pod_name = hosts[service_name_to_alias_mapping(name)]['pod-name']
    # TODO VFS-11325 do not copy escripts for each function invocation
    run_kubectl_command('cp', ['tests/utils/escripts/escript_utils.erl',
                               f'{pod_name}:/tmp/escript_utils.erl'])
    run_kubectl_command(
        'cp', ['tests/utils/escripts/archive_verification_mock.escript',
               f'{pod_name}:/tmp/archive_verification_mock.escript'])
    run_kubectl_command('exec', [pod_name, '--',
                                 '/tmp/archive_verification_mock.escript'])


# NOTE: because of underlying escript implementation this step currently works
# only for krakow oneprovider (TODO VFS-11324)
@wt(parsers.re('Archive verification is unmocked on (?P<name>.*) Oneprovider'))
def unmock_archive_verification(name, hosts):
    pod_name = hosts[service_name_to_alias_mapping(name)]['pod-name']
    # TODO VFS-11325 do not copy escripts for each function invocation
    run_kubectl_command('cp', ['tests/utils/escripts/escript_utils.erl',
                               f'{pod_name}:/tmp/escript_utils.erl'])
    run_kubectl_command(
        'cp', ['tests/utils/escripts/archive_verification_unmock.escript',
               f'{pod_name}:/tmp/archive_verification_unmock.escript'])
    run_kubectl_command('exec', [pod_name, '--',
                                 '/tmp/archive_verification_unmock.escript'])
