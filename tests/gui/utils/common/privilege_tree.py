"""Utils for operations on privilege trees in GUI tests
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence, Button


class PrivilegeRow(PageObject):
    name = id = Label('.node-text')
    toggle = Toggle('.one-way-toggle')

    def expand(self):
        self.web_elem.click()

    def activate(self):
        self.toggle.check()

    def deactivate(self):
        self.toggle.uncheck()

    def assert_privilege_granted(self, granted):
        if granted:
            msg = f'{self.name} should be granted but is not'
            assert self.toggle.is_checked(), msg
        else:
            msg = f'{self.name} should not be granted but it is'
            assert self.toggle.is_unchecked(), msg

    def set_privilege(self, granted):
        if granted:
            self.activate()
        else:
            self.deactivate()


class PrivilegeGroup(PageObject):
    name = id = Label('.one-tree-item-content')
    expander = Button('.tree-circle')
    toggle = Toggle('.one-way-toggle')

    sub_privileges = WebItemsSequence('.one-tree-item-content',
                                      cls=PrivilegeRow)

    def expand(self):
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
            assert self.toggle.is_maybe_checked(), msg
        elif granted:
            msg = f'{self.name} should be granted but is not'
            assert self.toggle.is_checked(), msg
        else:
            msg = f'{self.name} should not be granted but it is'
            assert self.toggle.is_unchecked(), msg


class PrivilegeTree(PageObject):
    privilege_groups = WebItemsSequence('.tree-item-content-container',
                                        cls=PrivilegeGroup)
    privileges = WebItemsSequence('.one-tree-item-content', cls=PrivilegeRow)

    def get_privilege_row(self, name):
        return self.privileges[name]

    def assert_privileges(self, privileges):
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
        self._assert_privileges(privileges)

    def _assert_privileges(self, privileges):
        for privilege_name, privilege_group in privileges.items():
            self._assert_privilege_group(privilege_group, privilege_name)

    def _assert_privilege_group(self, group, name):
        privilege_row = self.privilege_groups[name]
        granted = group['granted']
        if granted == 'Partially':
            sub_privileges = group['privilege subtypes']
            privilege_row.expand()
            for sub_name, sub_granted in sub_privileges.items():
                sub_row = privilege_row.get_sub_privilege_row(sub_name)
                sub_row.assert_privilege_granted(sub_granted)
        privilege_row.assert_privilege_granted(granted)

    def set_privileges(self, privileges):
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
        self._set_privileges(privileges)

    def _set_privileges(self, privileges):
        for privilege_name, privilege_group in privileges.items():
            self._set_privilege_group(privilege_group, privilege_name)

    def _set_privilege_group(self, group, name):
        privilege_row = self.privilege_groups[name]
        granted = group['granted']
        if granted == 'Partially':
            sub_privileges = group['privilege subtypes']
            privilege_row.expand()
            for sub_name, sub_granted in sub_privileges.items():
                sub_row = privilege_row.get_sub_privilege_row(sub_name)
                sub_row.set_privilege(sub_granted)
        else:
            privilege_row.get_sub_privilege_row(name).set_privilege(granted)
