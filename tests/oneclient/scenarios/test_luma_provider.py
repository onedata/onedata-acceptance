"""Test suite for operations on different storages with provider luma.
"""
__author__ = "Michal Wrona"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from functools import partial

from pytest_bdd import scenario
import pytest

from tests.oneclient.steps.reg_file_steps import *
from tests.oneclient.steps.file_steps import *
from tests.oneclient.steps.auth_steps import *


scenario = partial(scenario, '../features/luma_provider.feature')


@scenario('Operations on POSIX storage')
def test_posix_storage_operations(env_description_file):
    pass


@scenario('Operations on CEPH storage')
def test_ceph_storage_operations(env_description_file):
    pass


@scenario('Operations on Amazon S3 storage')
def test_s3_storage_operations(env_description_file):
    pass


@scenario('Operations on Openstack Swift storage')
def test_swift_storage_operations(env_description_file):
    pass
