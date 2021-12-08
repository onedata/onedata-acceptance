Feature: Oneprovider POSIX privileges GUI tests using multiple browsers

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
                  - file1
                  - dir1
          space2:
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
                  - dir1

    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [onezone, onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service


  Scenario: Space-owner-user changes file permission and user1 sees that it has changed
    When user of space_owner_browser sets file1 POSIX 775 privileges in "space1"

	# User1 checks permission code
    Then user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Files of "space1" in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks on menu for "file1" file in file browser
    And user of browser1 clicks "Permissions" option in data row menu in file browser
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in edit permissions modal
    And user of browser1 sees that current permission is "775"
    And user of browser1 clicks "Cancel" button in displayed modal


  Scenario: Space-owner-user changes directory permission and user1 sees that it has changed
    When user of space_owner_browser sets dir1 POSIX 664 privileges in "space1"

	# User1 checks permission code
    Then user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Files of "space1" in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks on menu for "dir1" file in file browser
    And user of browser1 clicks "Permissions" option in data row menu in file browser
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in edit permissions modal
    And user of browser1 sees that current permission is "664"
    And user of browser1 clicks "Cancel" button in displayed modal


  Scenario: User1 creates directory and fails to remove it because of change in parent directory permission

	# User1 creates dir
    When user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Files of "space2" in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 clicks "New directory" button from file browser menu bar
    And user of browser1 writes "dir2" into text field in modal "Create dir"
    And user of browser1 confirms create new directory using button

	# Space-owner-user changes permission code
    And user of space_owner_browser sets dir1 POSIX 753 privileges in "space2"

	# User1 fails to remove dir
    Then user of browser1 clicks on menu for "dir2" directory in file browser
    And user of browser1 clicks "Delete" option in data row menu in file browser
    And user of browser1 clicks on "Yes" button in modal "Delete modal"
    And user of browser1 sees that error modal with text "Deleting file(s) failed" appeared


  Scenario: User1 creates directory and fails to rename it because of change in parent directory permission

	# User1 creates dir
    When user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Files of "space2" in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 clicks "New directory" button from file browser menu bar
    And user of browser1 writes "dir2" into text field in modal "Create dir"
    And user of browser1 confirms create new directory using button

	# Space-owner-user changes permission code
    And user of space_owner_browser sets dir1 POSIX 753 privileges in "space2"

	# User1 fails to rename dir
    Then user of browser1 clicks on menu for "dir2" directory in file browser
    And user of browser1 clicks "Rename" option in data row menu in file browser
    And user of browser1 sees that "Rename" modal has appeared
    And user of browser1 writes "new_dir1" into text field in modal "Rename modal"
    And user of browser1 confirms rename directory using button
    And user of browser1 sees that error modal with text "Renaming the file failed" appeared


  Scenario: User1 creates directory and fails to create another directory because of change in parent directory permission

	# User1 creates dir
    When user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Files of "space2" in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 clicks "New directory" button from file browser menu bar
    And user of browser1 writes "dir2" into text field in modal "Create dir"
    And user of browser1 confirms create new directory using button

	# Space-owner-user changes permission code
    And user of space_owner_browser sets dir1 POSIX 753 privileges in "space2"

	# User1 fails to create dir
    Then user of browser1 clicks "New directory" button from file browser menu bar
    And user of browser1 writes "dir3" into text field in modal "Create dir"
    And user of browser1 confirms create new directory using button
    And user of browser1 sees that error modal with text "Creating directory failed" appeared


  Scenario: User1 fails to remove file because of change in parent directory permission

	# Space-owner-user uploads file
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space2" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks and presses enter on item named "dir1" in file browser
    And user of space_owner_browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of space_owner_browser changes current working directory to home using breadcrumbs

    # Space-owner-user changes permission code
    And user of space_owner_browser sets dir1 POSIX 753 privileges in "space2"

	# User1 fails to remove file
    And user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Files of "space2" in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    Then user of browser1 clicks on menu for "20B-0.txt" directory in file browser
    And user of browser1 clicks "Delete" option in data row menu in file browser
    And user of browser1 clicks on "Yes" button in modal "Delete modal"
    And user of browser1 sees that error modal with text "Deleting file(s) failed" appeared


  Scenario: User1 fails to rename file because of change in parent directory permission

	# Space-owner-user uploads file
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Files of "space2" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks and presses enter on item named "dir1" in file browser
    And user of space_owner_browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of space_owner_browser changes current working directory to home using breadcrumbs

	# Space-owner-user changes permission code
    And user of space_owner_browser sets dir1 POSIX 753 privileges in "space2"

	# User1 fails to rename file
    And user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Files of "space2" in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    Then user of browser1 clicks on menu for "20B-0.txt" directory in file browser
    And user of browser1 clicks "Rename" option in data row menu in file browser
    And user of browser1 sees that "Rename" modal has appeared
    And user of browser1 writes "new_file1" into text field in modal "Rename modal"
    And user of browser1 confirms rename directory using button
    And user of browser1 sees that error modal with text "Renaming the file failed" appeared


  Scenario: User1 fails to upload file because of change in parent directory permission

	# Space-owner-user changes permission code
    When user of space_owner_browser sets dir1 POSIX 753 privileges in "space2"

	# User1 fails to upload file
    And user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Files of "space2" in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    Then user of browser1 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir without waiting for upload to finish
    And user of browser1 sees that upload file failed
