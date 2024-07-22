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
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    And user of browser clicks and presses enter on item named "20B-0.txt" in file browser
    Then user of browser sees that content of downloaded file "20B-0.txt" is equal to: "11111111111111111111"


  Scenario: User removes existing file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    And user of browser clicks once on item named "20B-0.txt" in file browser
    And user of browser clicks on menu for "20B-0.txt" file in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    Then user of browser sees that item named "20B-0.txt" has disappeared from file browser


  Scenario: User renames file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    And user of browser clicks once on item named "20B-0.txt" in file browser
    And user of browser clicks on menu for "20B-0.txt" file in file browser
    And user of browser clicks "Rename" option in data row menu in file browser
    And user of browser sees that "Rename" modal has appeared
    And user of browser writes "new_file1" into text field in modal "Rename modal"
    And user of browser confirms rename directory using enter

    Then user of browser sees that item named "20B-0.txt" has disappeared from file browser
    And user of browser sees that item named "new_file1" has appeared in file browser
    And user of browser sees that item named "new_file1" is file in file browser


  Scenario: User fails to rename file into incorrect name
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    And user of browser clicks once on item named "20B-0.txt" in file browser
    And user of browser clicks on menu for "20B-0.txt" file in file browser
    And user of browser clicks "Rename" option in data row menu in file browser
    And user of browser sees that "Rename" modal has appeared
    And user of browser writes ".." into text field in modal "Rename modal"
    And user of browser clicks "Rename" button in displayed modal
    Then user of browser sees that error modal with text "Renaming the file failed!" appeared
    And user of browser refreshes site
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that item named "20B-0.txt" is file in file browser


  Scenario: User sees that after uploading file with name of already existing file, the uploaded file appeared with suffix
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    Then user of browser sees that item named "20B-0(1).txt" has appeared in file browser


  Scenario: User with weak connection downloads file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    # User downloads file
    And user of browser downloads item named "20B-0.txt" with slow connection in file browser
    Then user of browser sees that content of downloaded file "20B-0.txt" is equal to: "11111111111111111111"


  Scenario: User writes to file and sees that date time in modified column is updated
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser enables only "modified" column in columns configuration popover in file browser table
    And user of browser saves content of "modified" column for "20B-0.txt" in file browser
    And using REST, space-owner-user writes "NEW CONTENT" to file named "20B-0.txt" in "space1" in oneprovider-1
    Then user of browser sees that date time in "modified" column for "20B-0.txt" has become more current in file browser


  Scenario: User adds metadata to file and sees that date time in changed column is updated
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser enables only "changed" column in columns configuration popover in file browser table
    And user of browser saves content of "changed" column for "20B-0.txt" in file browser
    And user of browser succeeds to write "20B-0.txt" file basic metadata: "attr=val" in "space1"
    And user of browser opens file browser for "space1" space
    Then user of browser sees that date time in "changed" column for "20B-0.txt" has become more current in file browser


  Scenario: User changes file permissions and sees that date time in changed column is updated
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser enables only "changed" column in columns configuration popover in file browser table
    And user of browser saves content of "changed" column for "20B-0.txt" in file browser
    And user of browser clicks on "Permissions" in context menu for "20B-0.txt"
    And user of browser sees that "Directory details" modal is opened on "Permissions" tab
    And user of browser selects "POSIX" permission type in edit permissions panel
    And user of browser sets "000" permission code in edit permissions panel
    And user of browser clicks on "Save" button in edit permissions panel
    And user of browser opens file browser for "space1" space
    Then user of browser sees that date time in "changed" column for "20B-0.txt" has become more current in file browser
