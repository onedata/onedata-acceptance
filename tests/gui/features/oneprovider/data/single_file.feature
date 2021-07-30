Feature: Basic files tab operations on single file in file browser


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
                    - 20B-0.txt: 11111111111111111111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User downloads file and checks it's content
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1

    And user of browser double clicks on item named "20B-0.txt" in file browser
    Then user of browser sees that content of downloaded file "20B-0.txt" is equal to: "11111111111111111111"


  Scenario: User removes existing file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1

    And user of browser clicks once on item named "20B-0.txt" in file browser
    And user of browser clicks on menu for "20B-0.txt" file in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    Then user of browser sees that item named "20B-0.txt" has disappeared from file browser


  Scenario: User renames file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1

    And user of browser clicks once on item named "20B-0.txt" in file browser
    And user of browser clicks on menu for "20B-0.txt" file in file browser
    And user of browser clicks "Rename" option in data row menu in file browser
    And user of browser sees that "Rename" modal has appeared
    And user of browser writes "new_file1" into text field in modal "Rename modal"
    And user of browser confirms rename directory using enter

    Then user of browser sees that item named "20B-0.txt" has disappeared from file browser
    And user of browser sees that item named "new_file1" has appeared in file browser
    And user of browser sees that item named "new_file1" is file in file browser


  Scenario: User sees that after uploading file with name of already existing file, the uploaded file appeared with suffix
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    Then user of browser sees that item named "20B-0(1).txt" has appeared in file browser

