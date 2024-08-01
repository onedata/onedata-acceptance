Feature: Basic shares operations in Onezone GUI


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


  Scenario: User sees shares names and space's names in Shares sidebar for each share respectively
    When user of browser opens file browser for "space1" space
    And user of browser creates "share_dir1" share of "dir1" directory
    And user of browser opens file browser for "space2" space
    And user of browser creates "share_dir2" share of "dir2" directory

    And user of browser clicks on Shares in the main menu
    Then user of browser sees share "share_dir1" from "space1" space
    And user of browser sees share "share_dir2" from "space2" space