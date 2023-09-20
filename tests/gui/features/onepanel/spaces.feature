Feature: Basic spaces management utilities using onepanel

  Background:
    Given admin user does not have access to any space
    And there are no spaces supported by oneprovider-1 in Onepanel
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser1, browser2] logged as [admin, admin] to [Onezone, emergency interface of Onepanel] service


  Scenario Outline: Support space
    When user of browser1 creates "space1" space in Onezone

    # receive support token
    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks "Providers" of "space1" space in the sidebar
    And user of browser1 clicks Add support button on providers page
    And user of browser1 clicks Copy button on Add support page
    And user of browser1 sees an info notify with text matching to: .*copied.*
    And user of browser1 sends copied token to user of <client>

    # support space
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser is idle for 1 second
    And user of <client> clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of <client> clicks on Support space button in spaces page in Onepanel if there are some spaces already supported
    And user of <client> selects "posix" from storage selector in support space form in Onepanel
    And user of <client> types received token to Support token field in support space form in Onepanel
    And user of <client> types "1" to Size input field in support space form in Onepanel
    And user of <client> selects GiB radio button in support space form in Onepanel
    And user of <client> clicks on Support space button in support space form in Onepanel
    And user of <client> sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of <client> sees that space support record for "space1" has appeared in Spaces page in Onepanel

    # confirm support of space
    Then user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks "Providers" of "space1" space in the sidebar
    And user of browser1 sees "oneprovider-1" is on the providers list

    Examples:
    | client   |
    | browser1 |
    | browser2 |

  # TODO: uncomment after space unsupport fixes in 21.02 (VFS-6383)
#  Scenario Outline: Revoke space support
#    When user of browser1 creates "space1" space in Onezone
#    And user of browser1 sends support token for "space1" to user of browser2
#    And user of browser2 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
#          storage: posix
#          size: 1
#          unit: GiB
#    # assert space existence and support
#    And user of browser1 sees that "space1" has appeared on the spaces list in the sidebar
#    And user of browser1 clicks "space1" on the spaces list in the sidebar
#    And user of browser1 clicks "Providers" of "space1" space in the sidebar
#    And user of browser1 sees "oneprovider-1" is on the providers list
#    And user of browser1 sees that length of providers list of "space1" equals "1"
#
#    # unsupport space
#    And user of browser1 clicks on Clusters in the main menu
#    And user of browser1 clicks on "oneprovider-1" in clusters menu
#    And user of browser is idle for 1 second
#    And user of <client> clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
#    And user of <client> expands toolbar for "space1" space record in Spaces page in Onepanel
#    And user of <client> clicks on Revoke space support option in space's toolbar in Onepanel
#    And user of <client> checks the understand notice in cease oneprovider support for space modal in Onepanel
#    And user of <client> clicks on Cease support button in cease oneprovider support for space modal in Onepanel
#    And user of <client> sees an info notify with text matching to: Ceased.*[Ss]upport.*
#
#    # confirm lack of support for space
#    Then user of browser1 clicks "space1" on the spaces list in the sidebar
#    And user of browser1 clicks "Providers" of "space1" space in the sidebar
#    And user of browser1 sees that length of providers list of "space1" equals "0"
#
#    Examples:
#    | client   |
#    | browser1 |
#    | browser2 |


  # TODO: delete after space support revoke fixes in 21.02 (VFS-6383)
  Scenario: User successfully deletes space instead of revoking it
    When user of browser1 creates "space1" space in Onezone
    And user of browser1 sends support token for "space1" to user of browser2
    And user of browser2 supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB
    # assert space existence and support
    And user of browser1 sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks "Providers" of "space1" space in the sidebar
    And user of browser1 sees "oneprovider-1" is on the providers list
    And user of browser1 sees that length of providers list of "space1" equals "1"

    # unsupport space
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser is idle for 1 second
    And user of browser1 clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 expands toolbar for "space1" space record in Spaces page in Onepanel
    And user of browser1 clicks on Revoke space support option in space's toolbar in Onepanel
    And user of browser1 removes space using delete space modal invoked from provided link
    Then user of browser1 sees that "space1" has disappeared on the spaces list in the sidebar

