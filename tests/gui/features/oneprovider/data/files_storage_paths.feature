Feature: File storage paths tests

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
                  - file1: some file content
    And opened browser with user1 signed in to "onezone" service


  Scenario: User can see path of the file on a physical storage using GUI and the file can be accessed on the storage
    When user of browser opens file browser for "space1" space
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks on "Information" in context menu for "file1"
    Then user of browser sees path physical location in file details and copies it into the clipboard
    And user of browser sees that there is a file with content "some file content", in provider's storage mount point, under a path copied to clipboard
