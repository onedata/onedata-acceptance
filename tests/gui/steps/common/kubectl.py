"""This module contains gherkin steps to run acceptance tests featuring
interactions with kubectl pods.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.utils.bdd_utils import wt, parsers
from tests.utils.environment_utils import run_kubectl_command


@wt(parsers.parse('user of {browser_id} kills "{provider}" provider'))
def kubectl_delete_pod(provider, hosts):
    pod_name = hosts[provider]['pod-name']
    run_kubectl_command('delete', args=['pod', pod_name])
