Feature: Basic management of harvester index that includes metadata in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And admin user does not have access to any space other than defined in next steps
    And initial spaces configuration in "onezone" Onezone service:
      space1:
        owner: admin
        providers:
          - oneprovider-1:
              storage: posix
              size: 1000000
        storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - dir1
    And user admin has no harvesters other than defined in next steps
    And user admin has "harvester1" harvester in "onezone" Onezone service
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario: User sees basic metadata values and keys after creating index that includes basic metadata
    When user of browser succeeds to write "dir1" directory basic metadata: "attr=val" in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["basic", "file_name"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser sees only following files in Data discovery page:
         dir1:
           xattrs:
             attr: "\"val\""
         spaces:
           - space1


  Scenario: User sees JSON metadata values and keys after creating index that includes only JSON metadata
    When user of browser succeeds to write "dir1" directory JSON metadata: '{"id": 1}' in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["json", "file_name"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser sees only following files in Data discovery page:
         dir1:
           id: 1
         spaces:
           - space1


  Scenario: User sees RDF metadata values and keys after creating index that includes only RDF metadata
    When user of browser succeeds to write "dir1" directory RDF metadata: "<a>first rdf</a>" in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["rdf", "file_name"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser sees only following files in Data discovery page:
         dir1:
           rdf:
             "\"<a>first rdf</a>\""
         spaces:
           - space1


  Scenario: User sees basic, JSON and RDF metadata values and keys after creating index that includes basic, JSON and RDF metadata
    When user of browser succeeds to write "dir1" directory basic metadata: "attr=val" in "space1"
    And user of browser succeeds to write "dir1" directory JSON metadata: '{"id": 1}' in "space1"
    And user of browser succeeds to write "dir1" directory RDF metadata: "<a>first rdf</a>" in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["rdf", "file_name", "basic", "json"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser sees only following files in Data discovery page:
         dir1:
           xattrs:
             attr: "\"val\""
           id: 1
           rdf:
             "\"<a>first rdf</a>\""
         spaces:
           - space1


  Scenario: User sees metadata existence flags after creating index that includes metadata existence flags info file detail
    When user of browser succeeds to write "dir1" directory basic metadata: "attr=val" in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["basic", "json", "rdf", "file_name", "metadata_existence_flags"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser sees only following files in Data discovery page:
       dir1:
         xattrs:
           attr: "\"val\""
         jsonMetadataExists: false
         rdfMetadataExists: false
         xattrsMetadataExists: true
       spaces:
         - space1


  Scenario: User sees rejection reason and what is rejected in Data Discovery page after changing JSON metadata value and creating index that includes "include rejection reason" and "retry on rejection" toggles
    When user of browser succeeds to write "dir1" directory JSON metadata: '{"id": 1}' in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["json", "file_name", "include_rejection_reason", "retry_on_rejection"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    # change JSON metadata
    And user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser opens metadata panel on JSON tab for "dir1"
    And user of browser cleans JSON textarea in metadata panel
    And user of browser clicks on "Save" button in metadata panel
    And user of browser types '{"id": "one"}' to JSON textarea in metadata panel
    And user of browser clicks on "Save" button in metadata panel

    # copy file id to clipboard
    And user of browser clicks on "Info" navigation tab in "Directory Details" modal
    And user of browser clicks on "File ID" button in modal "Directory details"
    And user of browser clicks on "X" button in modal "Directory details"

    And user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester1" on the harvesters list in the sidebar
    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser sees rejected: ["id"] in results list on data discovery page
    And user of browser sees that rejection is caused by field [id] of type [long] with ID from clipboard


  Scenario: User sees what is rejected in Data Discovery page after changing JSON metadata value and creating index that includes include retry on rejection toggles
    When user of browser succeeds to write "dir1" directory JSON metadata: '{"id": 1}' in "space1"
    And user of browser adds "space1" space to "harvester1" harvester using available spaces dropdown

    And user of browser creates new index "index1" that includes ["json", "file_name", "retry_on_rejection"] toggles for "harvester1"
    And user of browser changes indices to "index1" on GUI plugin tab for "harvester1"

    # change JSON metadata
    And user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser opens metadata panel on JSON tab for "dir1"
    And user of browser cleans JSON textarea in metadata panel
    And user of browser types '{"id": "one"}' to JSON textarea in metadata panel
    And user of browser clicks on "Save" button in metadata panel

    And user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester1" on the harvesters list in the sidebar
    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page
    Then user of browser sees rejected: ["id"] in results list on data discovery page
    And user of browser does not see "__rejectionReason" in results list on data discovery page

