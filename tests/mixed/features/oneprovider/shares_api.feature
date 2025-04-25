Feature: Shares API tests

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
                - file1: 11111
    And opened browser with user1 signed in to "onezone" service
    And using REST, user user1 creates "share_file1" share of "space1/file1" supported by "oneprovider-1" provider


  Scenario: User reads file content using the command from "Download file content" from API section in share file details modal
    When user of browser opens shares view of "space1"
    And user of browser clicks "share_file1" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal is opened on "Info" tab
    And user of browser copies command for "Download file content" operation in API section from file details modal
    And user of browser executes copied command
    Then user of browser sees that output of executed command is equal to: "11111"


  Scenario: User reads file attributes using the command from "Get attributes" from API section in share file details modal
    When user of browser opens shares view of "space1"
    And user of browser clicks "share_file1" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal is opened on "Info" tab
    And user of browser copies command for "Get attributes" operation in API section from file details modal
    And user of browser executes copied command
    Then user of browser sees that output of executed command contains:
        type: REG
        size: 5
        name: file1


  Scenario Outline: User reads file metadata using the command from "<command_name>" from API section in share file details modal
    When using REST, user1 sets new <fmt> metadata: <metadata> for "file1" file in space "space1" in oneprovider-1
    And user of browser opens shares view of "space1"
    And user of browser clicks "share_file1" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal is opened on "Info" tab
    And user of browser copies command for "<command_name>" operation in API section from file details modal
    And user of browser executes copied command
    Then user of browser sees that output of executed command is equal to: "<expected_output>"

    Examples:
    | fmt    | metadata        | command_name                     | expected_output |
    | xattrs | attr=val        | Get extended attributes (xattrs) | {"attr":"val"}  |
    | JSON   | {"attr": "val"} | Get JSON metadata                | {"attr":"val"}  |
    | RDF    | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> | Get RDF metadata | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> |
