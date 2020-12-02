"""This module contains tests steps concerning environments operations
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.utils.bdd_utils import when, then, wt, parsers
from tests.utils.environment_utils import verify_env_ready
from tests.utils.onenv_utils import run_onenv_command


@wt(parsers.re('(?P<user>\w+) restarts oneprovider (?P<name>.*)'))
def restart_provider(name, users, hosts):
    run_onenv_command('exec', [name, '--', 'op_worker', 'stop'])
    verify_env_ready(users['admin'], hosts)
