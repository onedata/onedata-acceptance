Feature: Symlinks functionalities using multiple providers and multiple browsers

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


  Scenario: User sees non-owned symlink and can download it
    When user of space_owner_browser creates symlink of "file1" file in space "space1" in file browser
    And user of browser1 opens file browser for "space1" space
    Then user of browser1 sees only items named ["dir1", "file1", "file1(1)"] in file browser
    And user of browser1 clicks on menu for "file1(1)" directory in file browser
    And user of browser1 clicks "Download" option in data row menu in file browser
    And user of browser1 sees that "file1(1)" has been downloaded


  Scenario: User creates symlink of non-owned file
    When user of browser1 opens file browser for "space1" space
    Then user of browser1 creates symlink of "file1" file in space "space1" in file browser
    And user of browser1 sees only items named ["dir1", "file1", "file1(1)"] in file browser


  Scenario: User creates symlink of non-owned file with POSIX permission 000
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser clicks on "Permissions" in context menu for "file1"
    And user of space_owner_browser sees that "Directory details" modal is opened on "Permissions" tab
    And user of space_owner_browser selects "POSIX" permission type in edit permissions panel
    And user of space_owner_browser sets "000" permission code in edit permissions panel
    And user of space_owner_browser clicks on "Save" button in edit permissions panel

    And user of browser1 opens file browser for "space1" space
    Then user of browser1 creates symlink of "file1" file in space "space1" in file browser
    And user of browser1 sees only items named ["dir1", "file1", "file1(1)"] in file browser


 Scenario: User cannot delete symlink without "Write files" privilege
    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Write files: False
    And user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates symlink of "file1" file in space "space1" in file browser

    And user of browser1 opens file browser for "space1" space
    Then user of browser1 clicks on "Delete" in context menu for "file1(1)"
    And user of browser1 clicks on "Yes" button in modal "Delete modal"
    And browser1 is idle for 1 seconds
    And user of browser1 sees alert that file cannot be deleted because of insufficient privileges


  Scenario: User can delete symlink with privilege "Write files"
    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Write files: True
    And user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates symlink of "file1" file in space "space1" in file browser

    And user of browser1 opens file browser for "space1" space
    Then user of browser1 clicks on "Delete" in context menu for "file1(1)"
    And user of browser1 clicks on "Yes" button in modal "Delete modal"
    And user of browser1 does not see any item(s) named "file1(1)" in file browser


  Scenario: User can access folder by non-owned symlink
    When user of space_owner_browser creates symlink of "dir1" file in space "space1" in file browser
    And user of browser1 opens file browser for "space1" space
    Then user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 sees only items named ["dir2", "file2"] in file browser
