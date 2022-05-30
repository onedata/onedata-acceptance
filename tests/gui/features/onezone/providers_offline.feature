Feature: Basic management of providers offline in Onezone GUI


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


  Scenario: User sees "All your providers are offline" message when no provider is online
    Given provider named "oneprovider-1" is stopped
    When user of browser waits until provider "oneprovider-1" goes offline on providers map

    And user of browser clicks on Data in the main menu
    And user of browser clicks Files of "space1" space in the sidebar

    Then user of browser sees alert with title "ALL SUPPORTING ONEPROVIDERS ARE OFFLINE" on Onezone page
    And user of browser waits until provider "oneprovider-1" goes online on providers map
