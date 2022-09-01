Feature: Basic management of providers in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: space-owner-user
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User opens provider popup by clicking on supporting provider in data page
    When user of browser clicks on Providers in the main menu
    And user of browser clicks on provider "oneprovider-1" in providers sidebar
    Then user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map


  Scenario: User can go to Oneprovider by clicking on Visit provider in provider's popup
    When user of browser clicks on Providers in the main menu
    And user of browser clicks on provider "oneprovider-1" in providers sidebar
    And user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map

    Then user of browser clicks on Visit provider button on provider popover
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees current provider named "oneprovider-1" on file browser page


  Scenario: User sees that provider popup can be closed with clicking on map
    When user of browser clicks on Providers in the main menu
    And user of browser clicks on provider "oneprovider-1" in providers sidebar
    And user of browser clicks on Onezone world map
    Then user of browser does not see provider popover on Onezone world map


  Scenario: User sees that if space is displayed in provider in Data, that provider is also displayed in provider in Spaces
    When user of browser clicks on Providers in the main menu
    And user of browser clicks on provider "oneprovider-1" in providers sidebar
    And user of browser sees "space1" is on the spaces list on provider popover
    And user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Providers" of "space1" space in the sidebar
    Then user of browser sees "oneprovider-1" is on the providers list


    # TODO: uncomment after space unsupport fixes in 21.02 (VFS-6383)
#  Scenario: User sees that if space is unsupported by provider, the provider is not displayed in that space providers list
#    When user of browser clicks on Data in the main menu
#    And user of browser clicks "space1" on the spaces list in the sidebar
#    And user of browser clicks "Providers" of "space1" space in the sidebar
#    And user of browser revokes space support of "oneprovider-1" provider in oneproviders list in data sidebar
#    Then user of browser clicks "space1" on the spaces list in the sidebar
#    And user of browser clicks "Providers" of "space1" space in the sidebar
#    And user of browser sees that length of providers list of "space1" equals "0"
