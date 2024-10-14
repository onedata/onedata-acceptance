"""Test suite for authorization and mounting onedata client,
in multi-client environment.
"""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from functools import partial

from pytest_bdd import scenario
from tests.oneclient.steps.multi_auth_steps import *
from tests.utils.acceptance_utils import *

scenario = partial(scenario, "../features/multi_authorization.feature")


@scenario(
    "Successful authorization - 1 client per user",
)
def test_successful_authorization1(env_description_file):
    pass


@scenario(
    "Successful authorization - 2 clients of one user",
)
def test_successful_authorization2(env_description_file):
    pass


@scenario(
    "Successful authorization - 2 clients of one user on different hosts",
)
def test_successful_authorization3(env_description_file):
    pass


@scenario(
    "Bad and good authorization",
)
def test_good_and_bad_authorization(env_description_file):
    pass


@scenario(
    "Bad authorization",
)
def test_bad_authorization(env_description_file):
    pass
