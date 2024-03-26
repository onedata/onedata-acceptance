"""Operations on files structure in data tab in Oneprovider
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.browser import (
    assert_only_expected_items_presence_in_browser,
    click_and_press_enter_on_item_in_browser,
    assert_num_of_files_are_displayed_in_browser,
    check_if_item_is_dir_in_browser)
from tests.gui.steps.oneprovider.data_tab import (
    has_downloaded_file_content,
    go_one_back_using_breadcrumbs_in_data_tab_in_op)
from tests.gui.utils.oneprovider.file_browser.file_tree_node import Node


def build_tree_config(data):
    root = Node('root')
    root.path = ''
    _build_tree_config(data, root)
    return root


def _build_tree_config(data, parent: Node):
    for item in data:
        try:
            [(item_name, item_subtree)] = item.items()
            node = Node(item_name)
            node.set_parent(parent)
            parent.nodes.append(node)
            if isinstance(item_subtree, list):
                _build_tree_config(item_subtree, node)
            else:
                node.content = item_subtree
        except AttributeError:
            node = Node(item)
            node.set_parent(parent)
            parent.nodes.append(node)


def check_tree_browser(
        parent: Node, selenium, user, tmp_memory, op_container, tmpdir,
        which_browser):
    assert_only_expected_items_presence_in_browser(
        selenium, user, parent.get_items(), tmp_memory, which_browser)
    for child in parent.nodes:
        if check_if_item_is_dir_in_browser(
                selenium, user, child.name, tmp_memory, which_browser):
            click_and_press_enter_on_item_in_browser(
                selenium, user, child.name, tmp_memory, op_container,
                which_browser)
            if child.content is not None:
                # checking only number of children
                assert_num_of_files_are_displayed_in_browser(
                    user, int(child.content), tmp_memory, which_browser)
            else:
                check_tree_browser(
                    child, selenium, user, tmp_memory, op_container, tmpdir,
                    which_browser)
            go_one_back_using_breadcrumbs_in_data_tab_in_op(
                selenium, user, op_container, which_browser)
        elif child.content is not None:
            click_and_press_enter_on_item_in_browser(
                selenium, user, child.name, tmp_memory, op_container, which_browser)
            has_downloaded_file_content(
                user, child.name, str(child.content), tmpdir)


@wt(parsers.re(r'user of (?P<browser_id>\w+) sees that the (file|item) '
               'structure in (?P<which_browser>.*) '
               r'is as follow:\n(?P<config>(.|\s)*)'))
@wt(parsers.re(r'user of (?P<browser_id>\w+) sees that the file structure '
               'for archive with description: "(?P<description>.*)" '
               'in (?P<which_browser>.*) '
               r'is as follow:\n(?P<config>(.|\s)*)'))
def check_file_structure_in_browser(
        browser_id, config, selenium, tmp_memory, op_container, tmpdir,
        which_browser='file browser'):
    tree = yaml.load(config)
    root = build_tree_config(tree)
    check_tree_browser(
        root, selenium, browser_id, tmp_memory, op_container, tmpdir,
        which_browser)
