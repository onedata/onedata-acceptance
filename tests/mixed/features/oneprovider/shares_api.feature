Feature: Shares api tests

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


  Scenario: User can see that command "Download file content" from api section in share file details modal works properly
    When user of browser opens shares view of "space1"
    And user of browser clicks "share_file1" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal is opened on "Info" tab
    And user of browser copies command "Download file content" in api section from file details modal
    And user of browser executes copied command
    And user1 sees that output of executed command is equal to: "11111"


  Scenario: User can see that command "Get attributes" from api section in share file details modal works properly
    When user of browser opens shares view of "space1"
    And user of browser clicks "share_file1" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal is opened on "Info" tab
    And user of browser copies command "Get attributes" in api section from file details modal
    And user of browser executes copied command
    And user1 sees that output of executed command contains:
        type: REG
        size: 5
        name: file1


  Scenario Outline: User can see that command "<command_name>" from api section in share file details modal works properly
    When using REST, user1 sets new <fmt> metadata: <metadata> for "file1" file in space "space1" in oneprovider-1
    And user of browser opens shares view of "space1"
    And user of browser clicks "share_file1" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal is opened on "Info" tab
    And user of browser copies command "<command_name>" in api section from file details modal
    And user of browser executes copied command
    And user1 sees that output of executed command contains:
        attr: val

    Examples:
    | fmt   | metadata        | command_name                     |
    | basic | attr=val        | Get extended attributes (xattrs) |
    | JSON  | {"attr": "val"} | Get JSON metadata                |


  Scenario: User can see that command "Get RDF metadata" from api section in share file details modal works properly
    When using REST, user1 sets new RDF metadata: <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> for "file1" file in space "space1" in oneprovider-1
    And user of browser opens shares view of "space1"
    And user of browser clicks "share_file1" share in shares browser on shares view
    And user of browser sees file browser on single share view
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal is opened on "Info" tab
    And user of browser copies command "Get RDF metadata" in api section from file details modal
    And user of browser executes copied command
    And user1 sees that output of executed command is equal to: "<rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>"

