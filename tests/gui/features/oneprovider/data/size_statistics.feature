Feature: Size statistics tests

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
                        - dir2

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees size statistics after turning on size statistics
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that displayed size in data row of "dir1" is "—"
    And user of browser clicks on menu for "dir1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "Size Statistics" item displayed in "Directory Details" modal is not active
    And user of browser closes "Directory Details" modal

    And user of browser clicks "Providers" of "space1" space in the sidebar
    And user of browser clicks on "oneprovider-1" provider on providers page
    And user of browser checks size statistics toggle on space configuration page

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser waits for displayed size in data row of "dir1" to be "3 B"
    And user of browser clicks on size statistics icon for "dir1" directory in file browser
    Then user of browser sees that charts title is "DIRECTORY SIZE STATISTICS" in modal "Directory Details"
    And user of browser sees that bytes chart title is "LOGICAL AND PHYSICAL BYTE SIZE" in modal "Directory Details"
    And user of browser sees that count chart title is "FILE COUNT" in modal "Directory Details"
    And user of browser clicks on chart in modal "Directory Details"
    And user of browser sees that tooltip with size statistics header has date format in modal "Directory Details"
