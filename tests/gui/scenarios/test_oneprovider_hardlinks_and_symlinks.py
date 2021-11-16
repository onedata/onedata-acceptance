"""This module contains tests suite for hardlinks and symlinks
 using Oneprovider GUI and single browser instance.
"""

__author__ = "Agnieszka Warchoł, Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest import fixture, mark
from pytest_bdd import scenario, scenarios

from tests.gui.steps.common.miscellaneous import *


# empty test for backward compatibility on bamboo
scenarios('../features/pass.feature')
