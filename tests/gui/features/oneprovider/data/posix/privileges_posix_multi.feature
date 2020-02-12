Feature: Oneprovider POSIX privileges GUI tests using multiple browsers

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
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
                  - file1
                  - dir1
          space2:
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

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario: User1 changes file permission and user2 sees that it has changed
    When user of browser1 sets file1 POSIX 775 privileges in "space1"

	# User2 checks permission code
    Then user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks Data of "space1" in the sidebar
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 clicks on menu for "file1" file in file browser
    And user of browser2 clicks "Permissions" option in data row menu in file browser
    And user of browser2 sees that "Edit permissions" modal has appeared
    And user of browser2 selects "POSIX" permission type in edit permissions modal
    And user of browser2 sees that current permission is "775"
    And user of browser2 clicks "Cancel" button in displayed modal


  Scenario: User1 changes directory permission and user2 sees that it has changed
    When user of browser1 sets dir1 POSIX 664 privileges in "space1"

	# User2 checks permission code
    Then user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks Data of "space1" in the sidebar
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 clicks on menu for "dir1" file in file browser
    And user of browser2 clicks "Permissions" option in data row menu in file browser
    And user of browser2 sees that "Edit permissions" modal has appeared
    And user of browser2 selects "POSIX" permission type in edit permissions modal
    And user of browser2 sees that current permission is "664"
    And user of browser2 clicks "Cancel" button in displayed modal


  Scenario: User2 creates directory and fails to remove it because of change in parent directory permission

	# User2 creates dir
    When user of browser2 clicks "space2" on the spaces list in the sidebar
    And user of browser2 clicks Data of "space2" in the sidebar
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 clicks "New directory" button from file browser menu bar
    And user of browser2 writes "dir2" into name directory text field in modal "Create dir"
    And user of browser2 confirms create new directory using button

	# User1 changes permission code
    And user of browser1 sets dir1 POSIX 753 privileges in "space2"

	# User2 fails to remove dir
    Then user of browser2 clicks on menu for "dir2" directory in file browser
    And user of browser2 clicks "Delete" option in data row menu in file browser
    And user of browser2 clicks on "Yes" button in modal "Delete modal"
    And user of browser2 sees that error modal with text "Deleting file(s) failed" appeared


  Scenario: User2 creates directory and fails to rename it because of change in parent directory permission

	# User2 creates dir
    When user of browser2 clicks "space2" on the spaces list in the sidebar
    And user of browser2 clicks Data of "space2" in the sidebar
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 clicks "New directory" button from file browser menu bar
    And user of browser2 writes "dir2" into name directory text field in modal "Create dir"
    And user of browser2 confirms create new directory using button

	# User1 changes permission code
    And user of browser1 sets dir1 POSIX 753 privileges in "space2"

	# User2 fails to rename dir
    Then user of browser2 clicks on menu for "dir2" directory in file browser
    And user of browser2 clicks "Rename" option in data row menu in file browser
    And user of browser2 sees that "Rename" modal has appeared
    And user of browser2 writes "new_dir1" into name directory text field in modal "Rename modal"
    And user of browser2 confirms rename directory using button
    And user of browser2 sees that error modal with text "Renaming the file failed" appeared


  Scenario: User2 creates directory and fails to create another directory because of change in parent directory permission

	# User2 creates dir
    When user of browser2 clicks "space2" on the spaces list in the sidebar
    And user of browser2 clicks Data of "space2" in the sidebar
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 clicks "New directory" button from file browser menu bar
    And user of browser2 writes "dir2" into name directory text field in modal "Create dir"
    And user of browser2 confirms create new directory using button

	# User1 changes permission code
    And user of browser1 sets dir1 POSIX 753 privileges in "space2"

	# User2 fails to create dir
    Then user of browser2 clicks "New directory" button from file browser menu bar
    And user of browser2 writes "dir3" into name directory text field in modal "Create dir"
    And user of browser2 confirms create new directory using button
    And user of browser2 sees that error modal with text "Creating directory failed" appeared


  Scenario: User2 fails to remove file because of change in parent directory permission

	# User1 uploads file
    When user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space2" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser1 changes current working directory to home using breadcrumbs

   # User1 changes permission code
    And user of browser1 sets dir1 POSIX 753 privileges in "space2"

	# User2 fails to remove file
    And user of browser2 clicks "space2" on the spaces list in the sidebar
    And user of browser2 clicks Data of "space2" in the sidebar
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    Then user of browser2 clicks on menu for "20B-0.txt" directory in file browser
    And user of browser2 clicks "Delete" option in data row menu in file browser
    And user of browser2 clicks on "Yes" button in modal "Delete modal"
    And user of browser2 sees that error modal with text "Deleting file(s) failed" appeared


  Scenario: User2 fails to rename file because of change in parent directory permission

	# User1 uploads file
    When user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Data of "space2" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser1 changes current working directory to home using breadcrumbs

	# User1 changes permission code
    And user of browser1 sets dir1 POSIX 753 privileges in "space2"

	# User2 fails to rename file
    And user of browser2 clicks "space2" on the spaces list in the sidebar
    And user of browser2 clicks Data of "space2" in the sidebar
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    Then user of browser2 clicks on menu for "20B-0.txt" directory in file browser
    And user of browser2 clicks "Rename" option in data row menu in file browser
    And user of browser2 sees that "Rename" modal has appeared
    And user of browser2 writes "new_file1" into name directory text field in modal "Rename modal"
    And user of browser2 confirms rename directory using button
    And user of browser2 sees that error modal with text "Renaming the file failed" appeared


  Scenario: User2 fails to upload file because of change in parent directory permission

	# User1 changes permission code
    When user of browser1 sets dir1 POSIX 753 privileges in "space2"

	# User2 fails to upload file
    And user of browser2 clicks "space2" on the spaces list in the sidebar
    And user of browser2 clicks Data of "space2" in the sidebar
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    Then user of browser2 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser2 sees that upload file failed
