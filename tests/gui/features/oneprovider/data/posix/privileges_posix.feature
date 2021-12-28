Feature: Oneprovider POSIX privileges GUI tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - space-owner-user
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
                      - file11
                      - dir12
                  - file1

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: User sees that default permission code for uploaded file is 644
    When user of space_owner_browser uploads "20B-0.txt" to the root directory of "space1"

	# Check permission code
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks on menu for "20B-0.txt" file in file browser
    And user of browser_user1 clicks "Permissions" option in data row menu in file browser
    And user of browser_user1 sees that "Edit permissions" modal has appeared
    And user of browser_user1 selects "POSIX" permission type in edit permissions modal
    Then user of browser_user1 sees that current permission is "664"
    And user of browser_user1 clicks "Cancel" button in displayed modal


  Scenario: User sees that new directory default permission code is 775
    When user of space_owner_browser succeeds to create directory "dir2" in "space1"

	# Check permission code
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks on menu for "dir2" directory in file browser
    And user of browser_user1 clicks "Permissions" option in data row menu in file browser
    And user of browser_user1 sees that "Edit permissions" modal has appeared
    And user of browser_user1 selects "POSIX" permission type in edit permissions modal
    Then user of browser_user1 sees that current permission is "775"
    And user of browser_user1 clicks "Cancel" button in displayed modal


  Scenario: User sees file permission changes made by space owner

	# Change permission code
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "file1" file in file browser
    And user of space_owner_browser clicks "Permissions" option in data row menu in file browser
    And user of space_owner_browser sees that "Edit permissions" modal has appeared
    And user of space_owner_browser selects "POSIX" permission type in edit permissions modal
    And user of space_owner_browser sets "775" permission code in edit permissions modal
    And user of space_owner_browser clicks "Save" confirmation button in displayed modal

	# Check permission code
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks on menu for "file1" file in file browser
    And user of browser_user1 clicks "Permissions" option in data row menu in file browser
    And user of browser_user1 sees that "Edit permissions" modal has appeared
    And user of browser_user1 selects "POSIX" permission type in edit permissions modal
    Then user of browser_user1 sees that current permission is "775"
    And user of browser_user1 clicks "Cancel" button in displayed modal


  Scenario: User sees directory permission changes made by space owner

	# Change permission code
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" directory in file browser
    And user of space_owner_browser clicks "Permissions" option in data row menu in file browser
    And user of space_owner_browser sees that "Edit permissions" modal has appeared
    And user of space_owner_browser selects "POSIX" permission type in edit permissions modal
    And user of space_owner_browser sets "664" permission code in edit permissions modal
    And user of space_owner_browser clicks "Save" confirmation button in displayed modal

	# Check permission code
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks on menu for "dir1" directory in file browser
    And user of browser_user1 clicks "Permissions" option in data row menu in file browser
    And user of browser_user1 sees that "Edit permissions" modal has appeared
    And user of browser_user1 selects "POSIX" permission type in edit permissions modal
    Then user of browser_user1 sees that current permission is "664"
    And user of browser_user1 clicks "Cancel" button in displayed modal


  Scenario: User fails to download file because of lack in privileges
    When user of space_owner_browser sets file1 POSIX 220 privileges in "space1"

	# Fail to download file
    And user of browser_user1 opens file browser for "space1" space
    Then user of browser_user1 clicks and presses enter on item named "file1" in file browser
    And user of browser_user1 sees that error modal with text "Starting file download failed" appeared


  Scenario: User fails to upload file because of lack in privileges
    When user of space_owner_browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to upload file
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks and presses enter on item named "dir1" in file browser
    And user of browser_user1 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir without waiting for upload to finish
    Then user of browser_user1 sees that upload file failed


  Scenario: User fails to remove file because of lack in privileges
    When user of space_owner_browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to remove file
    And user of browser_user1 opens file browser for "space1" space
    Then user of browser_user1 clicks and presses enter on item named "dir1" in file browser
    And user of browser_user1 clicks on menu for "file11" file in file browser
    And user of browser_user1 clicks "Delete" option in data row menu in file browser
    And user of browser_user1 clicks on "Yes" button in modal "Delete modal"
    And user of browser_user1 sees that error modal with text "Deleting file(s) failed" appeared


  Scenario: User fails to rename file because of lack in privileges
    When user of space_owner_browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to rename file
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks and presses enter on item named "dir1" in file browser
    And user of browser_user1 clicks on menu for "file11" file in file browser
    And user of browser_user1 clicks "Rename" option in data row menu in file browser
    And user of browser_user1 sees that "Rename" modal has appeared
    And user of browser_user1 writes "new_file11" into text field in modal "Rename modal"
    And user of browser_user1 confirms rename directory using button
    Then user of browser_user1 sees that error modal with text "Renaming the file failed" appeared


  Scenario: User fails to remove directory because of lack in privileges
    When user of space_owner_browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to remove directory
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks and presses enter on item named "dir1" in file browser
    And user of browser_user1 clicks on menu for "dir12" directory in file browser
    And user of browser_user1 clicks "Delete" option in data row menu in file browser
    And user of browser_user1 clicks on "Yes" button in modal "Delete modal"
    Then user of browser_user1 sees that error modal with text "Deleting file(s) failed" appeared


  Scenario: User fails to remove directory containing file because of lack in privileges
    When user of space_owner_browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to remove directory
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks on menu for "dir1" directory in file browser
    And user of browser_user1 clicks "Delete" option in data row menu in file browser
    And user of browser_user1 clicks on "Yes" button in modal "Delete modal"
    Then user of browser_user1 sees that error modal with text "Deleting file(s) failed" appeared


  Scenario Outline: Non-owner user sees "no access" tag after changing privileges
    When user of space_owner_browser sets <file_name> POSIX 333 privileges in "space1"
    And user of space_owner_browser does not see "no access" tag on <file_name>
    And user of browser_user1 opens file browser for "space1" space
    Then user of browser_user1 sees "no access" tag on <file_name>

    Examples:
      | file_name |
      | file1     |
      | dir1      |


  Scenario Outline: User fails to change <item_type> permissions because of lack in privileges (POSIX)
    When user of space_owner_browser sets <name_of_item> POSIX 553 privileges in "space1"

    # Fail to change file permissions
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks on menu for "<name_of_item>" <item_type> in file browser
    And user of browser_user1 clicks "Permissions" option in data row menu in file browser
    And user of browser_user1 sees that "Edit permissions" modal has appeared
    And user of browser_user1 selects "POSIX" permission type in edit permissions modal
    And user of browser_user1 sets "775" permission code in edit permissions modal
    And user of browser_user1 clicks "Save" confirmation button in displayed modal
    Then user of browser_user1 sees that error modal with text "Modifying permissions failed!" appeared

    Examples:
      | item_type | name_of_item |
      | file      | file1        |
      | directory | dir1         |
