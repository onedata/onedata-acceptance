Feature: Basic data tab operations on directory JSON metadata in file browser


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
                - dir1:
                    - file2: 11111
                - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario Outline: Add valid metadata in JSON format
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<modal>" modal is opened on "Metadata" tab
    And user of browser clicks on "JSON" navigation tab in metadata panel
    And user of browser types '{"id": 1}' to JSON textarea in metadata panel
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "Close" button in modal "<modal>"
    Then user of browser sees metadata status tag for "<item>" in file browser
    And user of browser opens metadata panel on JSON tab for "<item>"
    And user of browser sees that JSON textarea in metadata panel contains '{"id": 1}'

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User doesn't see JSON metadata and metadata status tag after deleting JSON metadata
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser adds and saves '{"id": 1}' JSON metadata for "<item>"
    And user of browser opens metadata panel on JSON tab for "<item>"

    # remove JSON metadata
    And user of browser sees that JSON textarea in metadata panel contains '{"id": 1}'
    And user of browser cleans JSON textarea in metadata panel
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "Close" button in modal "<modal>"

    Then user of browser does not see metadata status tag for "<item>" in file browser
    And user of browser opens metadata panel on JSON tab for "<item>"
    And user of browser sees that JSON textarea in metadata panel is empty

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: Discard changes while entering metadata in JSON format
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser opens metadata panel on JSON tab for "<item>"
    And user of browser types '{"id": 1}' to JSON textarea in metadata panel
    And user of browser clicks on "Discard changes" button in metadata panel
    And user of browser clicks on "Close" button in modal "<modal>"

    And user of browser opens metadata panel on JSON tab for "<item>" directory
    Then user of browser sees that JSON textarea in metadata panel is empty

    Examples:
    | modal              | item  |
    | File details       | file1 |
    | Directory details  | dir1  |
