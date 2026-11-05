Feature: Data distribution operations for directories


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
                        - file2: 11111
                        - file3: 11111
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User checks directory's data distribution
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Data distribution" option in data row menu in file browser
    Then user of browser sees that data distribution for oneprovider-1 is at 100%
    And user of browser sees that data distribution for oneprovider-2 is at 0%
    And user of browser sees that size distribution for oneprovider-1 is "15 B"
    And user of browser sees that size distribution for oneprovider-2 is "0 B"


  Scenario: User checks directory's data distribution change for oneprovider-2 after file replication
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser replicates "file1" to provider "oneprovider-2"
    And user of browser clicks on menu on breadcrumbs in file browser
    And user of browser clicks "Data distribution" option in menu popup
    Then user of browser sees that data distribution for oneprovider-1 is at 100%
    And user of browser sees that data distribution for oneprovider-2 is at 33%
    And user of browser sees that size distribution for oneprovider-1 is "15 B"
    And user of browser sees that size distribution for oneprovider-2 is "5 B"