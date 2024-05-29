Feature: Test user has access to space via group membership


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: space-owner-user
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
    And directory tree structure on local file system:
          space_owner_browser:
              dir1:
                file1.txt:
                  content: 11111

    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service


  Scenario: User has access to space via group membership
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Files" of "space1" space in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser uses upload button from file browser menu bar to upload files from local directory "dir1" to remote current dir without waiting for upload to finish
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "space1" space members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal
    And user of space_owner_browser sends copied token to user of browser1

    And user of browser1 adds group "group1" to space using copied token
    Then user of browser1 sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser1 clicks "Files" of "space1" space in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks on menu for "file1.txt" file in file browser
    And user of browser1 clicks "Download" option in data row menu in file browser
    And user of browser1 sees that "file1.txt" has been downloaded


  Scenario: User fails to join to the space because the space was deleted
    When user of space_owner_browser copies invite token to "space1" space
    And user of space_owner_browser sends copied token to user of browser1
    And user of space_owner_browser removes "space1" spaces in Onezone page

    Then user of browser1 tries to join space using received token
    And user of browser1 sees error modal with info about invalid target with id of "space1" space
