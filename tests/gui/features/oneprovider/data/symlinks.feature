Feature: Basic files tab operations on symlinks in file browser


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
                - dir1:
                    - dir2
                    - file2: 11111
                - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User creates symbolic link of file in file browser and checks its presence
    When user of browser opens file browser for "space1" space
    And user of browser sees only items named ["dir1", "file1"] in file browser
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser
    And user of browser clicks file browser symlink button

    Then user of browser sees only items named ["dir1", "file1", "file1(1)"] in file browser
    And user of browser sees that item named "file1(1)" is symbolic link in file browser
    And user of browser sees that item named "file1(1)" is of 5 B size in file browser


  Scenario: Symbolic link details shows accurate information for newly created symlink
    When user of browser creates symlink of "file1" file in space "space1" in file browser
    And user of browser clicks on menu for "file1(1)" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser

    Then user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "file1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/file1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/file1" in "Symbolic link details" modal


  Scenario: User downloads symlink of file
    When user of browser creates symlink of "file1" file in space "space1" in file browser
    And user of browser double clicks on item named "file1(1)" in file browser
    And user of browser sees that content of downloaded file "file1" is equal to: "11111"


  Scenario: User creates symlink to symlink
    When user of browser creates symlink of "file1" file in space "space1" in file browser
    And user of browser creates symlink of "file1(1)" file in space "space1" in file browser
    Then user of browser sees only items named ["dir1", "file1", "file1(1)", "file1(1)(1)"] in file browser
    And user of browser sees that item named "file1(1)" is symbolic link in file browser
    And user of browser sees that item named "file1(1)(1)" is symbolic link in file browser

    # check first symlink information
    And user of browser clicks on menu for "file1(1)" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser

    Then user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "file1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/file1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/file1" in "Symbolic link details" modal
    And user of browser closes "Symbolic link details" modal

    # check second symlink information
    And user of browser clicks on menu for "file1(1)(1)" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser

    Then user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "file1(1)(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/file1(1)(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/file1(1)" in "Symbolic link details" modal


  Scenario: Newly created symlink to directory has right information and leads to original directory
    When user of browser creates symlink of "dir1" file in space "space1" in file browser
    Then user of browser sees only items named ["dir1", "file1", "dir1(1)"] in file browser
    And user of browser sees that item named "dir1(1)" is directory symbolic link in file browser
    And user of browser clicks on menu for "dir1(1)" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser

    And user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "dir1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/dir1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/dir1" in "Symbolic link details" modal
    And user of browser closes "Symbolic link details" modal

    And user of browser double clicks on item named "dir1(1)" in file browser
    Then user of browser sees only items named ["dir2", "file2"] in file browser
    And user of browser sees that current working directory displayed in breadcrumbs is /dir1


  Scenario: User creates symlinks in other directories than original files
    When user of browser opens file browser for "space1" space
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees only items named ["dir2", "file2"] in file browser

    # original file space1/dir1/file2
    And user of browser clicks on menu for "file2" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser

    # first symlink in space1/dir1/dir2
    And user of browser double clicks on item named "dir2" in file browser
    And user of browser clicks file browser symlink button
    Then user of browser sees only items named ["file2"] in file browser
    And user of browser sees that item named "file2" is symbolic link in file browser

    And user of browser clicks on menu for "file2" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "file2" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/dir1/dir2/file2" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/dir1/file2" in "Symbolic link details" modal
    And user of browser closes "Symbolic link details" modal

    # second symlink in space1
    And user of browser changes current working directory to home using breadcrumbs
    And user of browser clicks file browser symlink button
    And user of browser sees only items named ["dir1", "file1", "file2"] in file browser
    And user of browser sees that item named "file2" is symbolic link in file browser

    And user of browser clicks on menu for "file2" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "file2" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/file2" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/dir1/file2" in "Symbolic link details" modal


  Scenario: User creates symlink to hardlink
    When user of browser creates hardlink of "file1" file in space "space1" in file browser
    And user of browser creates symlink of "file1(1)" file in space "space1" in file browser
    And user of browser sees only items named ["dir1", "file1", "file1(1)", "file1(1)(1)"] in file browser

    And user of browser clicks on menu for "file1(1)(1)" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "file1(1)(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/file1(1)(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/file1(1)" in "Symbolic link details" modal


  Scenario: New symlink name is visible after symlink rename
    When user of browser creates symlink of "file1" file in space "space1" in file browser
    And user of browser succeeds to rename "file1(1)" to "symlink_file1" in "space1"
    Then user of browser sees only items named ["dir1", "file1", "symlink_file1"] in file browser

    And user of browser clicks on menu for "symlink_file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "symlink_file1" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/symlink_file1" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/file1" in "Symbolic link details" modal


  Scenario: Symlink is no longer visible after symlink removal
    When user of browser creates symlink of "file1" file in space "space1" in file browser

    # create another symlink
    And user of browser clicks file browser symlink button
    And user of browser sees only items named ["dir1", "file1", "file1(1)", "file1(2)"] in file browser
    And user of browser succeeds to remove "file1(1)" in "space1"

    Then user of browser sees only items named ["dir1", "file1", "file1(2)"] in file browser


  Scenario: File symlink is malformed after renaming target file
    When user of browser creates symlink of "file1" file in space "space1" in file browser
    And user of browser succeeds to rename "file1" to "target_file1" in "space1"
    And user of browser sees only items named ["dir1", "target_file1", "file1(1)"] in file browser
    Then user of browser sees that item named "file1(1)" is malformed symbolic link in file browser

    And user of browser clicks on menu for "file1(1)" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "file1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/file1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/file1" in "Symbolic link details" modal


  Scenario: Directory symlink is malformed after renaming target directory
    When user of browser creates symlink of "dir1" file in space "space1" in file browser
    And user of browser succeeds to rename "dir1" to "target_dir1" in "space1"
    And user of browser sees only items named ["file1", "target_dir1", "dir1(1)"] in file browser
    Then user of browser sees that item named "dir1(1)" is malformed symbolic link in file browser

    And user of browser clicks on menu for "dir1(1)" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "dir1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/dir1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/dir1" in "Symbolic link details" modal


  Scenario: File symlink is malformed after removing target file
    When user of browser creates symlink of "file1" file in space "space1" in file browser
    And user of browser succeeds to remove "file1" in "space1"
    And user of browser sees only items named ["dir1", "file1(1)"] in file browser
    Then user of browser sees that item named "file1(1)" is malformed symbolic link in file browser

    And user of browser clicks on menu for "file1(1)" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "file1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/file1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/file1" in "Symbolic link details" modal


  Scenario: Directory symlink is malformed after removing target directory
    When user of browser creates symlink of "dir1" file in space "space1" in file browser
    And user of browser succeeds to remove "dir1" in "space1"
    And user of browser sees only items named ["file1", "dir1(1)"] in file browser
    Then user of browser sees that item named "dir1(1)" is malformed symbolic link in file browser

    And user of browser clicks on menu for "dir1(1)" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Symbolic link details" modal has appeared
    And user of browser sees that symbolic link name is "dir1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link location is "/space1/dir1(1)" in "Symbolic link details" modal
    And user of browser sees that symbolic link target path is "/space1/dir1" in "Symbolic link details" modal

