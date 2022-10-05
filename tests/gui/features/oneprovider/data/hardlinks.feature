Feature: Basic files tab operations on hardlinks in file browser


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: space-owner-user
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
                    - dir2
                    - file2: 11111
                - file1: 11111
            groups:
                - group1

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User creates hardlink of file in the same directory in file browser and checks its presence
    When user of browser opens file browser for "space1" space
    And user of browser sees only items named ["dir1", "file1"] in file browser
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar

    Then user of browser sees only items named ["dir1", "file1", "file1(1)"] in file browser
    And user of browser sees hardlink status tag with "2 hard links" text for "file1" in file browser
    And user of browser sees hardlink status tag with "2 hard links" text for "file1(1)" in file browser
    And user of browser sees that item named "file1(1)" is of 5 B size in file browser


  Scenario: Hardlink tag opens File details modal with hardlinks information
    When user of browser creates hardlink of "file1" file in space "space1" in file browser
    And user of browser sees only items named ["dir1", "file1", "file1(1)"] in file browser
    And user of browser clicks on hardlink status tag for "file1" in file browser
    Then user of browser sees that "File details" modal has appeared
    And user of browser sees that "File details" modal is opened on "Hard links" tab
    And user of browser sees that there are 2 hardlinks in "File details" modal
    And user of browser sees that path of "file1" hardlink is "space1/file1" in "File details" modal
    And user of browser sees that path of "file1(1)" hardlink is "space1/file1(1)" in "File details" modal


  Scenario: User downloads hardlink of file
    When user of browser creates hardlink of "file1" file in space "space1" in file browser
    And user of browser clicks and presses enter on item named "file1(1)" in file browser
    Then user of browser sees that content of downloaded file "file1(1)" is equal to: "11111"


  Scenario: User creates hardlink of hardlink
    When user of browser creates hardlink of "file1" file in space "space1" in file browser
    And user of browser creates hardlink of "file1(1)" file in space "space1" in file browser
    Then user of browser sees only items named ["dir1", "file1", "file1(1)", "file1(1)(1)"] in file browser
    And user of browser sees hardlink status tag with "3 hard links" text for "file1" in file browser
    And user of browser sees hardlink status tag with "3 hard links" text for "file1(1)" in file browser
    And user of browser sees hardlink status tag with "3 hard links" text for "file1(1)(1)" in file browser
    And user of browser clicks on hardlink status tag for "file1" in file browser

    And user of browser sees that "File details" modal has appeared
    And user of browser sees that "File details" modal is opened on "Hard links" tab
    And user of browser sees that there are 3 hardlinks in "File details" modal
    And user of browser sees that path of "file1" hardlink is "space1/file1" in "File details" modal
    And user of browser sees that path of "file1(1)" hardlink is "space1/file1(1)" in "File details" modal
    And user of browser sees that path of "file1(1)(1)" hardlink is "space1/file1(1)(1)" in "File details" modal


  Scenario: User creates hardlinks in other directories than original files
    When user of browser opens file browser for "space1" space
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser sees only items named ["dir2", "file2"] in file browser

    # original file space1/dir1/file2
    And user of browser clicks on menu for "file2" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser

    # first hardlink in space1/dir1/dir2
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar
    Then user of browser sees only items named ["file2"] in file browser
    And user of browser sees hardlink status tag with "2 hard links" text for "file2" in file browser

    # second hardlink in space1
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser clicks "Place hard link" button from file browser menu bar
    And user of browser sees only items named ["dir1", "file1", "file2"] in file browser
    And user of browser sees hardlink status tag with "3 hard links" text for "file2" in file browser

    And user of browser clicks on hardlink status tag for "file2" in file browser
    And user of browser sees that "File details" modal has appeared
    And user of browser sees that "File details" modal is opened on "Hard links" tab
    And user of browser sees that there are 3 hardlinks in "File details" modal
    And user of browser sees paths ["space1/dir1/file2", "space1/file2", "space1/dir1/dir2/file2"] of hardlinks in "File details" modal


  Scenario: New hardlink name is visible after hardlink rename
    When user of browser creates hardlink of "file1" file in space "space1" in file browser
    And user of browser succeeds to rename "file1(1)" to "hardlink_file1" in "space1"
    Then user of browser sees only items named ["dir1", "file1", "hardlink_file1"] in file browser
    And user of browser sees hardlink status tag with "2 hard links" text for "hardlink_file1" in file browser

    And user of browser clicks on hardlink status tag for "hardlink_file1" in file browser
    And user of browser sees that "File details" modal has appeared
    And user of browser sees that "File details" modal is opened on "Hard links" tab
    And user of browser sees that there are 2 hardlinks in "File details" modal
    And user of browser sees that path of "file1" hardlink is "space1/file1" in "File details" modal
    And user of browser sees that path of "hardlink_file1" hardlink is "space1/hardlink_file1" in "File details" modal


  Scenario: Hardlink info is no longer visible after hardlink removal
    When user of browser creates hardlink of "file1" file in space "space1" in file browser

    # create another hardlink
    And user of browser clicks "Place hard link" button from file browser menu bar
    And user of browser sees only items named ["dir1", "file1", "file1(1)", "file1(2)"] in file browser
    And user of browser sees hardlink status tag with "3 hard links" text for "file1" in file browser
    And user of browser succeeds to remove "file1(1)" in "space1"

    Then user of browser sees only items named ["dir1", "file1", "file1(2)"] in file browser
    And user of browser sees hardlink status tag with "2 hard links" text for "file1" in file browser
    And user of browser clicks on hardlink status tag for "file1" in file browser
    And user of browser sees that "File details" modal has appeared
    And user of browser sees that "File details" modal is opened on "Hard links" tab
    And user of browser sees that there are 2 hardlinks in "File details" modal
    And user of browser sees that path of "file1" hardlink is "space1/file1" in "File details" modal
    And user of browser sees that path of "file1(2)" hardlink is "space1/file1(2)" in "File details" modal


