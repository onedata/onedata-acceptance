Feature: Basic data tab operations on directory metadata in file browser


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

  Scenario Outline: Open metadata modal and check absence of any metadata
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser clicks on menu for "<item>" directory in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees that "<modal>" modal has appeared
    Then user of browser sees [Basic, JSON, RDF] navigation tabs in metadata modal
    And user of browser sees that all metadata tabs are marked as empty
    And user of browser sees that there is no metadata in metadata modal

    Examples:
    | modal               | item  |
    | File metadata       | file1 |
    | Directory metadata  | dir1  |


  Scenario Outline: User adds basic metadata entry and checks their presence with metadata status tag
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser does not see metadata status tag for "<item>" in file browser
    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser types "attr" to key input box of new metadata basic entry
    And user of browser types "val" to value input box of attribute "attr" metadata basic entry
    And user of browser clicks on "Save all" button in metadata modal
    Then user of browser sees metadata status tag for "<item>" in file browser
    And user of browser clicks on metadata status tag for "<item>" in file browser
    Then user of browser sees that "<modal>" modal has appeared
    And user of browser sees basic metadata entry with attribute named "attr" and value "val"

    Examples:
    | modal              | item  |
    | File metadata      | file1 |
    | Directory metadata | dir1  |


  Scenario Outline: Delete one of two basic metadata entries
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser adds basic entry with key "attr1" and value "val1"
    And user of browser adds basic entry with key "attr2" and value "val2"
    And user of browser clicks on "Save all" button in metadata modal
    And user of browser opens "<modal>" metadata modal for "<item>"

    And user of browser clicks on delete icon for basic metadata entry with attribute named "attr1"
    Then user of browser does not see basic metadata entry with attribute named "attr1"
    And user of browser sees basic metadata entry with attribute named "attr2" and value "val2"
    And user of browser clicks on "Save all" button in metadata modal

    # reopen modal for assurance
    And user of browser opens "<modal>" metadata modal for "<item>"
    Then user of browser does not see basic metadata entry with attribute named "attr1"
    And user of browser sees basic metadata entry with attribute named "attr2" and value "val2"

    Examples:
    | modal              | item  |
    | File metadata      | file1 |
    | Directory metadata | dir1  |


  Scenario Outline: Delete all basic metadata entries after saving it
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser adds basic entry with key "attr" and value "val"
    And user of browser clicks on "Save all" button in metadata modal

    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser clicks on delete icon for basic metadata entry with attribute named "attr"
    Then user of browser sees that there is no basic metadata
    And user of browser clicks on "Save all" button in metadata modal
    Then user of browser does not see metadata status tag for "<item>" in file browser

    # reopen modal for assurance
    And user of browser opens "<modal>" metadata modal for "<item>"
    Then user of browser sees that there is no basic metadata

    Examples:
    | modal              | item  |
    | File metadata      | file1 |
    | Directory metadata | dir1  |


  Scenario Outline: Delete single basic metadata entry (one visit in modal)
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser adds basic entry with key "attr" and value "val"
    And user of browser sees basic metadata entry with attribute named "attr" and value "val"
    And user of browser clicks on delete icon for basic metadata entry with attribute named "attr"
    Then user of browser sees that there is no basic metadata

    And user of browser clicks on "Close" button in metadata modal
    Then user of browser does not see metadata status tag for "<item>" in file browser

    And user of browser opens "<modal>" metadata modal for "<item>"
    Then user of browser sees that there is no basic metadata

    Examples:
    | modal              | item  |
    | File metadata      | file1 |
    | Directory metadata | dir1  |


  Scenario Outline: User starts adding basic metadata, but discards changes
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser adds basic entry with key "attr" and value "val"
    And user of browser clicks on "Discard changes" button in metadata modal
    And user of browser opens "<modal>" metadata modal for "<item>"
    Then user of browser does not see basic metadata entry with attribute named "attr"

    Examples:
    | modal              | item  |
    | File metadata      | file1 |
    | Directory metadata | dir1  |


  Scenario Outline: Add valid metadata in JSON format
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser clicks on JSON navigation tab in metadata modal
    And user of browser types '{"id": 1}' to JSON textarea in metadata modal
    And user of browser clicks on "Save all" button in metadata modal
    Then user of browser sees metadata status tag for "<item>" in file browser
    And user of browser opens "<modal>" metadata modal for "<item>"
    And user of browser clicks on JSON navigation tab in metadata modal
    Then user of browser sees that JSON textarea in metadata modal contains '{"id": 1}'

    Examples:
    | modal              | item  |
    | File metadata      | file1 |
    | Directory metadata | dir1  |


  Scenario Outline: User doesn't see JSON metadata and metadata status tag after deleting JSON metadata
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser adds and saves '{"id": 1}' JSON metadata for "<item>"
    And user of browser opens metadata modal on JSON tab for "<item>"

    # remove JSON metadata
    And user of browser sees that JSON textarea in metadata modal contains '{"id": 1}'
    And user of browser cleans JSON textarea in metadata modal
    And user of browser clicks on "Save all" button in metadata modal

    Then user of browser does not see metadata status tag for "<item>" in file browser
    And user of browser opens metadata modal on JSON tab for "<item>"
    Then user of browser sees that JSON textarea in metadata modal is empty

    Examples:
    | item  |
    | file1 |
    | dir1  |


  Scenario Outline: Discard changes while entering metadata in JSON format
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser opens metadata modal on JSON tab for "<item>"
    And user of browser types '{"id": 1}' to JSON textarea in metadata modal
    And user of browser clicks on "Discard changes" button in metadata modal

    And user of browser opens metadata modal on JSON tab for "<item>" directory
    Then user of browser sees that JSON textarea in metadata modal is empty

    Examples:
    | item  |
    | file1 |
    | dir1  |


  Scenario Outline: Add valid metadata in XML format
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
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
    And user of browser clicks Files of "space1" in the sidebar
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
    And user of browser clicks Files of "space1" in the sidebar
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
