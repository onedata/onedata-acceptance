Feature: Navigating large file lists with a single browser


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

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service
    And using REST, user1 creates 200 empty files in "space1" named "file_001", "file_002", ..., "file_N" supported by "oneprovider-1" provider


  Scenario: User successfully jumps to a previously non-visible file after writing its name prefix to jump input
    When user of browser opens file browser for "space1" space
    And user of browser writes "file_1" to jump input in file browser and expects "file_100" to be highlighted
    Then user of browser sees that item named "file_100" is currently visible in file browser


  Scenario: User jumps to beginning of file list after writing "aaa" to jump input
    When user of browser opens file browser for "space1" space
    And user of browser scrolls to the bottom of file browser with "file_200" as the expected last file
    And user of browser sees that item named "file_200" is currently visible in file browser
    And user of browser writes "aaa" to jump input in file browser and expects "file_001" to be highlighted
    Then user of browser sees that item named "file_001" is currently visible in file browser


  Scenario: User jumps to the end of the list after writing "zzz" to jump input
    When user of browser opens file browser for "space1" space
    And user of browser writes "zzz" to jump input in file browser and expects "file_200" to be highlighted
    Then user of browser sees that item named "file_200" is currently visible in file browser


  Scenario: User repeatedly scrolls up the same number of screens from the end of the list and always sees the same files
    When user of browser opens file browser for "space1" space
    And user of browser scrolls to the bottom of file browser with "file_200" as the expected last file
    And user of browser scrolls up 7 screens in file browser
    And user of browser remembers visible files list in file browser

    Then user of browser scrolls to the bottom of file browser with "file_200" as the expected last file
    And user of browser scrolls up 7 screens in file browser
    And user of browser sees that visible files list is the same as remembered in file browser
