"""Utils to facilitate operations on docs sidebars on Onedata documentation"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import ButtonWithTextPageObject, WebItemsSequence
from tests.gui.utils.core.web_objects import PageObject


class DocsSidebar(PageObject):
    category_rows = WebItemsSequence("a", cls=ButtonWithTextPageObject)
    expanded_folders = WebItemsSequence(
        ".sidebar-folder.expanded", cls=ButtonWithTextPageObject
    )

    def get_active_rows_names(self):
        return [row.id for row in self.category_rows if row.is_active()]

    def get_expanded_folders_names(self):
        return [folder.id.split("\n")[0] for folder in self.expanded_folders]
