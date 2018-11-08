"""This module contains utility functions to be used in acceptance tests."""
import logging
import traceback

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import traceback
import logging
from time import time, sleep

from decorator import decorator


def log_exception():
    extracted_stack = traceback.format_exc(10)
    logging.error(extracted_stack)


def assert_generic(expression, should_fail, *args, **kwargs):
    if should_fail:
        assert_false(expression, *args, **kwargs)
    else:
        assert_(expression, *args, **kwargs)


def assert_(expression, *args, **kwargs):
    assert_result = expression(*args, **kwargs)
    assert assert_result


def assert_false(expression, *args, **kwargs):
    assert_result = expression(*args, **kwargs)
    assert not assert_result


def repeat_failed(attempts=10, timeout=None, interval=0.1,
                  exceptions=(Exception,)):
    """Returns wrapper on function, which keeps calling it until timeout or
    for attempts times in case of failure (exception).

    :param attempts: maximum num of attempts, defaults to 10
    :type attempts: int
    :param interval: time between subsequent calls
    :type interval: float
    :param timeout: time limit of now when to stop repeating fun,
                    if set alongside attempts take precedence
    :type timeout: float | None
    :param exceptions: in case of which consider failure of call
    :type exceptions: list[Exception]
    :return: wrapper decorator
    """

    @decorator
    def wrapper(fun, *args, **kwargs):
        now = time()
        limit, i = (now + timeout, now) if timeout else (attempts, 0)

        while i < limit:
            try:
                result = fun(*args, **kwargs)
            except exceptions:
                sleep(interval)
                i = time() if timeout else i+1
                continue
            else:
                return result
        return fun(*args, **kwargs)

    return wrapper
