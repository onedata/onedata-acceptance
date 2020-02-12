Feature: Oneprovider POSIX privileges GUI tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
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

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees that new updated file default permission code is 664
    When user of browser uploads "20B-0.txt" to the root directory of "space1"

	# Check permission code
    And user of browser clicks on menu for "20B-0.txt" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in edit permissions modal
    Then user of browser sees that current permission is "664"
    And user of browser clicks "Cancel" button in displayed modal


  Scenario: User sees that new directory default permission code is 775
    When user of browser succeeds to create directory "dir2" in "space1"

	# Check permission code
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in edit permissions modal
    Then user of browser sees that current permission is "775"
    And user of browser clicks "Cancel" button in displayed modal


  Scenario: User changes file permission

	# Change permission code
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in edit permissions modal
    And user of browser sets "775" permission code in edit permissions modal
    And user of browser clicks "Save" confirmation button in displayed modal

	# Check permission code
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in edit permissions modal
    And user of browser sees that current permission is "775"
    And user of browser clicks "Cancel" button in displayed modal


  Scenario: User changes directory permission

	# Change permission code
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in edit permissions modal
    And user of browser sets "664" permission code in edit permissions modal
    And user of browser clicks "Save" confirmation button in displayed modal

	# Check permission code
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in edit permissions modal
    And user of browser sees that current permission is "664"
    And user of browser clicks "Cancel" button in displayed modal


  Scenario: User fails to download file because of lack in privileges
    When user of browser sets file1 POSIX 220 privileges in "space1"

	# Fail to download file
    And user of browser double clicks on item named "file1" in file browser
    And user of browser sees that error modal with text "Starting file download failed" appeared


  Scenario: User fails to upload file because of lack in privileges
    When user of browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to upload file
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    Then user of browser sees that upload file failed


  Scenario: User fails to remove file because of lack in privileges
    When user of browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to remove file
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser clicks on menu for "file11" file in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"
    And user of browser sees that error modal with text "Deleting file(s) failed" appeared


  Scenario: User fails to rename file because of lack in privileges
    When user of browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to rename file
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser clicks on menu for "file11" file in file browser
    And user of browser clicks "Rename" option in data row menu in file browser
    And user of browser sees that "Rename" modal has appeared
    And user of browser writes "new_file11" into name directory text field in modal "Rename modal"
    And user of browser confirms rename directory using button
    And user of browser sees that error modal with text "Renaming the file failed" appeared


  Scenario: User fails to remove directory because of lack in privileges
    When user of browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to remove directory
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser clicks on menu for "dir12" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"
    And user of browser sees that error modal with text "Deleting file(s) failed" appeared


  Scenario: User fails to remove directory containing file because of lack in privileges
    When user of browser sets dir1 POSIX 553 privileges in "space1"

	# Fail to remove directory
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"
    And user of browser sees that error modal with text "Deleting file(s) failed" appeared


  Scenario: "Ok" confirmation button is disabled after entering incorrect permission code (3 char)

	# Change permission code
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in edit permissions modal
    And user of browser sets incorrect 3 char permission code in active modal
    Then user of browser sees that "Save" item displayed in modal is disabled
    And user of browser clicks "Cancel" button in displayed modal

