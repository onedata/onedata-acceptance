"""Utils for operations on privilege trees in GUI tests"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

import time

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItemsSequence,
)


class PrivilegeRow(PageObject):
    name = id = Label(".node-text")
    toggle = Toggle(".one-way-toggle")
    _checkbox = WebElement(".one-checkbox-base")

    def expand(self):
        self.web_elem.click()

    def activate(self):
        self.toggle.check()

    def deactivate(self):
        self.toggle.uncheck()

    def assert_privilege_granted(self, granted):
        if granted == "Partially":
            msg = f"{self.name} should be partially granted but is not"
            assert self.toggle.is_partial_checked(), msg
        elif granted:
            msg = f"{self.name} should be granted but is not"
            assert self.toggle.is_checked(), msg
        else:
            msg = f"{self.name} should not be granted but it is"
            assert self.toggle.is_unchecked(), msg

    def set_privilege(self, driver, granted, with_scroll=False):
        if with_scroll:
            if (self.toggle.is_checked() and not granted) or (
                not self.toggle.is_checked() and granted
            ):
                driver.execute_script(
                    "document.querySelector('.col-content').scrollTo(0, 0)"
                )
                elem_class = self._checkbox.get_attribute("class").split(" ")[0]
                try:
                    driver.find_element(
                        By.CSS_SELECTOR, "." + elem_class
                    ).click()
                except ElementNotInteractableException:
                    self.toggle.click()

        else:
            if granted:
                self.activate()
            else:
                self.deactivate()


class PrivilegeGroup(PageObject):
    name = id = Label(".one-tree-item-content")
    expander = Button(".tree-circle")
    toggle = Toggle(".one-way-toggle")

    sub_privileges = WebItemsSequence(
        ".one-tree-item-content", cls=PrivilegeRow
    )

    def expand(self):
        if not self.is_expanded():
            self.expander.click()

    def is_expanded(self):
        return "expanded" in self.web_elem.get_attribute("class")

    def collapse(self, driver):
        if self.is_expanded():
            try:
                driver.execute_script(
                    "document.querySelector('.col-content').scrollTo(0, 0)"
                )
                driver.find_element(
                    By.CSS_SELECTOR, ".tree-circle .oneicon-square-minus-empty"
                ).click()
            except RuntimeError:
                self.expander.click()

    def minimalize(self):
        self.expander.click()

    def activate(self):
        self.toggle.check()

    def deactivate(self):
        self.toggle.uncheck()

    def get_sub_privilege_row(self, name):
        return self.sub_privileges[name]

    def assert_privilege_granted(self, granted):
        if granted == "Partially":
            msg = f"{self.name} should be partially granted but is not"
            assert self.toggle.is_partial_checked(), msg
        elif granted:
            msg = f"{self.name} should be granted but is not"
            assert self.toggle.is_checked(), msg
        else:
            msg = f"{self.name} should not be granted but it is"
            assert self.toggle.is_unchecked(), msg


class PrivilegeTree(PageObject):
    privilege_groups = WebItemsSequence(
        ".has-checkbox-group", cls=PrivilegeGroup
    )
    privileges = WebItemsSequence(".one-tree-item-content", cls=PrivilegeRow)

    def get_privilege_row(self, name):
        return self.privileges[name]

    def assert_privileges(self, selenium, browser_id, privileges):
        """Assert privileges according to given config.
        For this method only dict should be passed!

        Config format given in earlier in yaml is as follow:

            privilege_type:
                granted: True/False/Partially
                privilege subtypes:            ---> always and only when
                                                    granted is Partially
                    privilege_subtype: True/False
            ...

            Space management:
              granted: Partially
              privilege subtypes:
                Modify space: True
                Remove space: False
            User management:
              granted: False
        """
        self._assert_privileges(selenium, browser_id, privileges)

    def _assert_privileges(self, selenium, browser_id, privileges):
        for privilege_name, privilege_group in privileges.items():
            self._assert_privilege_group(
                selenium, browser_id, privilege_group, privilege_name
            )

    def _assert_privilege_group(self, selenium, browser_id, group, name):
        driver = selenium[browser_id]
        privilege_row = self.privilege_groups[name]
        granted = group["granted"]
        if granted == "Partially":
            sub_privileges = group["privilege subtypes"]
            privilege_row.expand()
            time.sleep(0.1)
            for sub_name, sub_granted in sub_privileges.items():
                sub_row = privilege_row.get_sub_privilege_row(sub_name)
                sub_row.assert_privilege_granted(sub_granted)
            privilege_row.collapse(driver)
        privilege_row.assert_privilege_granted(granted)

    def set_privileges(
        self, selenium, browser_id, privileges, with_scroll=False
    ):
        """Set privileges according to given config.
        For this method only dict should be passed!

        Config format given in earlier in yaml is as follow:

            privilege_type:
                granted: True/False/Partially
                privilege subtypes:            ---> always and only when
                                                    granted is Partially
                    privilege_subtype: True/False
            ...

            Space management:
              granted: Partially
              privilege subtypes:
                Modify space: True
                Remove space: False
            User management:
              granted: False
        """
        self._set_privileges(selenium, browser_id, privileges, with_scroll)

    def _set_privileges(
        self, selenium, browser_id, privileges, with_scroll=False
    ):
        for privilege_name, privilege_group in privileges.items():
            self._set_privilege_group(
                selenium,
                browser_id,
                privilege_group,
                privilege_name,
                with_scroll,
            )

    def _set_privilege_group(
        self, selenium, browser_id, group, name, with_scroll=False
    ):
        driver = selenium[browser_id]
        privilege_row = self.privilege_groups[name]
        granted = group["granted"]
        if granted == "Partially":
            sub_privileges = group["privilege subtypes"]
            privilege_row.expand()
            for sub_name, sub_granted in sub_privileges.items():
                sub_row = privilege_row.get_sub_privilege_row(sub_name)
                sub_row.set_privilege(driver, sub_granted, with_scroll)
            privilege_row.collapse(driver)
        else:
            privilege_row.get_sub_privilege_row(name).set_privilege(
                driver, granted
            )

    def set_all_true(self):
        for priv_group in self.privilege_groups:
            priv_group.activate()
