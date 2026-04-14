Feature: Onezone behaviour with multiple providers
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

  Scenario: User opens a popup for a space's provider and goes into provider's settings
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Providers" of "space1" space in the sidebar
    And user of browser opens "oneprovider-1" provider menu on space providers data
    And user of browser opens "oneprovider-1" provider settings on space providers
    And user of browser reads "oneprovider-1" provider name on space provider settings menu
    
#   Scenario: User opens a popup for a space's provider and goes into provider's file browser