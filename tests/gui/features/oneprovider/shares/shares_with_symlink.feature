Feature: Shares with linked directories


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
                    - dir1
                    - dir2

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User cannot enter symlinked directory in shared directory which points outside share
    # create share
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir2" file in file browser
    And user of browser clicks "Share" option in data row menu in file browser
    And user of browser clicks on "Create" button in modal "Share directory"
    And user of browser clicks on "Close" button in modal "Share directory"

    # create and place symbolic link
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser clicks "Place symbolic link" button from file browser menu bar

    And user of browser opens shares view of "space1"
    And user of browser clicks "dir2" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser clicks and presses enter on item named "dir2" in file browser
    Then user of browser sees that item named "dir1" is malformed symbolic link in file browser