# TODO: VFS-9799 reimplement gui QoS tests after move to file info modal
  # Scenario: Newly created hardlink inherits metadata and QoS from original file
  #   When user of browser opens file browser for "space1" space
  #   And user of browser sees only items named ["dir1", "file1"] in file browser
  #   And user of browser adds and saves '{"id": 1}' JSON metadata for "file1"
  #   And user of browser creates "hello=WORLD" QoS requirement for "file1" in space "space1"
  #   And user of browser sees QoS status tag for "file1" in file browser
  #   And user of browser sees Metadata status tag for "file1" in file browser

  #   # create hardlink of file with status tags
  #   And user of browser creates hardlink of "file1" file in space "space1" in file browser
  #   And user of browser sees only items named ["dir1", "file1", "file1(1)"] in file browser
  #   Then user of browser sees QoS status tag for "file1(1)" in file browser
  #   And user of browser sees metadata status tag for "file1(1)" in file browser

  #   # check QoS of hardlink
  #   And user of browser clicks on QoS status tag for "file1(1)" in file browser
  #   And user of browser sees [hello = "WORLD"] QoS requirement in modal "Quality of Service"
  #   And user of browser clicks on "Close" button in modal "Quality of Service"

  #   # check metadata of hardlink
  #   And user of browser opens metadata panel on JSON tab for "file1(1)"
  #   And user of browser sees that JSON textarea in metadata panel contains '{"id": 1}'


# TODO: VFS-9799 reimplement gui QoS tests after move to file info modal
  # Scenario: New metadata and QoS are inherited by all hardlinks after file browser refresh
  #   When user of browser creates hardlink of "file1" file in space "space1" in file browser

  #   # add another hardlink
  #   And user of browser clicks "Place hard link" button from file browser menu bar
  #   And user of browser sees only items named ["dir1", "file1", "file1(1)", "file1(2)"] in file browser
  #   And user of browser adds and saves '{"id": 1}' JSON metadata for "file1(1)"
  #   And user of browser creates "hello=WORLD" QoS requirement for "file1(1)" in space "space1"

  #   And user of browser clicks "Refresh" button from file browser menu bar
  #   Then user of browser sees QoS status tag for "file1" in file browser
  #   And user of browser sees QoS status tag for "file1(1)" in file browser
  #   And user of browser sees QoS status tag for "file1(2)" in file browser
  #   And user of browser sees Metadata status tag for "file1" in file browser
  #   And user of browser sees Metadata status tag for "file1(1)" in file browser
  #   And user of browser sees Metadata status tag for "file1(2)" in file browser

  #   # check QoS of original file
  #   And user of browser clicks on QoS status tag for "file1" in file browser
  #   And user of browser sees [hello = "WORLD"] QoS requirement in modal "Quality of Service"
  #   And user of browser clicks on "Close" button in modal "Quality of Service"

  #   # check QoS of second hardlink
  #   And user of browser clicks on QoS status tag for "file1(2)" in file browser
  #   And user of browser sees [hello = "WORLD"] QoS requirement in modal "Quality of Service"
  #   And user of browser clicks on "Close" button in modal "Quality of Service"

  #   # check metadata of original file
  #   And user of browser opens metadata panel on JSON tab for "file1"
  #   And user of browser sees that JSON textarea in metadata panel contains '{"id": 1}'
  #   And user of browser clicks on "Close" button in modal "Metadata"

  #   # check metadata of second hardlink
  #   And user of browser opens metadata panel on JSON tab for "file1(2)"
  #   And user of browser sees that JSON textarea in metadata panel contains '{"id": 1}'


  Scenario: User sees change of hardlink posix permission after second hardlink permissions change
    # create hardlink
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar

    # change POSIX permission of created hardlink
    And user of browser clicks on "Permissions" in context menu for "file1"
    And user of browser sees that "File details" modal is opened on "Permissions" tab
    And user of browser selects "POSIX" permission type in edit permissions panel
    And user of browser sets "775" permission code in edit permissions panel
    And user of browser clicks on "Save" button in edit permissions panel
    And user of browser clicks on "X" button in modal "File details"

    # check permission of original file
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    Then user of browser sees that current permission is "775"


  Scenario: User sees change of hardlink ACL permission after first hardlink permissions change
    # create hardlink
    When user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Create hard link" option in data row menu in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks "Place hard link" button from file browser menu bar

    # change ACL permission of created hardlink
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser clicks on "Permissions" in context menu for "file1"
    And user of browser sees that "File details" modal is opened on "Permissions" tab
    And user of browser selects "ACL" permission type in edit permissions panel

    And user of browser adds ACE with "attributes:read attributes" privilege set for group group1
    And user of browser adds ACE with [general:delete, acl:read acl] privileges set for user space-owner-user
    And user of browser clicks on "Save" button in edit permissions panel
    And user of browser clicks on "X" button in modal "File details"

     # check permission of original file
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks on "Permissions" in context menu for "file1"
    And user of browser sees that "File details" modal is opened on "Permissions" tab
    And user of browser selects "ACL" permission type in edit permissions panel
    Then user of browser sees exactly 2 ACL records in edit permissions panel
