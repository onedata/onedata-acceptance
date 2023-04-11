"""Generic GUI testing utils - mainly helpers and extensions for Selenium.
"""

__author__ = "Jakub Liput, Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import os
import re
from contextlib import contextmanager
from itertools import islice
from time import sleep

try:
    from itertools import izip
except ImportError:
    izip = zip

from tests import gui
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# RE_URL regexp is matched as shown below:
#
# https://172.18.0.8/#/onedata/data/small_space/g2gDZAAEZ3VpZG0AAAAkZzJnQ
# \       \        /   \     / \  / \         /                        /
#  \        domain      \   /   tab  \___id__/                        /
#   \            /      access                                       /
#    \_base_url_/         \_________________method__________________/

RE_URL = re.compile(r'(?P<base_url>https?://(?P<domain>.*?)'
                    r'(/(?P<where>[^/]*)/(?P<cluster>[^/]*))?)'
                    r'(/i#)?(?P<method>/(?P<access>[^/]*)/(?P<tab>[^/]*)'
                    r'(/(?P<id>[^/]*).*)?)')


def parse_url(url):
    return RE_URL.match(url)


def go_to_relative_url(selenium, relative_url):
    new_url = RE_URL.match(selenium.current_url).group('base_url') + relative_url
    selenium.get(new_url)


def parse_seq(seq, pattern=None, separator=None, default=str):
    if pattern is not None:
        return [default(el.group()) for el in re.finditer(pattern, seq)]
    else:
        separator = ',' if separator is None else separator
        return [default(el.strip().strip('"'))
                for el in seq.strip('[]').split(separator) if el != '']


def upload_file_path(file_name):
    """Resolve an absolute path for file with name file_name stored in upload_files dir
    """
    return os.path.join(
        os.path.dirname(os.path.abspath(gui.__file__)),
        'upload_files',
        file_name)


def workflow_path(workflow_name):
    """Resolve an absolute path for workflow file with name workflow_name stored in automation-examples submodule
    """
    return os.path.abspath(os.path.join(os.path.dirname(gui.__file__ ), '..', 'automation-examples','workflows',workflow_name))


def strip_path(path_string, separator = '/'):
    """Strips string from whitespaces inside file path. Useful for file paths rendered
    in DOM which contains `\\n` characters in `innerText`.
    """
    return separator.join(
        [path_item.strip() for path_item in path_string.split(separator)])


@contextmanager
def rm_css_cls(driver, web_elem, css_cls):
    driver.execute_script("$(arguments[0]).removeClass('{}')".format(css_cls),
                          web_elem)
    yield web_elem
    driver.execute_script("$(arguments[0]).addClass('{}')".format(css_cls),
                          web_elem)


@contextmanager
def implicit_wait(driver, timeout, prev_timeout):
    driver.implicitly_wait(timeout)
    try:
        yield
    finally:
        driver.implicitly_wait(prev_timeout)


def iter_ahead(iterable):
    read_ahead = iter(iterable)
    next(read_ahead)
    for item, next_item in izip(iterable, read_ahead):
        yield item, next_item


def find_web_elem(web_elem_root, css_sel, err_msg):
    try:
        _scroll_to_css_sel(web_elem_root, css_sel)
        item = web_elem_root.find_element_by_css_selector(css_sel)
    except NoSuchElementException:
        with suppress(TypeError):
            err_msg = err_msg()
        raise RuntimeError(err_msg)
    else:
        return item


def find_web_elem_with_text(web_elem_root, css_sel, text, err_msg):
    items = web_elem_root.find_elements_by_css_selector(css_sel)
    _scroll_to_css_sel(web_elem_root, css_sel)
    for item in items:
        if item.text.lower() == text.lower():
            return item
    else:
        raise RuntimeError(f'Css element wtih "{text}" text not found')


def click_on_web_elem(driver, web_elem, err_msg, delay=True):
    disabled = 'disabled' in web_elem.get_attribute('class')
    # scroll to make the element visible
    if not web_elem.is_displayed():
        web_elem.location_once_scrolled_into_view
    if web_elem.is_enabled() and web_elem.is_displayed() and not disabled:
        # TODO VFS-7484 make optional sleep and localize only those tests that need it or find better alternative
        # currently checking if elem is enabled not always work (probably after striping disabled from web elem
        # elem is not immediately clickable)
        if delay:
            sleep(delay if isinstance(delay, float) else 0.25)
        action = ActionChains(driver)
        action.move_to_element(web_elem).click_and_hold(web_elem).release(web_elem)
        action.perform()
    else:
        with suppress(TypeError):
            err_msg = err_msg()
        raise RuntimeError(err_msg)


def _scroll_to_css_sel(web_elem_root, css_sel):
    driver = getattr(web_elem_root, 'parent', web_elem_root)
    driver.execute_script(f"var el = (typeof $ === 'function' ? "
                          f"$('{css_sel}')[0] : "
                          f"document.querySelector('{css_sel}')); "
                          f"el && el.scrollIntoView(true);")


@contextmanager
def suppress(*exceptions):
    try:
        yield
    except exceptions:
        pass


@contextmanager
def rm_css_cls(driver, web_elem, css_cls):
    driver.execute_script(f"arguments[0].classList.remove('{css_cls}')",
                          web_elem)
    yield web_elem
    driver.execute_script(f"arguments[0].classList.add('{css_cls}')",
                          web_elem)


def nth(seq, idx):
    return next(islice(seq, idx, None), None)


@contextmanager
def redirect_display(new_display):
    """Replace DISPLAY environment variable with new value"""
    old_display = os.environ.get('DISPLAY', 'DUMMY_DISPLAY')
    os.environ['DISPLAY'] = new_display
    try:
        yield
    finally:
        if old_display is not None:
            os.environ['DISPLAY'] = old_display
        else:
            del os.environ['DISPLAY']


def transform(val, strip_char=None):
    return val.strip(strip_char).lower().replace(' ', '_')
