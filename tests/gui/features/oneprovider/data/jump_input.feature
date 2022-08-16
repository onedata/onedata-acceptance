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

    And using REST, user1 creates 200 empty files in "space1" with names sorted alphabetically supported by "oneprovider-1" provider
    And users opened browser browsers' windows
    And users of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User successfully jumps to a previously non-visible file after writing its name prefix to jump input
    When user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser writes "file_1" to jump input in file browser
    Then user of browser sees that item named "file_100" is currently visible in file browser


  Scenario: User jumps to beginning of file list after writing "aaa" to jump input
    When user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser scrolls to the bottom of file browser
    And user of browser sees that item named "file_200" is currently visible in file browser
    And user of browser writes "aaa" to jump input in file browser
    Then user of browser sees that item named "file_001" is currently visible in file browser


  Scenario: User jumps to the end of the list after writing "zzz" to jump input
    When user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser writes "zzz" to jump input in file browser
    Then user of browser sees that item named "file_200" is currently visible in file browser

