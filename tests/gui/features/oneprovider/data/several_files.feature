Feature: Basic data tab operations on several files in file browser


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
                    - file1: 11111
                    - file2: 11111
                    - file3: 11111
                    - file4: 11111
                    - file5: 11111
                    - file6: 11111
                    - file7: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User selects a bunch of files using ctrl
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser sees items named ["file1", "file2", "file3", "file4", "file5", "file6", "file7"] in file browser in given order
    And user of browser selects ["file3", "file1"] items from file browser with pressed ctrl
    Then user of browser sees that ["file3", "file1"] items are selected in file browser
    And user of browser sees that "file2" item is not selected in file browser


  Scenario: User selects bunch of files using shift
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser sees items named ["file1", "file2", "file3", "file4", "file5", "file6", "file7"] in file browser in given order
    And user of browser selects ["file3", "file1"] items from file browser with pressed shift
    Then user of browser sees that ["file3", "file2", "file1"] items are selected in file browser


  Scenario: User selects bunch of files using ctrl and shift
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser sees items named ["file1", "file2", "file3", "file4", "file5", "file6", "file7"] in file browser in given order
    And user of browser selects ["file3", "file1"] items from file browser with pressed shift
    And user of browser selects "file5" item from file browser with pressed ctrl
    And user of browser selects "file7" item from file browser with pressed shift
    Then user of browser sees that ["file7", "file6", "file5", "file3", "file2", "file1"] items are selected in file browser


#  TODO: change test because of a new gui
#  Scenario: User sees that with several files selected only ["Create directory", "Create file", "Upload file", "Change element permissions", "Remove element"] buttons from toolbar are enabled
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees file browser in data tab in Oneprovider page
#
#    And user of browser selects ["file1", "file2"] items from file browser with pressed ctrl
#    Then user of browser sees that ["Create directory", "Create file", "Upload file", "Change element permissions", "Remove element"] buttons are enabled in toolbar in data tab in Oneprovider gui
#    And user of browser sees that ["Edit metadata", "Share element", "Rename element", "Copy element", "Cut element", "Show data distribution"] buttons are disabled in toolbar in data tab in Oneprovider gui


  Scenario: User removes several files
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser selects ["file1", "file2", "file3"] items from file browser with pressed ctrl
    And user of browser chooses Delete option from selection menu on file browser page
    And user of browser clicks on "Yes" button in modal "Delete modal"
    And user of browser sees that items named ["file1", "file2", "file3"] have disappeared from files browser
