Feature: Basic files tab operations on several files in file browser


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
                    - file1: 11111
                    - file2: 11111
                    - file3: 11111
                    - file4: 11111
                    - file5: 11111
                    - file6: 11111
                    - file7: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User selects a bunch of files using ctrl
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser sees items named ["file1", "file2", "file3", "file4", "file5", "file6", "file7"] in file browser in given order
    And user of browser selects ["file3", "file1"] items from file browser with pressed ctrl
    Then user of browser sees that ["file3", "file1"] items are selected in file browser
    And user of browser sees that "file2" item is not selected in file browser


  Scenario: User selects bunch of files using shift
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser sees items named ["file1", "file2", "file3", "file4", "file5", "file6", "file7"] in file browser in given order
    And user of browser selects ["file3", "file1"] items from file browser with pressed shift
    Then user of browser sees that ["file3", "file2", "file1"] items are selected in file browser


  Scenario: User selects bunch of files using ctrl and shift
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser sees items named ["file1", "file2", "file3", "file4", "file5", "file6", "file7"] in file browser in given order
    And user of browser selects ["file3", "file1"] items from file browser with pressed shift
    And user of browser selects "file5" item from file browser with pressed ctrl
    And user of browser selects "file7" item from file browser with pressed shift
    Then user of browser sees that ["file7", "file6", "file5", "file3", "file2", "file1"] items are selected in file browser


  Scenario: User removes several files
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser selects ["file1", "file2", "file3"] items from file browser with pressed ctrl
    And user of browser chooses Delete option from selection menu on file browser page
    And user of browser clicks on "Yes" button in modal "Delete modal"
    Then user of browser sees that items named ["file1", "file2", "file3"] have disappeared from file browser


  Scenario: User copies and pastes several files into another location
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser creates dir "dir1" in current dir
    And user of browser selects ["file1", "file2", "file3"] items from file browser with pressed ctrl
    And user of browser chooses Copy option from selection menu on file browser page
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks "Paste" button from file browser menu bar
    Then user of browser sees item(s) named ["file1", "file2", "file3"] in file browser


  Scenario: User cuts and pastes several files into another location
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser creates dir "dir1" in current dir
    And user of browser selects ["file1", "file2", "file3"] items from file browser with pressed ctrl
    And user of browser chooses Cut option from selection menu on file browser page
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks "Paste" button from file browser menu bar

    Then user of browser sees item(s) named ["file1", "file2", "file3"] in file browser
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser sees that items named ["file1", "file2", "file3"] have disappeared from file browser