Feature: Basic data tab operations on nested directory structure in file browser


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
                    - dir1:
                        - file2: 11111
                        - file3: 11111
                    - dir2:
                        - dir3
                        - dir4:
                            - file4: 11111
                            - file5: 11111
                            - file6: 11111
                            - file7: 11111
                            - file8: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User changes directory using breadcrumbs
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1

    And user of browser double clicks on item named "dir2" in file browser
    And user of browser sees that current working directory displayed in breadcrumbs is /dir2
    And user of browser double clicks on item named "dir4" in file browser
    And user of browser sees that current working directory displayed in breadcrumbs is /dir2/dir4

    And user of browser changes current working directory to home using breadcrumbs
    Then user of browser sees that current working directory displayed in breadcrumbs is space1


# TODO: change test because of a new gui
#  Scenario: User sees that with several directories selected only ["Create directory", "Create file", "Upload file", "Change element permissions", "Remove element"] buttons from toolbar are enabled
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees file browser in data tab in Oneprovider page
#    And user of browser selects ["dir1", "dir2"] items from file browser with pressed ctrl
#    Then user of browser sees that ["Create directory", "Create file", "Upload file", "Change element permissions", "Remove element"] buttons are enabled in toolbar in data tab in Oneprovider gui
#    And user of browser sees that ["Share element", "Edit metadata", "Rename element", "Copy element", "Cut element", "Show data distribution"] buttons are disabled in toolbar in data tab in Oneprovider gui
#
#
#  Scenario: User sees that with directory and file selected only ["Create directory", "Create file", "Upload file", "Remove element"] buttons from toolbar are enabled
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees file browser in data tab in Oneprovider page
#    And user of browser selects ["dir1", "file1"] items from file browser with pressed ctrl
#    Then user of browser sees that ["Create directory", "Create file", "Upload file", "Remove element"] buttons are enabled in toolbar in data tab in Oneprovider gui
#    And user of browser sees that ["Share element", "Edit metadata", "Rename element", "Change element permissions", "Copy element", "Cut element", "Show data distribution"] buttons are disabled in toolbar in data tab in Oneprovider gui


  Scenario: User removes directory containing several files
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1

    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    And user of browser sees that item named "dir1" has disappeared from files browser


  Scenario: User enters directory and views files in it
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser double clicks on item named "dir1" in file browser
    Then user of browser sees items named ["file2", "file3"] in file browser in given order

