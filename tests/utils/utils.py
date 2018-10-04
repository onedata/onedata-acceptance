import traceback
import logging


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
