Feature: Jump to file using jump input in file browser


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
    When user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser writes "file_1" to jump input in file browser and expects "file_100" to be highlighted
    Then user of browser sees that item named "file_100" is currently visible in file browser


  Scenario: User jumps to beginning of file list after writing "aaa" to jump input
    When user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser scrolls to the bottom of file browser
    And user of browser sees that item named "file_200" is currently visible in file browser
    And user of browser writes "aaa" to jump input in file browser and expects "file_001" to be highlighted
    Then user of browser sees that item named "file_001" is currently visible in file browser


  Scenario: User jumps to the end of the list after writing "zzz" to jump input
    When user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser writes "zzz" to jump input in file browser and expects "file_200" to be highlighted
    Then user of browser sees that item named "file_200" is currently visible in file browser


  Scenario: The user repeatedly scrolls through the same number of files from the top of the list at each screen size and always reaches the same set of files
    When user of browser opens file browser for "space1" space
    Then user of browser scrolls up 5 screens from the bottom of file browser in "space1" and always sees the same files after 10 trials for each screen size
