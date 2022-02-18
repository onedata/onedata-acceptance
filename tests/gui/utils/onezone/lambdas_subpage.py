"""Utils to facilitate operations on lambdas subpage of automation page in
Onezone gui """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Input, Label, \
    Button, WebItem, NamedButton
from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import Element


class LambdaAddForm(PageObject):
    lambda_name = WebItem('.name-field .text-like-field', cls=InputBox)
    docker_image = WebItem('.dockerImage-field .text-like-field', cls=InputBox)
    create_button = Button('.btn-primary')


class Revision(Element):
    name = id = Label('.name')
    menu_button = Button('.one-menu-toggle')


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
