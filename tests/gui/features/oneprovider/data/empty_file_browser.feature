Feature: Data tab operations with empty file browser


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

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


#  TODO: change test because of a new gui
#  Scenario: User creates new file (presses ENTER after entering file name)
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees file browser in data tab in Oneprovider page
#    And user of browser sees that current working directory displayed in breadcrumbs is space1
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file1" on keyboard
#    And user of browser presses enter on keyboard
#    And user of browser sees that the modal has disappeared
#    Then user of browser sees that item named "file1" has appeared in file browser
#    And user of browser sees that item named "file1" is file in file browser
#
#
#  Scenario: User creates new file (clicks CREATE confirmation button after entering file name)
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees file browser in data tab in Oneprovider page
#    And user of browser sees that current working directory displayed in breadcrumbs is space1
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file1" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    Then user of browser sees that item named "file1" has appeared in file browser
#    And user of browser sees that item named "file1" is file in file browser


  Scenario: User creates new directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1
    And user of browser clicks "New directory" button from file browser menu bar
    And user of browser writes "dir1" into name directory text field in modal "Create dir"
    And user of browser confirms create new directory using button
    Then user of browser sees that item named "dir1" has appeared in file browser
    And user of browser sees that item named "dir1" is directory in file browser


  Scenario: User uploads a small file to space that accepts large files
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    Then user of browser sees that item named "20B-0.txt" has appeared in file browser


  Scenario: User sees empty directory message in directory without items
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees empty file browser in data tab in Oneprovider page
    Then user of browser sees empty directory message in file browser


#  TODO: change test because of a new gui
#  Scenario: User creates files and sees that they are ordered on list by creation order
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees that current working directory displayed in breadcrumbs is space1
#    And user of browser sees file browser in data tab in Oneprovider page
#
#    # create file1
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file1" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file1" has appeared in file browser
#
#    # create file2
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file2" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file2" has appeared in file browser
#
#    # create file3
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file3" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file3" has appeared in file browser
#
#    # create file4
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file4" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file4" has appeared in file browser
#
#    # create file5
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file5" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file5" has appeared in file browser
#
#    And user of browser sees items named ["file5", "file4", "file3", "file2", "file1"] in file browser in given order
#    And user of browser refreshes site
#    And user of browser sees nonempty file browser in data tab in Oneprovider page
#    Then user of browser sees items named ["file1", "file2", "file3", "file4", "file5"] in file browser in given order
#
#
#  Scenario: User upload files and sees they are ordered on list by upload order (uploads one file at time)
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees that current working directory displayed in breadcrumbs is space1
#    And user of browser sees file browser in data tab in Oneprovider page
#
#    # create file1
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file1" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file1" has appeared in file browser
#
#    # create file2
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file2" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file2" has appeared in file browser
#
#    # create file3
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file3" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file3" has appeared in file browser
#
#    And user of browser uses upload button in toolbar to upload file "20B-0.txt" to current dir
#    And user of browser uses upload button in toolbar to upload file "20B-1.txt" to current dir
#
#    And user of browser sees items named ["20B-1.txt", "file3", "file2", "file1"] in file browser in given order
#    And user of browser sees items named ["20B-0.txt", "file3", "file2", "file1"] in file browser in given order
#    And user of browser refreshes site
#    And user of browser sees nonempty file browser in data tab in Oneprovider page
#    Then user of browser sees items named ["20B-0.txt", "20B-1.txt", "file1", "file2", "file3"] in file browser in given order


  Scenario: User sees modification date after uploading file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser sees that item named "20B-0.txt" has appeared in file browser
    Then user of browser sees that modification date of item named "20B-0.txt" is not earlier than 120 seconds ago in file browser


#  TODO: change test because of a new gui
#  Scenario: User sees modification date after creating file
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees that current working directory displayed in breadcrumbs is space1
#    And user of browser sees file browser in data tab in Oneprovider page
#
#    # create file1
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file1" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file1" has appeared in file browser
#    Then user of browser sees that modification date of item named "file1" is not earlier than 120 seconds ago in file browser


  Scenario: User sees file size after upload and after site refresh
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    # upload file
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    Then user of browser sees that item named "20B-0.txt" is of 20 B size in file browser
    And user of browser refreshes site
    And user of browser sees nonempty file browser in data tab in Oneprovider page
    And user of browser sees that item named "20B-0.txt" is of 20 B size in file browser


#  TODO: change test because of a new gui
#  Scenario: User uploads file and checks if provider name is displayed in the data distribution panel
#    When user of browser clicks "space1" on the spaces list in the sidebar
#    And user of browser clicks Data of "space1" in the sidebar
#    And user of browser sees file browser in data tab in Oneprovider page
#
#    # upload file
#    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
#    And user of browser sees that item named "20B-0.txt" has appeared in file browser
#
#    And user of browser selects "20B-0.txt" item from file browser with pressed ctrl
#
#    And user of browser clicks on menu for "20B-0.txt" file in file browser
#    And user of browser clicks "Data distribution" option in data row menu in file browser
#
#    And user of browser sees that "Data distribution" modal has appeared
#    Then user of browser sees that chunk bar for provider "oneprovider-1" is entirely filled
#    And user of browser clicks "Close" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared

