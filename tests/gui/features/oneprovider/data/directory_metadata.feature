Feature: Basic data tab operations on directory metadata in file browser


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

  And user opened browser window
  And user of browser opened onezone page
  And user of browser logged as user1 to Onezone service

  Scenario: Open metadata panel and check presence of navigation tabs
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees that "Directory metadata" modal has appeared
    Then user of browser sees [Basic, JSON, RDF] navigation tabs in "Directory metadata" modal


  Scenario: Metadata icon is visible if directory has basic metadata entry
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    And user of browser does not see metadata status tag for "dir1" in file browser
    And user of browser opens "Directory metadata" modal for "dir1" directory
    And user of browser types "attr" to key input box of new metadata basic entry in "Directory metadata" modal
    And user of browser types "val" to value input box of attribute "attr" metadata basic entry in "Directory metadata" modal
    And user of browser clicks on "Save all" button in modal "Directory metadata"
    Then user of browser sees metadata status tag for "dir1" in file browser


    Scenario: Add basic metadata to directory and check their presence after reopening
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser adds basic entry with key "attr" and value "val" for directory
      And user of browser clicks on "Save all" button in modal "Directory metadata"
      Then user of browser sees metadata status tag for "dir1" in file browser

      And user of browser opens "Directory metadata" modal for "dir1" directory
      Then user of browser sees basic metadata entry with attribute named "attr" and value "val" in "Directory metadata" modal


    Scenario: Delete one of two basic metadata entry for directory
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser adds basic entry with key "attr1" and value "val1" for directory
      And user of browser adds basic entry with key "attr2" and value "val2" for directory
      And user of browser clicks on "Save all" button in modal "Directory metadata"
      And user of browser opens "Directory metadata" modal for "dir1" directory

      And user of browser clicks on delete basic metadata entry icon for basic metadata entry with attribute named "attr1" in "Directory metadata" modal
      Then user of browser does not see basic metadata entry with attribute named "attr1" in "Directory metadata" modal
      And user of browser sees basic metadata entry with attribute named "attr2" and value "val2" in "Directory metadata" modal
      And user of browser clicks on "Save all" button in modal "Directory metadata"

      # reopen modal for assurance
      And user of browser opens "Directory metadata" modal for "dir1" directory
      Then user of browser does not see basic metadata entry with attribute named "attr1" in "Directory metadata" modal
      And user of browser sees basic metadata entry with attribute named "attr2" and value "val2" in "Directory metadata" modal


    Scenario: Delete basic metadata for directory after saving it
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser adds basic entry with key "attr" and value "val" for directory
      And user of browser clicks on "Save all" button in modal "Directory metadata"

      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser clicks on delete basic metadata entry icon for basic metadata entry with attribute named "attr" in "Directory metadata" modal
      Then user of browser sees that there is no basic metadata for directory
      And user of browser clicks on "Save all" button in modal "Directory metadata"
      Then user of browser does not see metadata status tag for "dir1" in file browser

      # reopen modal for assurance
      And user of browser opens "Directory metadata" modal for "dir1" directory
      Then user of browser sees that there is no basic metadata for directory


    Scenario: Delete single basic metadata entry for directory (one visit in modal)
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser adds basic entry with key "attr" and value "val" for directory
      And user of browser sees basic metadata entry with attribute named "attr" and value "val" in "Directory metadata" modal
      And user of browser clicks on delete basic metadata entry icon for basic metadata entry with attribute named "attr" in "Directory metadata" modal
      Then user of browser sees that there is no basic metadata for directory

      And user of browser clicks on "Close" button in modal "Directory metadata"
      Then user of browser does not see metadata status tag for "dir1" in file browser

      And user of browser opens "Directory metadata" modal for "dir1" directory
      Then user of browser sees that there is no basic metadata for directory


    Scenario: User starts adding basic metadata to directory but discards changes
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser adds basic entry with key "attr" and value "val" for directory
      And user of browser clicks on "Discard changes" button in modal "Directory metadata"
      And user of browser opens "Directory metadata" modal for "dir1" directory
      Then user of browser does not see basic metadata entry with attribute named "attr" in "Directory metadata" modal


    Scenario: Add valid metadata to directory in JSON format
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser clicks on JSON navigation tab in "Directory metadata" modal
      And user of browser types "{"id": 1}" to JSON textarea in "Directory metadata" modal
      And user of browser clicks on "Save all" button in modal "Directory metadata"
      Then user of browser sees metadata status tag for "dir1" in file browser
      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser clicks on JSON navigation tab in "Directory metadata" modal
      Then user of browser sees that JSON textarea in "Directory metadata" modal contains {"id": 1}


    Scenario: User doesn't see JSON metadata and metadata status tag after deleting JSON metadata
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser adds "{"id": 1}" JSON metadata for "dir1" directory
      And user of browser opens JSON metadata tab for "dir1" directory

      # remove JSON metadata
      And user of browser sees that JSON textarea in "Directory metadata" modal contains {"id": 1}
      And user of browser cleans JSON textarea in "Directory metadata" modal
      And user of browser clicks on "Save all" button in modal "Directory metadata"

      Then user of browser does not see metadata status tag for "dir1" in file browser
      And user of browser opens JSON metadata tab for "dir1" directory
      Then user of browser sees that JSON textarea in "Directory metadata" modal is empty


    Scenario: Discard changes while entering metadata in JSON format
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser opens JSON metadata tab for "dir1" directory
      And user of browser types "{"id": 1}" to JSON textarea in "Directory metadata" modal
      And user of browser clicks on "Discard changes" button in modal "Directory metadata"

      And user of browser opens JSON metadata tab for "dir1" directory
      Then user of browser sees that JSON textarea in "Directory metadata" modal is empty


    Scenario: Add valid metadata to directory in XML format
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser clicks on RDF navigation tab in "Directory metadata" modal
      And user of browser types "<rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>" to RDF textarea in "Directory metadata" modal
      And user of browser clicks on "Save all" button in modal "Directory metadata"
      Then user of browser sees metadata status tag for "dir1" in file browser
      And user of browser opens "Directory metadata" modal for "dir1" directory
      And user of browser clicks on RDF navigation tab in "Directory metadata" modal
      Then user of browser sees that RDF textarea in "Directory metadata" modal contains <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>


    Scenario: User doesn't see RDF metadata and metadata status tag after deleting metadata in XML format
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser adds "<rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>" RDF metadata for "dir1" directory
      And user of browser opens RDF metadata tab for "dir1" directory

      # remove RDF metadata
      And user of browser sees that RDF textarea in "Directory metadata" modal contains <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>
      And user of browser cleans RDF textarea in "Directory metadata" modal
      And user of browser clicks on "Save all" button in modal "Directory metadata"

      Then user of browser does not see metadata status tag for "dir1" in file browser
      And user of browser opens RDF metadata tab for "dir1" directory
      Then user of browser sees that RDF textarea in "Directory metadata" modal is empty


    Scenario: Discard changes while entering metadata for directory in XML format
      When user of browser clicks "space1" on the spaces list in the sidebar
      And user of browser clicks Data of "space1" in the sidebar
      And user of browser sees file browser in data tab in Oneprovider page

      And user of browser opens RDF metadata tab for "dir1" directory
      And user of browser types "<rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>" to RDF textarea in "Directory metadata" modal
      And user of browser clicks on "Discard changes" button in modal "Directory metadata"

      And user of browser opens RDF metadata tab for "dir1" directory
      Then user of browser sees that RDF textarea in "Directory metadata" modal is empty
