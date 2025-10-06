Feature: Operations on share file download links by user is not logged in


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
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
                      - dir2:
                        - file1: 1111

    And users opened [space_owner_browser, browser1] browsers' windows
    And user of space_owner_browser opened onezone page
    And user of space_owner_browser logged as space-owner-user to Onezone service


  Scenario: Without logging in, non space owner user can open file download link from file in shared directory
    When using REST, user space-owner-user creates "share_dir1" share of "space1/dir1" supported by "oneprovider-1" provider
    And user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser opens "share_dir1" single share view of "dir1" using "Shared" tag
    And user of space_owner_browser goes to "/dir1/dir2" in shares file browser
    And user of space_owner_browser clicks on menu for "file1" file in shares file browser
    And user of space_owner_browser clicks "Copy download URL" option in data row menu in shares file browser
    And user of space_owner_browser sends copied URL to user of browser1

    And user of browser1 opens URL received from user of space_owner_browser without waiting
    Then user of browser1 sees that content of downloaded file "file1" is equal to: "1111"
