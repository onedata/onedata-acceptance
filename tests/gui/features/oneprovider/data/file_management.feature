Feature: Basic file management operations


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
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                        - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User successfully pastes file copied from other directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser double clicks on item named "dir1" in file browser
    And user of browser selects "file1" items from file browser with pressed ctrl
    And user of browser chooses Copy option from selection menu on file browser page
    And user of browser changes current working directory to home using breadcrumbs
    And user of browser clicks "Paste" button from file browser menu bar
    Then user of browser sees items named ["dir1", "file1"] in file browser in given order
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees items named "file1" in file browser in given order

  Scenario: User successfully pastes file cut from other directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser double clicks on item named "dir1" in file browser
    And user of browser selects "file1" items from file browser with pressed ctrl
    And user of browser chooses Cut option from selection menu on file browser page
    And user of browser changes current working directory to home using breadcrumbs
    And user of browser clicks "Paste" button from file browser menu bar
    Then user of browser sees items named ["dir1", "file1"] in file browser in given order
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees empty directory message in file browser