"""Utils to facilitate operations on the Docs page of Onedata homepage."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import (
    ButtonWithTextPageObject,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.homepage.documentation_base import (
    BaseDocumentationPage,
    BaseDocumentationSidebar,
)


class DocsSidebar(BaseDocumentationSidebar):
    category_rows = WebItemsSequence("a", cls=ButtonWithTextPageObject)

    def get_active_rows_names(self) -> list[str]:
        return [row.text for row in self.category_rows if row.is_active()]


class DocsPage(BaseDocumentationPage):
    sidebar = WebItem(".sidebar-root-list", cls=DocsSidebar)
