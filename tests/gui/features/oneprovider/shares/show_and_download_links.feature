Feature: Operations on file links: download/show


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            users:
                - user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                      - dir2:
                        - file1: 11111

    And users opened [space_owner_browser, browser1] browsers' windows
    And user of space_owner_browser opened onezone page
    And user of space_owner_browser logged as space-owner-user to Onezone service


  Scenario: Without logging in, other user can open file download link from file in space owner's shared directory
    When using REST, user space-owner-user creates "share_dir1" share of "space1/dir1" supported by "oneprovider-1" provider
    And user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser opens "share_dir1" single share view of "dir1" using "Shared" tag
    And user of space_owner_browser goes to "/dir1/dir2" in shares file browser
    And user of space_owner_browser clicks on menu for "file1" file in shares file browser
    And user of space_owner_browser clicks "Copy download URL" option in data row menu in shares file browser
    And user of space_owner_browser sends copied URL to user named browser1

    And user of browser1 opens "shares download" URL received from user of space_owner_browser in browser's location bar
    Then user of browser1 sees that content of downloaded file "file1" is equal to: "11111"


  Scenario: Logged in user, can open download link copied from space owner's file details modal
    When user of space_owner_browser opens file browser for "space1" space

    And user of browser1 opens onezone page
    And user of browser1 log as user1 to Onezone service

    And user of space_owner_browser copies "Download" browser link of "dir1/dir2/file1" item to clipboard in "space1" space
    And user of space_owner_browser sends copied URL to user named browser1

    And user of browser1 opens "download" URL received from user of space_owner_browser in browser's location bar
    And user of browser1 sees that "file download" modal has appeared
    And user of browser1 clicks on "download" button in modal "file download"
    Then user of browser1 sees that content of downloaded file "file1" is equal to: "11111"
  

  Scenario: Logged in user, can open show link copied from space owner's file details modal and can see specific file selected
    When user of space_owner_browser opens file browser for "space1" space

    And user of browser1 opens onezone page
    And user of browser1 log as user1 to Onezone service

    And user of space_owner_browser copies "Show" browser link of "dir1/dir2/file1" item to clipboard in "space1" space
    And user of space_owner_browser sends copied URL to user named browser1

    And user of browser1 opens file browser for "space1" space
    And user of browser1 opens "show" URL received from user of space_owner_browser in browser's location bar
    Then user of browser1 sees that ["file1"] items are selected in file browser
    And user of browser1 sees that current working directory displayed in breadcrumbs on file browser is "space1/dir1/dir2"

