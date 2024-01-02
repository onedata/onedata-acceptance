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

    And users opened [space_owner_browser, browser1] browsers' windows
    And user of space_owner_browser opened onezone page
    And user of space_owner_browser logged as space-owner-user to Onezone service


  Scenario Outline: User selects desirable columns to be visible and can see only them in transfers table
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates "share_dir1" share of "dir1" directory
    And user of space_owner_browser hands "share_dir1" share's URL of "dir1" to user of browser1

    # opening share by user of browser1
    And user of browser1 opens received URL
    And user of browser1 sees that public share is named "share_dir1"

    And user of browser1 sees that current working directory path visible in share's public interface file browser is as follows: share_dir1
    And user of browser1 sees file browser on share's public interface
    And user of browser1 clicks and presses enter on item named "dir1" in file browser

    And user of browser1 enables only <columns_list> columns in columns configuration popover in file browser table
    Then user of browser1 sees only <columns_list> columns in file browser
    And user of browser1 refreshes site
    And user of browser1 sees file browser in files tab on share's public interfac in Oneprovider page
    And user of browser1 sees only <columns_list> columns in file browser

  # in standard browser view max 3 columns can be displayed
  Examples:
    |columns_list                              |
    |["Size", "Modification"]                |
    |[]|