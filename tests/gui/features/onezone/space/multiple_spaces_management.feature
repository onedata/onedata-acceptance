Feature: Management of multiple spaces in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
        space2:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees that after going to Oneprovider the home space is automatically loaded into view
    When user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser sets space named "space2" as home by clicking on home outline in that space record in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser expands submenu of space named "space1" by clicking on space record in expanded "DATA SPACE MANAGEMENT" Onezone panel

    # go to provider
    And user of browser clicks on provider "oneprovider-1" in submenu of space named "space1" in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map
    And user of browser clicks on the "Go to your files" button in "oneprovider-1" provider's popup displayed on world map

    # check displayed space
    And user of browser sees that Oneprovider session has started
    And user of browser is idle for 15 seconds
    And user of browser refreshes webapp
    Then user of browser sees that displayed directory tree in sidebar panel belongs to home space named "space2"


  Scenario: User sees that after going to Oneprovider, without having any home space, the first one alphabetically is loaded into view
    When user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser expands submenu of space named "space2" by clicking on space record in expanded "DATA SPACE MANAGEMENT" Onezone panel

    # go to provider
    And user of browser clicks on provider "oneprovider-1" in submenu of space named "space2" in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map
    And user of browser clicks on the "Go to your files" button in "oneprovider-1" provider's popup displayed on world map

    # check displayed space
    And user of browser sees that Oneprovider session has started
    Then user of browser sees that displayed directory tree in sidebar panel belongs to space named "space1"


  Scenario: User changes viewed space in Oneprovider
    When user of browser expands the "DATA SPACE MANAGEMENT" Onezone sidebar panel
    And user of browser expands submenu of space named "space2" by clicking on space record in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser clicks on provider "oneprovider-1" in submenu of space named "space2" in expanded "DATA SPACE MANAGEMENT" Onezone panel
    And user of browser sees that provider popup for provider "oneprovider-1" has appeared on world map
    And user of browser clicks on the "Go to your files" button in "oneprovider-1" provider's popup displayed on world map
    And user of browser sees that Oneprovider session has started

    And user of browser sees that displayed directory tree in sidebar panel belongs to space named "space1"
    And user of browser uses spaces select to change data space to "space2"
    Then user of browser sees that displayed directory tree in sidebar panel belongs to space named "space2"
