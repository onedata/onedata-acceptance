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


#  Scenario: Non-owner user sees hardlink created by file owner and can download it
#    When user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser
#    And user of browser1 opens file browser for "space1" space
#    Then user of browser1 sees only items named ["dir1", "file1", "file1(1)"] in file browser
#    And user of browser1 clicks on hardlink status tag for "file1" in file browser
#    And user of browser1 sees that "File details" modal has appeared
#    And user of browser1 sees that "File details" modal is opened on "Hard links" tab
#    And user of browser1 sees that there are 2 hardlinks in "File details" modal
#    And user of browser1 sees that path of "file1" hardlink is "space1/file1" in "File details" modal
#    And user of browser1 sees that path of "file1(1)" hardlink is "space1/file1(1)" in "File details" modal


#  Scenario: Non-owner user sees hardlink without read permission created by file owner and cannot download it
#    When user of space_owner_browser opens file browser for "space1" space
#    And user of space_owner_browser clicks on "Permissions" in context menu for "file1"
#    And user of space_owner_browser sees that "Directory details" modal is opened on "Permissions" tab
#    And user of space_owner_browser selects "POSIX" permission type in edit permissions panel
#    And user of space_owner_browser sets "622" permission code in edit permissions panel
#    And user of space_owner_browser clicks on "Save" button in edit permissions panel
#    And user of space_owner_browser clicks on "X" button in modal "Directory details"
#    And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser
#
#    And user of browser1 opens file browser for "space1" space
#    And user of browser1 clicks on menu for "file1" directory in file browser
#    And user of browser1 clicks "Download" option in data row menu in file browser
#    And browser1 is idle for 1 seconds
#    Then user of browser1 sees alert that file cannot be downloaded because of insufficient privileges


#  Scenario: User changes ACL privileges of file and sees that ACL privileges for hardlink has changed as well
#    When user of space_owner_browser opens file browser for "space1" space
#    And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser
#    And user of space_owner_browser clicks on "Permissions" in context menu for "file1"
#    And user of space_owner_browser selects "POSIX" permission type in edit permissions panel
#    And user of space_owner_browser sets "622" permission code in edit permissions panel
#    And user of space_owner_browser clicks on "Save" button in edit permissions panel
#    And user of space_owner_browser clicks on "X" button in modal "Directory details"
#
#    And user of space_owner_browser clicks on "Permissions" in context menu for "file1(1)"
#    Then user of space_owner_browser sees that current permission is "622"


#Scenario: Non-owner user creates metadata for a hardlink and owner user sees that
#  When user of space_owner_browser opens file browser for "space1" space
#  And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser
#
#  And user of browser1 opens file browser for "space1" space
#  And user of browser1 clicks on "Metadata" in context menu for "file1(1)"
#  And user of browser1 adds basic entry with key "attr1" and value "val1"
#  And user of browser1 clicks on "Save" button in metadata panel
#
#  And user of space_owner_browser clicks on "Metadata" in context menu for "file1"
#  Then user of space_owner_browser sees basic metadata entry with attribute named "attr1" and value "val1"


#Scenario: Non-owner user creates QoS for a hardlink and owner user sees that
#    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
#    And user of space_owner_browser clicks "user1" user in "space1" space members users list
#    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
#          QoS management:
#            granted: True
#  And user of space_owner_browser opens file browser for "space1" space
#  And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser
#
#  And user of browser1 opens file browser for "space1" space
#  And user of browser1 clicks on "Quality of Service" in context menu for "file1(1)"
#  And user of browser1 clicks on "Add Requirement" button in QoS panel
#  And user of browser1 clicks "enter as text" label in QoS panel
#  And user of browser1 writes "geo=PL" into expression text field in QoS panel
#  And user of browser1 confirms entering expression in expression text field in QoS panel
#  And user of browser1 clicks on "Save" button in QoS panel
#
#  And user of space_owner_browser clicks on "Quality of Service" in context menu for "file1(1)"
#  Then user of space_owner_browser sees [geo = "PL"] QoS requirement in QoS panel


#Scenario: Non-owner user creates hardlink for owner user file
#  When user of browser1 opens file browser for "space1" space
#  And user of browser1 creates hardlink of "file1" file in space "space1" in file browser


#Scenario: Non-owner user cannot delete hardlink without "write files" privilege
#    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
#    And user of space_owner_browser clicks "user1" user in "space1" space members users list
#    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
#          Data management:
#            granted: Partially
#            privilege subtypes:
#              Write files: False
#    And user of space_owner_browser opens file browser for "space1" space
#    And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser
#
#    And user of browser1 opens file browser for "space1" space
#    And user of browser1 clicks on "Delete" in context menu for "file1(1)"
#    And user of browser1 clicks on "Yes" button in modal "Delete modal"
#    And browser1 is idle for 1 seconds
#    Then user of browser1 sees alert that file cannot be deleted because of insufficient privileges


  Scenario: Non-owner user can delete hardlink with "write files" privilege
    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Data management:
            granted: Partially
            privilege subtypes:
              Write files: True
    And user of space_owner_browser opens file browser for "space1" space
    And user of space_owner_browser creates hardlink of "file1" file in space "space1" in file browser

    And user of browser1 opens file browser for "space1" space
    And user of browser1 clicks on "Delete" in context menu for "file1(1)"
    And user of browser1 clicks on "Yes" button in modal "Delete modal"
    Then user of browser1 does not see any item(s) named "file1(1)" in file browser
