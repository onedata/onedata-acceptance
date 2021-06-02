Feature: Hardlinks and symlinks functionalities using multiple providers and multiple browsers

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
                      - dir2
                      - file2: 11111
                  - file1: 11111

    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [onezone, onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service


  Scenario: Non-owner user sees hardlink created by file owner and can download it
    When user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser
    And user of browser1 opens file browser for "space1" space
    Then user of browser1 sees only items named ["dir1", "file1", "file1(1)"] in file browser
    And user of browser1 clicks on hardlink status tag for "file1" in file browser
    And user of browser1 sees that "File details" modal has appeared
    And user of browser1 sees that "File details" modal is opened on "Hard links" tab
    And user of browser1 sees that there are 2 hardlinks in "File details" modal
    And user of browser1 sees that path of "file1" hardlink is "/space1/file1" in "File details" modal
    And user of browser1 sees that path of "file1(1)" hardlink is "/space1/file1(1)" in "File details" modal



