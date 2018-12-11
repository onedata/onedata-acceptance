Feature: Basic management of providers in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              home space for:
                  - user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User opens provider popup by clicking on supporting provider in data page
    When user of browser clicks on Data in the sidebar
    And user of browser clicks on provider "oneprovider-1" in data sidebar
    Then user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map


  Scenario: User can go to Oneprovider by clicking on Visit provider in provider's popup
    When user of browser clicks on Data in the sidebar
    And user of browser clicks on provider "oneprovider-1" in data sidebar
    And user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map
    And user of browser clicks on Visit provider button on provider popover
    And user of browser sees that Oneprovider session has started
    Then user of browser sees that URL matches: https?://[^/]*/#/onedata/data/.*


  Scenario: User sees that provider popup can be closed with clicking on map
    When user of browser clicks on Data in the sidebar
    And user of browser clicks on provider "oneprovider-1" in data sidebar
    And user of browser clicks on Onezone world map
    Then user of browser does not see provider popover on Onezone world map


  Scenario: User sees that if space is displayed in provider in Data, that provider is also displayed in provider in Spaces
    When user of browser clicks on Data in the sidebar
    And user of browser clicks on provider "oneprovider-1" in data sidebar
    And user of browser sees "space1" is on the spaces list on provider popover
    And user of browser clicks on Spaces in the sidebar
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    Then user of browser sees "oneprovider-1" is on the providers list


  Scenario: User sees that home space of provider should have "cloud with home" icon
    When user of browser clicks on Data in the sidebar
    And user of browser clicks on provider "oneprovider-1" in data sidebar
    Then user of browser sees that home of "oneprovider-1" has appeared in the data sidebar


  Scenario: User sees that when no provider is working appropriate msg is shown
    Given there are no working provider(s) named "oneprovider-1"
    When user of browser expands the "GO TO YOUR FILES" Onezone sidebar panel
    Then user of browser sees that provider "oneprovider-1" in expanded "GO TO YOUR FILES" Onezone panel is not working
    And user of browser sees alert with title "All your providers are offline" on world map in Onezone gui
