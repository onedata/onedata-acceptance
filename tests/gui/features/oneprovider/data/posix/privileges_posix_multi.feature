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
    And opened oneprovider-1 Oneprovider view in web GUI by users of [browser1, browser2]


  Scenario: User1 changes file permission and user2 sees that it has changed

	# User1 changes permission code
    When user of browser1 uses spaces select to change data space to "space1"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 selects "file1" item(s) from file browser with pressed ctrl
    And user of browser1 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in active modal
    And user of browser1 clicks on input box in active modal
    And user of browser1 sets "775" permission code in active modal
    And user of browser1 presses enter on keyboard
    And user of browser1 sees that the modal has disappeared
    
	# User2 checks permission code
    Then user of browser2 uses spaces select to change data space to "space1"             
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 selects "file1" item(s) from file browser with pressed ctrl
    And user of browser2 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser2 sees that "Edit permissions" modal has appeared
    And user of browser2 selects "POSIX" permission type in active modal
    And user of browser2 clicks on input box in active modal
    And user of browser2 sees that current permission is "775"
    And user of browser2 clicks "Cancel" confirmation button in displayed modal
    And user of browser2 sees that the modal has disappeared


  Scenario: User1 changes directory permission and user2 sees that it has changed

	# User1 changes permission code
    When user of browser1 uses spaces select to change data space to "space1"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser1 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in active modal
    And user of browser1 clicks on input box in active modal
    And user of browser1 sets "664" permission code in active modal
    And user of browser1 presses enter on keyboard
    And user of browser1 sees that the modal has disappeared

	# User2 checks permission code
    Then user of browser2 uses spaces select to change data space to "space1"
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser2 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser2 sees that "Edit permissions" modal has appeared
    And user of browser2 selects "POSIX" permission type in active modal
    And user of browser2 clicks on input box in active modal
    And user of browser2 sees that current permission is "664"
    And user of browser2 clicks "Cancel" confirmation button in displayed modal
    And user of browser2 sees that the modal has disappeared


  Scenario: User2 creates directory and fails to remove it because of change in parent directory permission

	# User2 creates dir
    When user of browser2 uses spaces select to change data space to "space2"
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 clicks the button from top menu bar with tooltip "Create directory"
    And user of browser2 sees that "New directory" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "dir2" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees that the modal has disappeared

	# User1 changes permission code
    And user of browser1 uses spaces select to change data space to "space2"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 changes current working directory to space2 using breadcrumbs
    And user of browser1 selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser1 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in active modal
    And user of browser1 clicks on input box in active modal
    And user of browser1 sets "753" permission code in active modal
    And user of browser1 clicks "Ok" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

	# User2 fails to remove dir
    Then user of browser2 selects "dir2" item(s) from file browser with pressed ctrl
    And user of browser2 clicks the button from top menu bar with tooltip "Remove element"
    And user of browser2 sees that "Remove files" modal has appeared
    And user of browser2 clicks "Yes" confirmation button in displayed modal
    And user of browser2 sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser2 sees that the modal has disappeared


  Scenario: User2 creates directory and fails to rename it because of change in parent directory permission

	# User2 creates dir
    When user of browser2 uses spaces select to change data space to "space2"
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 clicks the button from top menu bar with tooltip "Create directory"
    And user of browser2 sees that "New directory" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "dir2" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees that the modal has disappeared

	# User1 changes permission code
    And user of browser1 uses spaces select to change data space to "space2"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 changes current working directory to space2 using breadcrumbs
    And user of browser1 selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser1 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in active modal
    And user of browser1 clicks on input box in active modal
    And user of browser1 sets "753" permission code in active modal
    And user of browser1 clicks "Ok" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

	# User2 fails to rename dir
    Then user of browser2 selects "dir2" item(s) from file browser with pressed ctrl
    And user of browser2 clicks the button from top menu bar with tooltip "Rename element"
    And user of browser2 sees that "Rename file or directory" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "new_dir1" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser2 sees that the modal has disappeared


  Scenario: User2 creates directory and fails to create another directory because of change in parent directory permission

	# User2 creates dir
    When user of browser2 uses spaces select to change data space to "space2"
    And user of browser2 refreshes site
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 clicks the button from top menu bar with tooltip "Create directory"
    And user of browser2 sees that "New directory" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "dir2" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees that the modal has disappeared

	# User1 changes permission code
    And user of browser1 uses spaces select to change data space to "space2"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 changes current working directory to space2 using breadcrumbs
    And user of browser1 selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser1 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in active modal
    And user of browser1 clicks on input box in active modal
    And user of browser1 sets "753" permission code in active modal
    And user of browser1 clicks "Ok" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

	# User2 fails to create dir
    Then user of browser2 clicks the button from top menu bar with tooltip "Create directory"
    And user of browser2 sees that "New directory" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "dir3" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser2 sees that the modal has disappeared


  Scenario: User2 creates file and fails to remove it because of change in parent directory permission

	# User2 creates file
    When user of browser2 uses spaces select to change data space to "space2"
    And user of browser2 refreshes site
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 clicks the button from top menu bar with tooltip "Create file"
    And user of browser2 sees that "New file" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "file1" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees that the modal has disappeared

	# User1 changes permission code
    And user of browser1 uses spaces select to change data space to "space2"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 changes current working directory to space2 using breadcrumbs
    And user of browser1 selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser1 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in active modal
    And user of browser1 clicks on input box in active modal
    And user of browser1 sets "753" permission code in active modal
    And user of browser1 clicks "Ok" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

	# User2 fails to remove file
    Then user of browser2 selects "file1" item(s) from file browser with pressed ctrl
    And user of browser2 clicks the button from top menu bar with tooltip "Remove element"
    And user of browser2 sees that "Remove files" modal has appeared
    And user of browser2 clicks "Yes" confirmation button in displayed modal
    And user of browser2 sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser2 sees that the modal has disappeared


  Scenario: User2 creates file and fails to rename it because of change in parent directory permission

	# User2 creates file
    When user of browser2 uses spaces select to change data space to "space2"
    And user of browser2 refreshes site
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 clicks the button from top menu bar with tooltip "Create file"
    And user of browser2 sees that "New file" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "file1" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees that the modal has disappeared

	# User1 changes permission code
    And user of browser1 uses spaces select to change data space to "space2"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 changes current working directory to space2 using breadcrumbs
    And user of browser1 selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser1 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in active modal
    And user of browser1 clicks on input box in active modal
    And user of browser1 sets "753" permission code in active modal
    And user of browser1 clicks "Ok" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

	# User2 fails to rename file
    Then user of browser2 selects "file1" item(s) from file browser with pressed ctrl
    And user of browser2 clicks the button from top menu bar with tooltip "Rename element"
    And user of browser2 sees that "Rename file or directory" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "new_file1" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser2 sees that the modal has disappeared


  Scenario: User2 creates file and fails to create another file because of change in parent directory permission

	# User2 creates file
    When user of browser2 uses spaces select to change data space to "space2"
    And user of browser2 refreshes site
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 clicks the button from top menu bar with tooltip "Create file"
    And user of browser2 sees that "New file" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "file1" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees that the modal has disappeared

	# User1 changes permission code
    And user of browser1 uses spaces select to change data space to "space2"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 changes current working directory to space2 using breadcrumbs
    And user of browser1 selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser1 clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser1 sees that "Edit permissions" modal has appeared
    And user of browser1 selects "POSIX" permission type in active modal
    And user of browser1 clicks on input box in active modal
    And user of browser1 sets "753" permission code in active modal
    And user of browser1 clicks "Ok" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

	# User2 fails to create file
    Then user of browser2 clicks the button from top menu bar with tooltip "Create file"
    And user of browser2 sees that "New file" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types "file2" on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser2 sees that the modal has disappeared
