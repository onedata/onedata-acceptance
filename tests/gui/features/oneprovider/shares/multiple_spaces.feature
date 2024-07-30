Feature: Share management with multiple spaces in Oneprovider GUI


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
        space2:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir2

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: Names of spaces in SHARES sidebar in Onepanel are displayed correctly
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Share / Publish" option in data row menu in file browser
    And user of browser sees that "Share / Publish directory" modal has appeared
    And user of browser writes "share_dir1" into text field in modal "Share / Publish directory"
    And user of browser clicks on "Create" button in modal "Share / Publish directory"

    And user of browser opens file browser for "space2" space
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Share / Publish" option in data row menu in file browser
    And user of browser sees that "Share / Publish directory" modal has appeared
    And user of browser writes "share_dir2" into text field in modal "Share / Publish directory"
    And user of browser clicks on "Create" button in modal "Share / Publish directory"

    And user of browser clicks on Shares in the main menu
    Then user of browser sees share "share_dir1" from "space1" space
    And user of browser sees share "share_dir2" from "space2" space