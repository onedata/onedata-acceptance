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


  Scenario: User creates new directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1
    And user of browser clicks "New directory" button from file browser menu bar
    And user of browser writes "dir1" into input name text field in modal "Create dir"
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


  Scenario: User sees modification date after uploading file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser sees that item named "20B-0.txt" has appeared in file browser
    Then user of browser sees that modification date of item named "20B-0.txt" is not earlier than 120 seconds ago in file browser


  Scenario: User sees file size after upload
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    # upload file
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    Then user of browser sees that item named "20B-0.txt" is of 20 B size in file browser


  Scenario: User uploads file and checks if provider name is displayed in the data distribution panel
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    # upload file
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    And user of browser clicks on menu for "20B-0.txt" file in file browser
    And user of browser clicks "Data distribution" option in data row menu in file browser

    And user of browser sees that "Data distribution" modal has appeared
    Then user of browser sees that chunk bar for provider "oneprovider-1" is entirely filled
    And user of browser clicks "Close" confirmation button in displayed modal

