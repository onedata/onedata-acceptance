"""This module implements some common basic functions and functionality for
acceptance tests of onedata.
"""
__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

from pytest_bdd import parsers
from pytest_bdd import when, then


def list_parser(list):
    return [el.strip() for el in list.strip("[]").split(',') if el != ""]


def make_arg_list(arg):
    return "[" + arg + "]"

