Feature: Basic spaces management utilities using onepanel

  Background:
    Given users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [oneprovider-1 provider panel, Onezone] page
    And user of [browser1, browser2] logged as [admin, admin] to [Onepanel, Onezone] service


  Scenario: Support space
    Given there are no spaces supported in Onepanel used by user of browser1

    # create space
    When user of browser2 clicks on Create space button in spaces sidebar
    And user of browser2 writes "helloworld" into space name text field
    And user of browser2 clicks on Create new space button
    And user of browser2 sees that "helloworld" has appeared on the spaces list in the sidebar

    # receive support token
    And user of browser2 clicks "helloworld" on the spaces list in the sidebar
    And user of browser2 clicks Providers of "helloworld" in the sidebar
    And user of browser2 clicks Get support button on providers page
    And user of browser2 clicks Copy button on Get support page
    And user of browser2 sees an info notify with text matching to: .*copied.*
    And user of browser2 sends copied token to user of browser1

    # support space
    And user of browser1 clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on Support space button in spaces page in Onepanel if there are some spaces already supported
    And user of browser1 selects "posix" from storage selector in support space form in Onepanel
    And user of browser1 types received token to Support token field in support space form in Onepanel
    And user of browser1 types "1" to Size input field in support space form in Onepanel
    And user of browser1 selects GiB radio button in support space form in Onepanel
    And user of browser1 clicks on Support space button in support space form in Onepanel
    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "helloworld" has appeared in Spaces page in Onepanel

    # confirm support of space
    And user of browser2 clicks "helloworld" on the spaces list in the sidebar
    And user of browser2 clicks Providers of "helloworld" in the sidebar
    And user of browser2 sees "oneprovider-1" is on the providers list


  Scenario: Revoke space support
    # assert space existence and support
    When user of browser2 sees that "helloworld" has appeared on the spaces list in the sidebar
    And user of browser2 clicks "helloworld" on the spaces list in the sidebar
    And user of browser2 clicks Providers of "helloworld" in the sidebar
    And user of browser2 sees "oneprovider-1" is on the providers list
    And user of browser2 sees that length of providers list of "helloworld" equals "1"

    # unsupport space
    And user of browser1 clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 expands toolbar for "helloworld" space record in Spaces page in Onepanel
    And user of browser1 clicks on Revoke space support option in space's toolbar in Onepanel
    And user of browser1 clicks on Yes, revoke button in REVOKE SPACE SUPPORT modal in Onepanel
    And user of browser1 sees an info notify with text matching to: .*[Ss]upport.*revoked.*

    # confirm lack of support for space
    And user of browser2 clicks "helloworld" on the spaces list in the sidebar
    And user of browser2 clicks Providers of "helloworld" in the sidebar
    And user of browser2 sees that length of providers list of "helloworld" equals "0"
