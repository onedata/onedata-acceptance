Feature: Create archive

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
                        - file1: 100
                    - file1: 100
                    - file2


    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service

    Scenario: User sees Editor disabled label after marking dataset and metadata write protection
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser click Dataset write protection toggle in Datasets modal
    And user of browser click Metadata write protection toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    Then user of browser sees data protected status tag for "dir1" in file browser
    And user of browser sees metadata protected status tag for "dir1" in file browser
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees Editor disabled label in Metadata modal
    And user of browser clicks on "Close" button in metadata modal

    Scenario: User sees that file has dataset tag with arrow after marking its parent directory as dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    Then user of browser double clicks on item named "dir1" in file browser
    And user of browser sees Dataset status tag for "file1" in file browser


