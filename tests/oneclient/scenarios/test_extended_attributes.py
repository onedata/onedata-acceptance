"""Test suite for extended attributes support.
"""
__author__ = "Bartek Kryza"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from functools import partial

from pytest_bdd import scenario

from tests.oneclient.steps.auth_steps import *
from tests.oneclient.steps.dir_steps import *
from tests.oneclient.steps.file_steps import *
from tests.oneclient.steps.reg_file_steps import *
from tests.oneclient.steps.extended_attributes_steps import *
from tests.utils.acceptance_utils import *


scenario = partial(scenario, '../features/extended_attributes.feature')


@scenario('Check extended attribute exists')
def test_extended_attribute_exists(env_description_file):
    pass


@scenario('Check string extended attribute has correct value')
def test_string_extended_attribute_has_value(env_description_file):
    pass


@scenario('Check JSON extended attribute has correct value')
def test_json_extended_attribute_has_value(env_description_file):
    pass


@scenario('Check numeric extended attribute has correct value')
def test_numeric_extended_attribute_has_value(env_description_file):
    pass
