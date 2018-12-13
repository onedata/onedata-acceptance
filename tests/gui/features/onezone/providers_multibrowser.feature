Feature: Basic management of providers in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              home space for:
                  - user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
          space2:
              owner: user1
              home space for:
                  - user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser1, browser2] logged as [user1, admin] to [Onezone, Onepanel] service


  Scenario: User sees that after unsupporting space, number displayed in space counter for given provider decreases
    When user of browser1 clicks on Data in the main menu
    And user of browser1 clicks on provider "oneprovider-1" in data sidebar
    And user of browser1 sees that spaces counter for "oneprovider-1" provider displays 2 in data sidebar
    And user of browser1 sees that length of spaces list on provider popover is 2

    # unsupport space
    And user of browser2 clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 expands toolbar for "space1" space record in Spaces page in Onepanel
    And user of browser2 clicks on Revoke space support option in space's toolbar in Onepanel
    And user of browser2 clicks on Yes, revoke button in REVOKE SPACE SUPPORT modal in Onepanel
    And user of browser2 sees an info notify with text matching to: .*[Ss]upport.*revoked.*

    # confirm results
#    And user of browser1 is idle for 8 seconds
    Then user of browser1 sees that spaces counter for "oneprovider-1" provider displays 1 in data sidebar
    And user of browser1 sees that length of spaces list on provider popover is 1

