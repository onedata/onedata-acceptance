Feature: Management of providers on world map in Onezone GUI


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
                  - oneprovider-2:
                      storage: posix
                      size: 1000000

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: Oneprovider-1 circle is placed east of oneprovider-2 circle on world map
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    And user of browser sees "oneprovider-1" is on the providers list
    And user of browser sees "oneprovider-2" is on the providers list
    Then user of browser sees that provider "oneprovider-1" is placed east of "oneprovider-2" on world map