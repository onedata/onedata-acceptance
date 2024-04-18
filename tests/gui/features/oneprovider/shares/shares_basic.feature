Feature: Oneprovider shares basic functionality

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
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                        - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario Outline: User selects desirable columns to be visible and can see only them in files table
    When user of browser opens file browser for "space1" space
    And user of browser creates "share_dir1" share of "dir1" directory
    And user of browser clicks on "share_dir1" share link with icon in shares panel
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser enables only <columns_list> columns in columns configuration popover in file browser table
    Then user of browser sees only <columns_list> columns in file browser
    And user of browser refreshes site
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees only <columns_list> columns in file browser

  Examples:
    |columns_list            |
    |["Size", "Modified"]|
    |[]                      |