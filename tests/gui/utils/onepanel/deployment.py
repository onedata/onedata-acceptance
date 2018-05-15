"""Utils to facilitate deployment steps in panel GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (WebItemsSequence, Label,
                                               Button, NamedButton,
                                               Input, WebItem)
from tests.gui.utils.common.common import Toggle
from .storages import StorageContentPage
from .nodes import HostRecord


class Step1(PageObject):
    """Used in both provider and zone panel"""
    hosts = WebItemsSequence('tr.cluster-host-table-row', cls=HostRecord)
    deploy = Button('button.btn-deploy-cluster')
    zone_name = Input('input.field-main-name')
    zone_domain_name = Input('input.field-main-domainName')

    def __str__(self):
        return str(self.parent)


class Step2(PageObject):
    """Used only in provider panel"""
    provider_name = Input('input.field-editTop-name')
    onezone_domain = Input('input.field-editTop-onezoneDomainName')
    domain = Input('input.field-editDomain-domain')
    subdomain = Input('input.field-editSubdomain-subdomain')
    latitude = Input('input.field-editBottom-geoLatitude')
    longitude = Input('input.field-editBottom-geoLongitude')
    admin_email = Input('input.field-editBottom-adminEmail')
    register = NamedButton('button', text='Register')
    subdomain_delegation = Toggle('.one-way-toggle.toggle-field-editTop-subdomainDelegation') 

    def __str__(self):
        return str(self.parent)


class NodeIP(PageObject):
    hostname = Label('td.cell-hostname')
    ip_address = Input('td.cell-ip-address input')


class SetupIP(PageObject):
    setup_ip_addresses = NamedButton('button', text='Setup IP adresses')
    nodes = WebItemsSequence('tr.cluster-host-ip-form-row', cls=NodeIP)

    def __str__(self):
        return str(self.parent)


class Step4(PageObject):
    next_step = Button('button.btn-cert-next')
    lets_encrypt_toggle = Toggle('.one-way-toggle-control')

    def __str__(self):
        return str(self.parent)


class Step5(StorageContentPage):
    """Used only in provider panel"""
    finish = NamedButton('button', text='Finish')

    def __str__(self):
        return str(self.parent)


class LastStep(PageObject):
    """Used in both provider and zone panel"""
    manage_the_cluster = NamedButton('button', text='Manage the cluster')

    def __str__(self):
        return str(self.parent)


class Deployment(PageObject):
    num = Label('ul.one-steps li.one-step.active .step-number')
    title = Label('ul.one-steps li.one-step.active .step-title',
                  parent_name='cluster deployment step')

    _deployment_step_css = '.steps-row + .row'
    step1 = WebItem(_deployment_step_css, cls=Step1)
    step2 = WebItem(_deployment_step_css, cls=Step2)
    setup_ip = WebItem(_deployment_step_css, cls=SetupIP)
    step4 = WebItem(_deployment_step_css, cls=Step4)
    step5 = WebItem(_deployment_step_css, cls=Step5)
    laststep = WebItem(_deployment_step_css, cls=LastStep)

    def __str__(self):
        return '{} deployment step in {}'.format(self.title, self.parent)
