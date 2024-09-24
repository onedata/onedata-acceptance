"""Utils for operations on privilege trees in GUI tests
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence, Button, \
    WebElement
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By


class PrivilegeRow(PageObject):
    name = id = Label('.priv')
    toggle = Toggle('.one-way-toggle')
    _checkbox = WebElement('.one-checkbox-base')
    effective_granted = WebElement('.effective .one-icon')
    effective_revoke = WebElement('.effective .priv-revoke')

    def expand(self):
        self.web_elem.click()

    def activate(self):
        self.toggle.check()

    def deactivate(self):
        self.toggle.uncheck()

    def assert_privilege_granted(self, granted):
        if granted == "Partially":
            msg = f'{self.name} should be partially granted but is not'
            assert self.toggle.is_partial_checked(), msg
        elif granted:
            msg = f'{self.name} should be granted but is not'
            assert self.toggle.is_checked(), msg
        else:
            msg = f'{self.name} should not be granted but it is'
            assert self.toggle.is_unchecked(), msg

    def assert_effective_privilege_granted(self, granted):
        if granted:
            msg = f'{self.name} should be granted but is not'
            assert 'oneicon-checked' in self.effective_granted.get_attribute('class'), msg
        else:
            msg = f'{self.name} should not be granted but it is'
            assert self.effective_revoke, msg

    def set_privilege(self, driver, granted, with_scroll=False):
        if with_scroll:
            if (self.toggle.is_checked() and not granted) or (
                    not self.toggle.is_checked() and granted):
                driver.execute_script(
                    "document.querySelector('.col-content').scrollTo(0, 0)")
                elem_id = self._checkbox.get_attribute('id')
                try:
                    driver.find_element(By.CSS_SELECTOR, '#' + elem_id).click()
                except ElementNotInteractableException:
                    self.toggle.click()
        else:
            if granted:
                self.activate()
            else:
                self.deactivate()
        if granted:
            return self.toggle.is_checked()
        else:
            return self.toggle.is_unchecked()


class PrivilegeGroup(PageObject):
    name = id = Label('.group-privilege-text-container div')
    expander = Button('.group-privilege-text-container .one-icon')
    _expander = WebElement('.group-privilege-text-container .one-icon')
    toggle = Toggle('.toggle-column.group .one-way-toggle')
    _checkbox = WebElement('.one-checkbox-base')
    effective_priv = Label('.pill')

    sub_privileges = WebItemsSequence('.privilege-row', cls=PrivilegeRow)

    def expand(self, driver):
        if not self.is_expanded():
            expander_id = self._expander.get_attribute('id')
            try:
                driver.execute_script(
                    "document.querySelector('.col-content').scrollTo(0, 0)")
                driver.find_element(
                    By.CSS_SELECTOR, f'#{expander_id}').click()
            except ElementNotInteractableException:
                self.expander.click()

    def is_expanded(self):
        return 'oneicon-arrow-up' in self._expander.get_attribute('class')

    def collapse(self, driver):
        if self.is_expanded():
            try:
                driver.execute_script(
                    "document.querySelector('.col-content').scrollTo(0, 0)")
                driver.find_element(
                    By.CSS_SELECTOR, '.table-privileges .oneicon-arrow-up').click()
            except ElementNotInteractableException:
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
        if granted == 'Partially':
            msg = f'{self.name} should be partially granted but is not'
            assert self.toggle.is_partial_checked(), msg
        elif granted:
            msg = f'{self.name} should be granted but is not'
            assert self.toggle.is_checked(), msg
        else:
            msg = f'{self.name} should not be granted but it is'
            assert self.toggle.is_unchecked(), msg

    def assert_effective_privilege_granted(self, granted):
        granted_count = int(self.effective_priv.split('/')[0])
        all_count = int(self.effective_priv.split('/')[1])
        if granted == 'Partially':
            msg = f'{self.name} should be partially granted but is not'
            assert granted_count != all_count and granted_count > 0, msg
        elif granted:
            msg = f'{self.name} should be granted but is not'
            assert granted_count == all_count, msg
        else:
            msg = f'{self.name} should not be granted but it is'
            assert granted_count == 0, msg

    def set_privilege(self, driver, granted, with_scroll=False):
        count = 2 if self.toggle.is_partial_checked() and not granted else 1
        if with_scroll:
            if ((self.toggle.is_checked() and not granted) or (
                    not self.toggle.is_checked() and granted) or
                    self.toggle.is_partial_checked()):
                driver.execute_script(
                    "document.querySelector('.col-content').scrollTo(0, 0)")
                elem_id = self._checkbox.get_attribute('id')
                for i in range(count):
                    try:
                        driver.find_element(
                            By.CSS_SELECTOR, '#' + elem_id).click()
                    except ElementNotInteractableException:
                        self.toggle.click()
        else:
            if granted:
                self.activate()
            else:
                self.deactivate()
        if granted:
            return self.toggle.is_checked()
        else:
            return self.toggle.is_unchecked()


class PrivilegeTree(PageObject):
    privilege_groups = WebItemsSequence('.group-privilege-row',
                                        cls=PrivilegeGroup)
    privileges = WebItemsSequence('.privilege-row ', cls=PrivilegeRow)
    spinner = WebElement('.spin-spinner-block')

    def get_privilege_row(self, name):
        return self.privileges[name]

    def assert_privileges(self, selenium, browser_id, privileges,
                          is_direct_privileges=True):
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
        self._assert_privileges(selenium, browser_id, privileges,
                                is_direct_privileges)

    def _assert_privileges(self, selenium, browser_id, privileges,
                           is_direct_privileges):
        for privilege_name, privilege_group in privileges.items():
            self._assert_privilege_group(selenium, browser_id, privilege_group,
                                         privilege_name, is_direct_privileges)

    def _assert_privilege_group(self, selenium, browser_id, group, name,
                                is_direct_privileges):
        driver = selenium[browser_id]
        privilege_row = self.privilege_groups[name]
        granted = group['granted']
        if granted == 'Partially':
            sub_privileges = group['privilege subtypes']
            privilege_row.expand(driver)
            for sub_name, sub_granted in sub_privileges.items():
                if is_direct_privileges:
                    self.privileges[sub_name].assert_privilege_granted(sub_granted)
                else:
                    self.privileges[sub_name].assert_effective_privilege_granted(sub_granted)
            privilege_row.collapse(driver)
        if is_direct_privileges:
            privilege_row.assert_privilege_granted(granted)
        else:
            privilege_row.assert_effective_privilege_granted(granted)

    def set_privileges(self, selenium, browser_id, privileges,
                       with_scroll=False):
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
        return self._set_privileges(selenium, browser_id, privileges,
                                    with_scroll)

    def _set_privileges(self, selenium, browser_id, privileges,
                        with_scroll=False):
        result = True
        for privilege_name, privilege_group in privileges.items():
            result = result and self._set_privilege_group(
                selenium, browser_id, privilege_group, privilege_name,
                with_scroll)
        return result

    def _set_privilege_group(self, selenium, browser_id, group, name,
                             with_scroll=False):
        driver = selenium[browser_id]
        privilege_row = self.privilege_groups[name]
        granted = group['granted']
        result = True
        if granted == 'Partially':
            sub_privileges = group['privilege subtypes']
            privilege_row.expand(driver)
            time.sleep(1)
            for sub_name, sub_granted in sub_privileges.items():
                result = result and self.privileges[sub_name].set_privilege(
                    driver, sub_granted, with_scroll)
            privilege_row.collapse(driver)
        else:
            result = result and privilege_row.set_privilege(
                driver, granted, with_scroll)
        return result

    def set_all_true(self):
        for priv_group in self.privilege_groups:
            priv_group.activate()

    def wait_for_load_privileges(self):
        for _ in range(50):
            try:
                self.spinner
                time.sleep(0.1)
            except RuntimeError:
                return
        raise RuntimeError(
            'Did not manage to set privileges, exceeded loading time')
