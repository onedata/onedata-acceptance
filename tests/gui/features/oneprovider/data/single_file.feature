Feature: Basic data tab operations on single file in file browser


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
                    - 20B-0.txt: 11111111111111111111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User downloads file and checks it's content
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1

    And user of browser double clicks on item named "20B-0.txt" in file browser
    Then user of browser sees that content of downloaded file "20B-0.txt" is equal to: "11111111111111111111"


# TODO: change test because of a new gui
#  Scenario: User fails to create new file because of existing file with given name
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees that current working directory displayed in breadcrumbs is space1
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "20B-0.txt" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    Then user of browser sees an error notify with text matching to: .*failed.*


  Scenario: User removes existing file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1

    And user of browser clicks once on item named "20B-0.txt" in file browser
    And user of browser clicks on menu for "20B-0.txt" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    Then user of browser sees that item named "20B-0.txt" has disappeared from files browser


  Scenario Outline: User renames file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1

    And user of browser clicks once on item named "20B-0.txt" in file browser
    And user of browser clicks on menu for "20B-0.txt" directory in file browser
    And user of browser clicks "Rename" option in data row menu in file browser
    And user of browser sees that "Rename" modal has appeared
    And user of browser writes "new_file1" into name directory text field in modal "Rename modal"
    And user of browser confirms rename directory using <confirmation_method>

    Then user of browser sees that item named "20B-0.txt" has disappeared from files browser
    And user of browser sees that item named "new_file1" has appeared in file browser
    And user of browser sees that item named "new_file1" is file in file browser

    Examples:
    | confirmation_method |
    | enter               |
    | button              |


  Scenario: User sees that after uploading file with name of already existing file, the uploaded file appeared with suffix
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    Then user of browser sees that item named "20B-0(1).txt" has appeared in file browser

