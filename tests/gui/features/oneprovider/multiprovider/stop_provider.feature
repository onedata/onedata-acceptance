Feature: Operations when current provider stops

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
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                        - file1: 11111
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees space's size stats per provider after clicking show statistics, then oneprovider-2 is stopped and user sees error message
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser opens size statistics per provider view using breadcrumbs menu in "space1"
    Then user of browser sees that logical_size for oneprovider-1 is "5 B"
    And user of browser sees that logical_size for oneprovider-2 is "5 B"
    And user of browser sees that physical_size for oneprovider-1 is "5 B"
    And user of browser sees that physical_size for oneprovider-2 is "0 B"
    And user of browser sees that oneprovider-1 content is "1 file, 1 directory"
    And user of browser sees that oneprovider-2 content is "1 file, 1 directory"
    And provider named oneprovider-2 is stopped
    And user of browser sees that error message for oneprovider-2 is "Proxy error: no connection to peer Oneprovider."

    And user of browser clicks on Data in the main menu
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser waits until provider "oneprovider-2" goes online on providers map


  Scenario: User switches to oneprovider-2 after oneprovider-1 has been stopped
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And provider named oneprovider-1 is stopped
    Then user of browser sees "SELECTED ONEPROVIDER IS CURRENTLY OFFLINE" error on spaces page
    And user of browser clicks on Choose other Oneprovider on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page
