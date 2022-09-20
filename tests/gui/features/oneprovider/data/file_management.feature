Feature: Basic file management operations

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
                        - file1: 11111
                        - file_d1_2: 11111
                    - file1: 11111
                    - file2
                    - file3

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User successfully pastes file copied from other directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser selects "file_d1_2" items from file browser with pressed ctrl
    And user of browser chooses Copy option from selection menu on file browser page
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser clicks "Paste" button from file browser menu bar
    Then user of browser sees item(s) named file_d1_2 in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser sees item(s) named file_d1_2 in file browser


  Scenario: User successfully pastes file cut from other directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser selects "file_d1_2" items from file browser with pressed ctrl
    And user of browser chooses Cut option from selection menu on file browser page
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser clicks "Paste" button from file browser menu bar
    Then user of browser sees item(s) named file_d1_2 in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser does not see any item(s) named file_d1_2 in file browser


  Scenario: User fails to paste file to where it was copied from
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser selects "file1" items from file browser with pressed ctrl
    And user of browser chooses Copy option from selection menu on file browser page
    And user of browser clicks "Paste" button from file browser menu bar

    Then user of browser sees that error modal with text "Copying some of files failed!" appeared


  Scenario: User fails to paste copied file to directory with identical file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser selects "file1" items from file browser with pressed ctrl
    And user of browser chooses Copy option from selection menu on file browser page

    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks "Paste" button from file browser menu bar

    Then user of browser sees that error modal with text "Copying some of files failed!" appeared


  Scenario: Space owner can copy file to a directory which has 677 permission code
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    # change permissions
    And user of browser clicks on "Permissions" in context menu for "dir1"
    And user of browser sees that "Directory details" modal is opened on "Permissions" tab
    And user of browser selects "POSIX" permission type in edit permissions panel
    And user of browser sets "677" permission code in edit permissions panel
    And user of browser clicks on "Save" button in edit permissions panel
    And user of browser clicks on "Close" button in modal "Directory details"

    And user of browser clicks on menu for "file2" directory in file browser
    And user of browser clicks "Copy" option in data row menu in file browser

    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks "Paste" button from file browser menu bar

    Then user of browser sees item(s) named file2 in file browser
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser sees item(s) named file2 in file browser


  Scenario: Space owner can move file to a directory which has 677 permission code
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    # change permissions
    And user of browser clicks on "Permissions" in context menu for "dir1"
    And user of browser sees that "Directory details" modal is opened on "Permissions" tab
    And user of browser selects "POSIX" permission type in edit permissions panel
    And user of browser sets "677" permission code in edit permissions panel
    And user of browser clicks on "Save" button in edit permissions panel
    And user of browser clicks on "Close" button in modal "Directory details"

    And user of browser clicks on menu for "file3" directory in file browser
    And user of browser clicks "Cut" option in data row menu in file browser

    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks "Paste" button from file browser menu bar

    Then user of browser sees item(s) named file3 in file browser
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser does not see any item(s) named file3 in file browser
