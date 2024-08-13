"""This package contains python tests to run GUI acceptance tests.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import pytest

BROWSER = None


@pytest.fixture(scope='session', autouse=True)
def get_browser(request):
    global BROWSER
    BROWSER = request.config.getoption('--driver')
    return BROWSER


