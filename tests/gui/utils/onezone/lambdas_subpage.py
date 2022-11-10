"""Utils to facilitate operations on lambdas subpage of automation page in
Onezone gui """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label, \
    Button, WebItem, WebElement
from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import Element


class LambdaArgument(PageObject):
    add_argument = Button('.add-field-button')
    argument_name = WebItem('.entryName-field .text-like-field', cls=InputBox)
    type_dropdown = WebElement('.entryDataSpec-field '
                               '.ember-power-select-trigger')


class LambdaResult(PageObject):
    add_result = Button('.add-field-button')
    result_name = WebItem('.entryName-field .text-like-field', cls=InputBox)
    type_dropdown = WebElement('.entryDataSpec-field '
                               '.ember-power-select-trigger')


class LambdaArguments(PageObject):
    add_argument = Button('.add-field-button')
    bracket_1st = WebItem('.collection-item:nth-child(1) ', cls=LambdaArgument)
    bracket_2nd = WebItem('.collection-item:nth-child(2) ', cls=LambdaArgument)
    bracket_3rd = WebItem('.collection-item:nth-child(3) ', cls=LambdaArgument)


class LambdaResults(PageObject):
    add_result = Button('.add-field-button')
    bracket_1st = WebItem('.collection-item:nth-child(1) ', cls=LambdaResult)
    bracket_2nd = WebItem('.collection-item:nth-child(2) ', cls=LambdaResult)
    bracket_3rd = WebItem('.collection-item:nth-child(3) ', cls=LambdaResult)


class LambdaAddForm(PageObject):
    lambda_name = WebItem('.name-field .text-like-field', cls=InputBox)
    docker_image = WebItem('.dockerImage-field .text-like-field', cls=InputBox)

    mount_space_toggle = Toggle('.mountSpace-field .form-control')
    read_only_toggle = Toggle('.readonly-field .form-control')

    argument = WebItem('.arguments-field ', cls=LambdaArguments)
    result = WebItem('.results-field ', cls=LambdaResults)

    create_button = Button('.btn-primary')


class Revision(Element):
    number = id = Label('.revision-number')
    name = Label('.name')
    menu_button = Button('.one-menu-toggle')

    add_to_workflow = Button('.add-to-workflow-action-trigger')


class Lambda(Element):
    name = id = Label('.lambda-name')
    menu_button = Button('.one-menu-toggle')
    create_new_revision = Button('.create-atm-lambda-revision-action-trigger')
    show_revisions_button = Button('.expand-button')
    revision_list = WebItemsSequence('.revisions-table '
                                     '.revisions-table-revision-entry',
                                     cls=Revision)


class LambdasPage(PageObject):
    elements_list = WebItemsSequence('.atm-lambdas-list'
                                     ' .atm-lambdas-list-entry', cls=Lambda)
    form = WebItem('.atm-lambda-form ', cls=LambdaAddForm)
