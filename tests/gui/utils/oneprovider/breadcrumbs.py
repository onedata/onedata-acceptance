"""Utils and fixtures to facilitate operations on breadcrumbs in
Oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from functools import partial

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, WebItem, WebItemsSequence
from tests.gui.utils.core.web_objects import ButtonWithTextPageObject


class _Breadcrumbs(PageObject):
    _breadcrumbs = WebItemsSequence(
        ".fb-breadcrumbs-dir .fb-breadcrumbs-dir-name",
        cls=ButtonWithTextPageObject,
    )
    space_root = Button(".fb-breadcrumbs-dir-root")
    menu_button = Button(".fb-breadcrumbs-current-dir-button")

    def __str__(self):
        return f"Breadcrumbs({self.pwd()}) in {self.parent}"

    def pwd(self):
        return "/".join(directory.text for directory in self._breadcrumbs)

    def chdir(self, path, archive=False):
        if not path or path == "/":
            self.space_root()
        else:
            path = path.split("/")
            breadcrumbs = self._breadcrumbs
            assert len(path) <= len(
                breadcrumbs
            ), f"specified path {path} exceeded one displayed in breadcrumbs {self}"

            i, dir1, dir2 = None, None, None
            err_msg = "{dir} not found on {idx}th position in {item}"
            if archive:
                breadcrumbs = [elem for i, elem in enumerate(breadcrumbs) if i != 1]

            breadcrumbs_name = [item.text for item in breadcrumbs]

            # works only if '...' is after archive name in path
            if "..." in breadcrumbs_name:
                path[1] = "..."
                if len(breadcrumbs_name) < len(path):
                    for i in range(2, 2 + (len(path) - len(breadcrumbs))):
                        path.remove(path[i])

                for i, (dir1, dir2) in enumerate(zip(path, breadcrumbs_name)):
                    if i == 0:
                        continue
                    assert dir1 == dir2, err_msg.format(dir=dir1, idx=i, item=self)
                breadcrumbs[breadcrumbs_name.index(dir2) - 1].click()
            else:
                for i, (dir1, dir2) in enumerate(zip(path, breadcrumbs)):
                    if i == 0:
                        continue
                    assert dir1 == dir2.text, err_msg.format(dir=dir1, idx=i, item=self)
                dir2.click()

    def go_one_back(self):
        breadcrumbs = self._breadcrumbs
        if len(breadcrumbs) - 2 < 0:
            raise RuntimeError(f"Cannot go back in breadcrumbs {breadcrumbs}")
        breadcrumbs[len(breadcrumbs) - 2].click()

    @property
    def breadcrumbs(self):
        return self._breadcrumbs


Breadcrumbs = partial(WebItem, cls=_Breadcrumbs)
