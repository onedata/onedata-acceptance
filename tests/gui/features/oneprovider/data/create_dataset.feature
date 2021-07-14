Feature: Create Dataset


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
                    - file1: 110
                    - file2: 110
                    - file3: 110


    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service

    Scenario: User sees that file has dataset tag set after marking it as dataset
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks Mark this file as dataset toggle in Datasets modal
    And user of browser clicks Close button in Datasets modal
    Then user of browser sees Dataset status tag for "file1" in file browser
