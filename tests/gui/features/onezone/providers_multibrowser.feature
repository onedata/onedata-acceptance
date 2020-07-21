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

    And users opened [browser_unified, browser_emergency] browsers' windows
    And users of [browser_unified, browser_emergency] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser_unified, browser_emergency] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service


  Scenario: User sees that after unsupporting space, number displayed in space counter for given provider decreases
    When user of browser_unified clicks on Providers in the main menu
    And user of browser_unified clicks on provider "oneprovider-1" in providers sidebar
    And user of browser_unified sees that spaces counter for "oneprovider-1" provider displays 2 in data sidebar
    And user of browser_unified sees that length of spaces list on provider popover is 2

    # unsupport space
    And user of browser_emergency clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_emergency expands toolbar for "space2" space record in Spaces page in Onepanel
    And user of browser_emergency clicks on Revoke space support option in space's toolbar in Onepanel
    And user of browser_emergency checks the understand notice in cease oneprovider support for space modal in Onepanel
    And user of browser_emergency clicks on Cease support button in cease oneprovider support for space modal in Onepanel
    And user of browser_emergency sees an info notify with text matching to: Ceased.*[Ss]upport.*

    # confirm results
    And user of browser_unified is idle for 8 seconds
    Then user of browser_unified sees that spaces counter for "oneprovider-1" provider displays 1 in data sidebar
    And user of browser_unified sees that length of spaces list on provider popover is 1

