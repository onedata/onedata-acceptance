Feature: Operations on non-protected file whose hardlink is in data write-protected dataset


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


Scenario: User deletes non-protected file whose hardlink is in data write-protected dataset
    When user of browser goes to file browser, creates hardlink of file located in "/file1" path and places it in "/dir1" path in "space1"
    And using web GUI, user of browser creates dataset with data and metadata write protection flags for item "dir1" in space "space1" in oneprovider-1
    
    And user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"
    Then user of browser does not see any item(s) named "file1" in file browser


Scenario: User renames non-protected file whose hardlink is in data write-protected dataset
    When user of browser goes to file browser, creates hardlink of file located in "/file1" path and places it in "/dir1" path in "space1"
    And using web GUI, user of browser creates dataset with data and metadata write protection flags for item "dir1" in space "space1" in oneprovider-1

    And user of browser succeeds to rename "file1" to "file2" in "space1"
    Then user of browser does not see any item(s) named "file1" in file browser
    And user of browser sees item(s) named "file2" in file browser


Scenario: User moves non-protected file whose hardlink is in data write-protected dataset
    When user of browser goes to file browser, creates hardlink of file located in "/file1" path and places it in "/dir1" path in "space1"
    And using web GUI, user of browser creates dataset with data and metadata write protection flags for item "dir1" in space "space1" in oneprovider-1

    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Cut" option in data row menu in file browser
    And user of browser goes to "/dir2" in file browser
    And user of browser clicks "Paste" button from file browser menu bar
    Then user of browser sees item(s) named "file1" in file browser
    And user of browser goes to ".." in file browser
    And user of browser does not see any item(s) named "file1" in file browser