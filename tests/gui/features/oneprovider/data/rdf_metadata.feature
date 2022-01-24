Feature: Basic data tab operations on directory RDF metadata in file browser


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


   Scenario Outline: Add valid metadata in XML format
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser clicks on RDF navigation tab in metadata modal
    And user of browser types '<content>' to RDF textarea in metadata modal
    And user of browser clicks on "Save all" button in metadata modal
    Then user of browser sees metadata status tag for "<item>" in file browser
    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser clicks on RDF navigation tab in metadata modal
    Then user of browser sees that RDF textarea in metadata modal contains '<content>'

    Examples:
    | modal              | item  | content |
    | File metadata      | file1 | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> |
    | Directory metadata | dir1  | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> |


  Scenario Outline: User doesn't see RDF metadata and metadata status tag after deleting metadata in XML format
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser adds and saves '<content>' RDF metadata for "<item>"
    And user of browser opens metadata modal on RDF tab for "<item>"

    # remove RDF metadata
    And user of browser sees that RDF textarea in metadata modal contains '<content>'
    And user of browser cleans RDF textarea in metadata modal
    And user of browser clicks on "Save all" button in metadata modal

    Then user of browser does not see metadata status tag for "<item>" in file browser
    And user of browser opens metadata modal on RDF tab for "<item>" directory
    Then user of browser sees that RDF textarea in metadata modal is empty

    Examples:
    | item  | content |
    | file1 | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> |
    | dir1  | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> |


  Scenario Outline: Discard changes while entering metadata for directory in XML format
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser opens metadata modal on RDF tab for "<item>"
    And user of browser types '<content>' to RDF textarea in metadata modal
    And user of browser clicks on "Discard changes" button in metadata modal

    And user of browser opens metadata modal on RDF tab for "<item>" directory
    Then user of browser sees that RDF textarea in metadata modal is empty

    Examples:
    | item  | content |
    | file1 | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> |
    | dir1  | <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML> |
