"""Utils to facilitate provider operations in op panel GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.web_elements import (Label, NamedButton,
                                               Input, Button, WebItem)


class ProviderDetailsCommon(PageObject):
    id = Label('.field-main-id')
    urls = Label('.field-main-urls')


class ProviderDetails(ProviderDetailsCommon):
    provider_name = Label('.field-showTop-name')
    domain = Label('.field-showDomain-domain')
    latitude = Label('.field-showBottom-geoLatitude')
    longitude = Label('.field-showBottom-geoLongitude')


class ModifyProviderDetailsForm(ProviderDetailsCommon):
    provider_name = Input('input.field-editTop-name')
    domain = Input('input.field-editDomain-domain')
    subdomain = Input('input.field-editSubdomain-subdomain')
    latitude = Input('input.field-editBottom-geoLatitude')
    longitude = Input('input.field-editBottom-geoLongitude')
    modify_provider_details = NamedButton('button',
                                          text='Modify provider details')
    subdomain_delegation = Toggle('.one-way-toggle.toggle-field-editTop'
                                  '-subdomainDelegation')


class ProviderContentPage(PageObject):
    details = WebItem('.provider-registration-form', cls=ProviderDetails)
    form = WebItem('.provider-registration-form', cls=ModifyProviderDetailsForm)
    modify_provider_details = NamedButton('button.btn-modify-provider',
                                          text='Modify provider details')
    cancel_modifying = NamedButton('button.btn-modify-provider',
                                   text='Cancel modifying')
    deregister_provider = Button('button.btn-deregister-provider')
