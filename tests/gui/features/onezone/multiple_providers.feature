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

  Scenario: User can see correct opened provider tab after opening provider settings in Providers sections of a space
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Providers" of "space1" space in the sidebar
    And user of browser opens "oneprovider-1" provider menu on space providers data page
    Then user of browser opens "Settings" option on space providers menu in provider menu in provider section in space
    And user of browser can see "oneprovider-1" is selected in tab in header in the settings section in the space provider page
    And user of browser can see "oneprovider-1" provider name is displayed in the message in the settings section in the space provider page

  Scenario: User can see correct opened provider tab after opening provider file browser in Providers sections of a space
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Providers" of "space1" space in the sidebar
    And user of browser opens "oneprovider-1" provider menu on space providers data page
    Then user of browser opens "Browse files" option on space providers menu in provider menu in provider section in space
    And user of browser sees current provider named "oneprovider-1" on file browser page