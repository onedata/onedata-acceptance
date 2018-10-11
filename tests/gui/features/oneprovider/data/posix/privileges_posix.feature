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
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser


  Scenario: User sees that new file default permission code is 664
    
	# Create file
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks the button from top menu bar with tooltip "Create file"
    And user of browser sees that "New file" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "file2" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared
    
	# Check permission code
    And user of browser selects "file2" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    Then user of browser sees that current permission is "664"
    And user of browser clicks on input box in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared


  Scenario: User sees that new directory default permission code is 775

	# Create directory
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks the button from top menu bar with tooltip "Create directory"
    And user of browser sees that "New directory" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "dir2" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Check permission code
    And user of browser selects "dir2" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    Then user of browser sees that current permission is "775"
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared


  Scenario: User changes file permission (presses ENTER after entering new permission code)

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "775" permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Check permission code
    Then user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser sees that current permission is "775"
    And user of browser clicks on input box in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared


  Scenario: User changes file permission (clicks confirmation button after entering new permission code)

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "775" permission code in active modal
    And user of browser clicks "Ok" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared

	# Check permission code
    Then user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser sees that current permission is "775"
    And user of browser clicks "Ok" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared


  Scenario: User changes directory permission (presses ENTER after entering new permission code)

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "664" permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Check permission code
    Then user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser sees that current permission is "664"
    And user of browser clicks on input box in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared


  Scenario: User changes directory permission (clicks confirmation button after entering new permission code)

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "664" permission code in active modal
    And user of browser clicks "OK" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared

	# Check permission code
    Then user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser sees that current permission is "664"
    And user of browser clicks on input box in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared


  Scenario: User fails to download file because of lack in privileges

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "220" permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Fail to download file
    And user of browser double clicks on item named "file1" in file browser
    Then user of browser sees that "Cannot download file" modal has appeared
    And user of browser clicks "OK" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared


  Scenario: User fails to upload file because of lack in privileges

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "553" permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Fail to upload file
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser uses upload button in toolbar to upload file "20B-0.txt" to current dir
    Then user of browser sees an error notify with text matching to: .*failed.*


  Scenario: User fails to create file because of lack in privileges

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "553" permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Fail to create file
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Create file"
    And user of browser sees that "New file" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "file1" on keyboard
    And user of browser presses enter on keyboard
    Then user of browser sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser sees that the modal has disappeared


  Scenario: User fails to remove file because of lack in privileges

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser changes current working directory to space1 using breadcrumbs
    And user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "553" permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Fail to remove file
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser selects "file11" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Remove element"
    And user of browser sees that "Remove files" modal has appeared
    And user of browser clicks "Yes" confirmation button in displayed modal
    Then user of browser sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser sees that the modal has disappeared


  Scenario: User fails to rename file because of lack in privileges

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser changes current working directory to space1 using breadcrumbs
    And user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "553" permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Fail to rename file
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser selects "file11" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Rename element"
    And user of browser sees that "Rename file or directory" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "new_file11" on keyboard
    And user of browser presses enter on keyboard
    Then user of browser sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser sees that the modal has disappeared


  Scenario: User fails to remove directory because of lack in privileges

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser changes current working directory to space1 using breadcrumbs
    And user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "553" permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Fail to remove directory
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser selects "dir12" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Remove element"
    And user of browser sees that "Remove files" modal has appeared
    And user of browser clicks "Yes" confirmation button in displayed modal
    Then user of browser sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser sees that the modal has disappeared


  Scenario: User fails to remove directory containing file because of lack in privileges

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser changes current working directory to space1 using breadcrumbs
    And user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets "553" permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared

	# Fail to remove directory
    And user of browser selects "dir1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Remove element"
    And user of browser sees that "Remove files" modal has appeared
    And user of browser clicks "Yes" confirmation button in displayed modal
    Then user of browser sees an error notify with text matching to: .*[Aa]ccess denied.*
    And user of browser sees that the modal has disappeared


  Scenario: "Ok" confirmation button is disabled after entering incorrect permission code (3 char)

	# Change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets incorrect 3 char permission code in active modal
    And user of browser sees that "Ok" item displayed in modal is disabled
    And user of browser clicks "Cancel" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared


  Scenario: User fails to change permission code to incorrect one (2 char, presses enter after entering permission code)

	# Fail to change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets incorrect 2 char permission code in active modal
    And user of browser presses enter on keyboard
    And user of browser sees an error notify with text matching to: .*failed.*
    And user of browser clicks "Cancel" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared


  Scenario: User fails to change permission code to incorrect one (2 char, clicks confirmation button after entering permission code)

	# Fail to change permission code
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "file1" item(s) from file browser with pressed ctrl
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in active modal
    And user of browser clicks on input box in active modal
    And user of browser sets incorrect 2 char permission code in active modal
    And user of browser clicks "Ok" confirmation button in displayed modal
    And user of browser sees an error notify with text matching to: .*failed.*
    And user of browser clicks "Cancel" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared
