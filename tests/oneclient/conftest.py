"""This module contains definitions of fixtures used in oneclient tests
of onedata.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import pytest
import errno

from tests.conftest import export_logs


@pytest.fixture(autouse=True)
def skip_by_env(skip_by_env):
    """Autouse fixture defined in tests.conftest
    """
    pass


@pytest.fixture(autouse=True)
def xfail_by_env(xfail_by_env):
    """Autouse fixture defined in tests.conftest
    """
    pass


@pytest.fixture(autouse=True, scope='module')
def run_around_suite(request, env_description_abs_path):
    yield
    export_logs(request, env_description_abs_path)


@pytest.fixture(autouse=True)
def run_around_testcase(users):
    unmount_all_clients_and_purge_spaces(users)
    yield
    unmount_all_clients_and_purge_spaces(users)


def unmount_all_clients_and_purge_spaces(users):
    for user in users.values():
        for client in user.clients.values():
            purge_spaces(client)
            client.unmount()
        user.clients.clear()


def purge_spaces(client):
    try:
        spaces = client.list_spaces()
        for space in spaces:
            space_path = client.absolute_path(space)
            try:
                client.rm(path=space_path, recursive=True)
            except FileNotFoundError:
                pass
            except OSError as e:
                # ignore EACCES errors during cleaning
                if e.errno == errno.EACCES:
                    pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print("Error during cleaning up spaces: {}".format(e))
