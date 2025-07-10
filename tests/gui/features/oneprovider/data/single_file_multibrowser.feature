Feature: Basic files tab operations on single file in multibrowser

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              users:
                  - user2
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
              storage:
                defaults:
                  provider: oneprovider-1
                directory tree:
                  - dir1
                  - file1: 11111

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario: User can see other user's full name as a file owner in file details
    When user of browser1 expands account settings dropdown in the sidebar
    And user of browser1 clicks on Manage account item in expanded settings dropdown in the sidebar
    And user of browser1 activates edit box by clicking on the user full name in Profile page
    And user of browser1 types "John Smith" to user full name edit box in Profile page
    And user of browser1 clicks on confirm button displayed next to user full name edit box in Profile page
    And user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks "Files" of "space1" space in the sidebar
    And user of browser2 sees file browser in files tab in Oneprovider page
    And user of browser2 clicks on "Information" in context menu for "file1"
    And user of browser2 sees that "File details" modal is opened on "Info" tab
    Then user of browser2 can see that file owner is "John Smith (user1)" in file details

