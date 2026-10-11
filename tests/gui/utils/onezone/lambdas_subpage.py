"""Utils to facilitate operations on lambdas subpage of automation page in
Onezone gui"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import NamedElement, PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import ListPage


class FileAttr(PageObject):
    x = Button(".tag-remove")


class ParameterSetting(PageObject):
    file_type = Button(".fileType-field .field-component")
    carried_file_attrs = Button(".fileAttributes-field .field-component")
    attributes = WebItemsSequence(".tag-item", cls=FileAttr)


class LambdaParameter(PageObject):
    add_button = Button(".add-field-button", scroll=False)
    name = WebItem(".entryName-field .text-like-field", cls=InputBox)
    type_dropdown = WebElement(".entryDataSpec-field .ember-power-select-trigger", scroll=False)
    remove_element = Button(".remove-trigger", scroll=False)
    settings = Button(".oneicon-settings", scroll=False)
    parameter_settings = WebItem(".dataTypeEditor-children", cls=ParameterSetting)
    default_data_type = WebElement(".default-data-type-editor .data-type-header", scroll=False)
    outer_data_type = WebElement(
        ".data-type-editor > .data-type-header:not(.data-type-editor-default .data-type-header)",
        scroll=False,
    )

    def get_default_type(self) -> str:
        return self.default_data_type.text

    def get_outer_type(self) -> str:
        return self.outer_data_type.text


class LambdaParameters(PageObject):
    label = WebElement(":scope > label.control-label")
    add_button = Button(".add-field-button")
    bracket_1st = WebItem(".collection-item:nth-child(1)", cls=LambdaParameter)
    bracket_2nd = WebItem(".collection-item:nth-child(2)", cls=LambdaParameter)
    bracket_3rd = WebItem(".collection-item:nth-child(3)", cls=LambdaParameter)


class LambdaAddForm(PageObject):
    lambda_name = WebItem(".name-field .text-like-field", cls=InputBox)
    docker_image = WebItem(".dockerImage-field .text-like-field", cls=InputBox)

    mount_space_toggle = Toggle(".mountSpace-field .form-control")
    read_only_toggle = Toggle(".readonly-field .form-control")

    argument = WebItem(".arguments-field", cls=LambdaParameters)
    result = WebItem(".results-field", cls=LambdaParameters)
    configuration_parameters = WebItem(".configParameters-field", cls=LambdaParameters)
    create_button = Button(".btn-primary")


class Revision(NamedElement):
    number = id = Label(".revision-number")
    name = Label(".name")
    menu_button = Button(".one-menu-toggle")

    add_to_workflow = Button(".add-to-workflow-action-trigger")


class Lambda(NamedElement):
    name = id = Label(".lambda-name")
    lambda_menu = Button(".atm-lambda-actions-trigger.one-menu-toggle")
    menu_button = Button(".one-menu-toggle")
    create_new_revision = Button(".create-atm-lambda-revision-action-trigger")
    show_revisions_button = Button(".expand-button")
    revision_list = WebItemsSequence(
        ".revisions-table .revisions-table-revision-entry", cls=Revision
    )


class LambdasPage(ListPage):
    lambdas_list = WebItemsSequence(".atm-lambdas-list .atm-lambdas-list-entry", cls=Lambda)
    form = WebItem(".atm-lambda-form ", cls=LambdaAddForm)
