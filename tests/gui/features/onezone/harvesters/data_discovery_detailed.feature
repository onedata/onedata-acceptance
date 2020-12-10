Feature: Testing features in Discovery Page in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And admin user does not have access to any space other than defined in next steps
    And initial spaces configuration in "onezone" Onezone service:
          space_of_files_with_xattrs:
            owner: admin
            providers:
              - oneprovider-1:
                  storage: posix
                  size: 1000000
            storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - dir1_1:
                    - file_with_xattrs1:
                        content: 11111
                        metadata:
                          type: basic
                          author: John Doe
                          year: 1998
                    - file_with_xattrs2:
                        content: 11111
                        metadata:
                          type: basic
                          author: John Doe
                          year: 1970
                    - file_with_xattrs3:
                        content: 11111
                        metadata:
                          type: basic
                          author: Samantha Anderson
                          year: 2000
                    - file_with_xattrs4:
                        content: 11111
                        metadata:
                          type: basic
                          author: John Smith
                          year: 1998
          space_of_files_with_json_meta:
            owner: admin
            providers:
              - oneprovider-1:
                  storage: posix
                  size: 1000000
            storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - dir2_1:
                    - file_with_json1:
                        content: 11111
                        metadata:
                          type: json
                          author: John Doe
                          year: 1998
                    - file_with_json2:
                        content: 11111
                        metadata:
                          type: json
                          author: John Doe
                          year: 1970
                    - file_with_json3:
                        content: 11111
                        metadata:
                          type: json
                          author: Samantha Anderson
                          year: 2000
                    - file_with_json4:
                        content: 11111
                        metadata:
                          type: json
                          author: John Smith
                          year: 1998

    And user admin has no harvesters other than defined in next steps
    And user admin has "harvester1" harvester in "onezone" Onezone service
    And spaces ["space_of_files_with_xattrs", "space_of_files_with_json_meta"] belong to "harvester1" harvester of user admin
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario: Files records are paged for as many is given
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    And user of browser sees that paging is set for 10 pages
    Then user of browser sees 10 files on data discovery page
    And user of browser opens next page of data discovery page
    And user of browser sees 2 files on data discovery page


  Scenario: User can filter visible properties of files records
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # author contains "John Smith"
    And user of browser clicks on add query block icon in data discovery page
    And user of browser chooses "any property" property for a query in query builder popup
    And user of browser chooses "has phrase" from comparators list in query builder popup
    And user of browser writes "John Smith" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup
    And user of browser clicks "Query" button on data discovery page

    And user of browser clicks "Filter properties" button on data discovery page
    And user of browser chooses following properties to filter on data discovery page:
          - author
          - __onedata:
              - fileName
              - xattrs:
                  - author

    And user of browser clicks "Filter properties" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_json4:
              author: "\"John Smith\""
            file_with_xattrs4:
              xattrs:
                author: "\"John Smith\""

    And user of browser does not see following properties of files in data discovery page:
            file_with_json4:
              year: 1998
            file_with_xattrs4:
              xattrs:
                year: 1998


  Scenario: User can sort files records
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester
    And user of browser chooses "__onedata.fileName.keyword" sorting parameter on data discovery page
    And user of browser chooses "asc" sorting order on data discovery page
    Then user of browser sees files with following order on data discovery page:
          - dir1_1
          - dir2_1
          - file_with_json1
          - file_with_json2
          - file_with_json3
          - file_with_json4
          - file_with_xattrs1
          - file_with_xattrs2
          - file_with_xattrs3
          - file_with_xattrs4

    And user of browser opens next page of data discovery page
    And user of browser sees files with following order on data discovery page:
          - space_of_files_with_json_meta
          - space_of_files_with_xattrs


  Scenario: User can query for data with curl command given in GUI
    When user of browser removes all tokens
    And user of browser creates new token named "Onezone REST" with basic Onezone REST Access template
    And user of browser clicks on copy button in token view
    And user of browser sets copied access token as TOKEN environment variable
    And user of browser opens Data Discovery page of "harvester1" harvester

    # author contains "John Smith"
    And user of browser clicks on add query block icon in data discovery page
    And user of browser chooses "any property" property for a query in query builder popup
    And user of browser chooses "has phrase" from comparators list in query builder popup
    And user of browser writes "John Smith" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "REST API" button on data discovery page
    And user of browser clicks copy command icon in REST API modal
    And user of browser runs copied curl command
    Then user of browser sees that querying curl result matches following files:
          file_with_json4:
            year: 1998
            author: John Smith
          file_with_xattrs4:
            xattrs:
              year: 1998
              author: John Smith
