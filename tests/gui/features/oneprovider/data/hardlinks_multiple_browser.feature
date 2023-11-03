Feature: Hardlinks functionalities using multiple providers and multiple browsers

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


  Scenario: User sees non-owned hardlink and can download it
    When user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser
    And user of browser1 opens file browser for "space1" space
    Then user of browser1 sees only items named ["dir1", "file1", "file1(1)"] in file browser
    And user of browser1 clicks on menu for "file1(1)" directory in file browser
    And user of browser1 clicks "Download" option in data row menu in file browser
    And user of browser1 sees that "file1(1)" has been downloaded


  Scenario: User sees non-owned hardlink without POSIX read permission and cannot download it
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser clicks on "Permissions" in context menu for "file1"
    And user of space_owner_browser sees that "Directory details" modal is opened on "Permissions" tab
    And user of space_owner_browser selects "POSIX" permission type in edit permissions panel
    And user of space_owner_browser sets "622" permission code in edit permissions panel
    And user of space_owner_browser clicks on "Save" button in edit permissions panel
    And user of space_owner_browser clicks on "X" button in modal "Directory details"
    And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser

    And user of browser1 opens file browser for "space1" space
    Then user of browser1 sees only items named ["dir1", "file1", "file1(1)"] in file browser
    And user of browser1 clicks on menu for "file1(1)" directory in file browser
    And user of browser1 clicks "Download" option in data row menu in file browser
    And browser1 is idle for 1 second
    And user of browser1 sees alert that file cannot be downloaded because of insufficient privileges


  Scenario: User can create hardlink of non-owned file with POSIX permission 000
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser clicks on "Permissions" in context menu for "file1"
    And user of space_owner_browser sees that "Directory details" modal is opened on "Permissions" tab
    And user of space_owner_browser selects "POSIX" permission type in edit permissions panel
    And user of space_owner_browser sets "000" permission code in edit permissions panel
    And user of space_owner_browser clicks on "Save" button in edit permissions panel

    And user of browser1 opens file browser for "space1" space
    Then user of browser1 creates hardlink of "file1" file in space "space1" in file browser
    And user of browser1 sees only items named ["dir1", "file1", "file1(1)"] in file browser


  Scenario: User can delete hardlink that is linked with the file inside a directory without the "Write" POSIX permission
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser clicks on "Permissions" in context menu for "dir1"
    And user of space_owner_browser sees that "Directory details" modal is opened on "Permissions" tab
    And user of space_owner_browser selects "POSIX" permission type in edit permissions panel
    And user of space_owner_browser sets "755" permission code in edit permissions panel
    And user of space_owner_browser clicks on "Save" button in edit permissions panel
    And user of space_owner_browser clicks and presses enter on item named "dir1" in file browser
    And user of space_owner_browser creates hard link of "file2" placed in "/.." directory on file browser

    And user of browser1 opens file browser for "space1" space
    Then user of browser1 clicks on "Delete" in context menu for "file2"
    And user of browser1 clicks on "Yes" button in modal "Delete modal"
    And user of browser1 does not see any item(s) named "file2" in file browser


  Scenario: User creates metadata for non-owned hardlink and owner user sees them on original file
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser

    And user of browser1 opens file browser for "space1" space
    And user of browser1 clicks on "Metadata" in context menu for "file1(1)"
    And user of browser1 adds basic entry with key "attr1" and value "val1"
    And user of browser1 clicks on "Save" button in metadata panel

    And user of space_owner_browser clicks on "Metadata" in context menu for "file1"
    Then user of space_owner_browser sees basic metadata entry with attribute named "attr1" and value "val1"


  Scenario: User creates QoS for non-owned hardlink and owner user sees them on original file
    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          QoS management:
            granted: True
    And user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser

    And user of browser1 opens file browser for "space1" space
    And user of browser1 clicks on "Quality of Service" in context menu for "file1(1)"
    And user of browser1 clicks on "Add Requirement" button in QoS panel
    And user of browser1 clicks "enter as text" label in QoS panel
    And user of browser1 writes "geo=PL" into expression text field in QoS panel
    And user of browser1 confirms entering expression in expression text field in QoS panel
    And user of browser1 clicks on "Save" button in QoS panel

    And user of space_owner_browser clicks on "Quality of Service" in context menu for "file1"
    Then user of space_owner_browser sees [geo = "PL"] QoS requirement in QoS panel


  Scenario: User changes ACL privileges of a file and sees that ACL privileges for a hardlink have changed as well
    When user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser
    And user of space_owner_browser sets "file1" ACL [allow, acl:read acl] privileges for user space-owner-user in "space1"
    And user of space_owner_browser clicks on "Permissions" in context menu for "file1(1)"
    And user of space_owner_browser selects "ACL" permission type in edit permissions panel
    Then user of space_owner_browser sees exactly 1 ACL record in edit permissions panel
    And user of space_owner_browser sees that first ACL record in edit permissions panel is set for user space-owner-user
    And user of space_owner_browser sees that only [allow, acl:read acl] privileges are set in first ACL record in edit permissions panel
