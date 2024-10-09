"""Utils for GUI tests"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from .common.common import LoginPage, OnePage, PublicOnePage
from .common.modals import Modals
from .common.popups import Popups
from .onepanel import Onepanel
from .oneprovider import OPLoggedIn
from .oneprovider.shares.private_share import PrivateShareView
from .oneprovider.shares.public_share import PublicShareView
from .oneservices.cdmi import CDMIClient
from .onezone import OZLoggedIn
from .onezone.data_discovery_page import DataDiscoveryPage
from .onezone.privacy_policy import PrivacyPolicy
from .onezone.terms_of_use import TermsOfUse
