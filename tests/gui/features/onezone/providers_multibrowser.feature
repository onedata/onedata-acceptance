Feature: Basic management of providers in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user2
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: space-owner-user
              home space for:
                  - space-owner-user
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
          space2:
              owner: space-owner-user
              home space for:
                  - space-owner-user
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
          space3:
              owner: space-owner-user
              home space for:
                  - space-owner-user


    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, oneprovider-1 provider panel] page
    And user of [space_owner_browser, browser1] logged as [space-owner-user, admin] to [Onezone, emergency interface of Onepanel] service


  Scenario: User sees that after unsupporting space, number displayed in space counter for given provider decreases
    When user of space_owner_browser clicks on Providers in the main menu
    And user of space_owner_browser clicks on provider "oneprovider-1" in providers sidebar
    And user of space_owner_browser sees that spaces counter for "oneprovider-1" provider displays 2 in data sidebar
    And user of space_owner_browser sees that length of spaces list on provider popover is 2

    # unsupport space
    And user of browser1 clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 expands toolbar for "space2" space record in Spaces page in Onepanel
    And user of browser1 clicks on Revoke space support option in space's toolbar in Onepanel
    And user of browser1 checks the understand notice in cease oneprovider support for space modal in Onepanel
    And user of browser1 clicks on Cease support button in cease oneprovider support for space modal in Onepanel
    And user of browser1 sees an info notify with text matching to: Ceased.*[Ss]upport.*

    # confirm results
    And user of space_owner_browser is idle for 8 seconds
    Then user of space_owner_browser sees that spaces counter for "oneprovider-1" provider displays 1 in data sidebar
    And user of space_owner_browser sees that length of spaces list on provider popover is 1


  Scenario: User sees provider on the space providers map after supporting
    When user of space_owner_browser clicks Overview of "space3" in the sidebar
    And user of space_owner_browser sees no providers on the map on "space3" space overview data page
    And user of space_owner_browser sends support token for "space3" to user of browser1

    And user of browser1 supports "space3" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 10000

    And user of space_owner_browser clicks Overview of "space3" in the sidebar
    And user of space_owner_browser sees 1 provider on the map on "space3" space overview data page
    And user of space_owner_browser clicks the map on "space3" space overview data page

    Then user of space_owner_browser sees 1 provider on the map on "space3" space providers data page
    And user of space_owner_browser sees "oneprovider-1" is on the providers list
    And user of space_owner_browser clicks "oneprovider-1" provider icon on the map on providers data page

    And user of space_owner_browser sees that provider popup for provider "oneprovider-1" has appeared on world map
