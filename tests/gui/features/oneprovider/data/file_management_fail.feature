Feature: Basic file management operations

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
                        - file1: 11111
                    - file1: 11111
                    - file2

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User fails to paste file to where it was copied from
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser double clicks on item named "dir1" in file browser
    And user of browser selects "file1" items from file browser with pressed ctrl
    And user of browser chooses Copy option from selection menu on file browser page
    And user of browser clicks "Paste" button from file browser menu bar

    Then user of browser sees that error modal with text "Copying some of files failed!" appeared


  Scenario: User fails to paste copied file to directory with identical file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser selects "file1" items from file browser with pressed ctrl
    And user of browser chooses Copy option from selection menu on file browser page

    And user of browser double clicks on item named "dir1" in file browser
    And user of browser clicks "Paste" button from file browser menu bar

    Then user of browser sees that error modal with text "Copying some of files failed!" appeared


  Scenario: User fails to paste copied file to directory without permissions
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    # change permissions
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "POSIX" permission type in edit permissions modal
    And user of browser sets "675" permission code in edit permissions modal
    And user of browser clicks "Save" confirmation button in displayed modal

    And user of browser clicks on menu for "file2" directory in file browser
    And user of browser clicks "Copy" option in data row menu in file browser

    And user of browser double clicks on item named "dir1" in file browser
    And user of browser clicks "Paste" button from file browser menu bar

    Then user of browser sees that error modal with text "Copying some of files failed!" appeared
