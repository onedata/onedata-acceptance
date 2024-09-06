Feature: Basic shares operations in Onezone GUI featuring shares sidebar


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


  Scenario: User sees shares names and spaces names in Shares sidebar for each share respectively
    When user of browser opens file browser for "space1" space
    And user of browser creates "share_dir1" share of "dir1" directory
    And user of browser opens file browser for "space2" space
    And user of browser creates "share_dir2" share of "dir2" directory

    And user of browser clicks on Shares in the main menu
    Then user of browser sees share name "share_dir1" in the shares list in the sidebar
    And user of browser sees space name "space1" of "share_dir1" share in shares list in the sidebar
    And user of browser sees share name "share_dir2" in the shares list in the sidebar
    And user of browser sees space name "space2" of "share_dir2" share in shares list in the sidebar