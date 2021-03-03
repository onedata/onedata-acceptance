"""Utils for common operations in GUI tests
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


def scroll_to_css_selector(driver, css_sel):
    driver.execute_script(f"var el = (typeof $ === 'function' ? "
                          f"$('{css_sel}')[0] : "
                          f"document.querySelector('{css_sel}')); "
                          f"el && el.scrollIntoView(true);")
