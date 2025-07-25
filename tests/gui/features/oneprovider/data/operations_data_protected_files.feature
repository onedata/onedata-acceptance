Feature: Operations on data-protected files inheriting protection from hardlink


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
                    - dir1
                    - dir2
                    - file1

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service

    When user of browser opens file browser for "space1" space
    And user of browser creates hard link of "file1" placed in "/dir1" directory on file browser in "space1"
    And user of browser goes to ".." in file browser
    And user of browser creates dataset for item "dir1" in "space1"

    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Write protection" option in data row menu in dataset browser
    And user of browser checks data write protection toggle in Write Protection modal

    And user of browser opens file browser for "space1" space


Scenario: User deletes non-protected file whose hardlink is in data write-protected dataset
    When user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"
    Then user of browser does not see any item(s) named "file2" in file browser


Scenario: User renames non-protected file whose hardlink is in data write-protected dataset
    When user of browser succeeds to rename "file1" to "file2" in "space1"
    Then user of browser does not see any item(s) named "file1" in file browser
    And user of browser sees item(s) named "file2" in file browser


Scenario: User moves non-protected file whose hardlink is in data write-protected dataset
    When user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Cut" option in data row menu in file browser
    And user of browser goes to "/dir2" in file browser
    And user of browser clicks "Paste" button from file browser menu bar
    Then user of browser sees item(s) named "file1" in file browser
