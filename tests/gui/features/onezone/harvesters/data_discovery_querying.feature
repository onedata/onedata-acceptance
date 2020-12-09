Feature: Querying for data discovery in Discovery Page in Onezone GUI

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


  Scenario: Metadata keys are harvested when default index is set in GUI plugin
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester1" on the harvesters list in the sidebar
    And user of browser clicks Indices of "harvester1" harvester in the sidebar
    And user of browser sees "Used by GUI" tag on "generic-index" index record in indices page
    And user of browser expands "generic-index" index record in indices page
    And user of browser sees 100% progress for all spaces in "generic-index" index harvesting

    And user of browser opens Data Discovery page of "harvester1" harvester

    And user of browser clicks on add query block icon in data discovery page
    And user of browser clicks on condition properties expander in query builder
    Then user of browser sees ["author", "year"] on condition properties list


  Scenario: User sees appropriate files after searching by "any property" property
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # author contains "John"
    And user of browser clicks on add query block icon in data discovery page
    And user of browser chooses "any property" property for a query in query builder popup
    And user of browser chooses "has phrase" from comparators list in query builder popup
    And user of browser writes "John Smith" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_json4:
              spaceId: space_of_files_with_json_meta
              author: "\"John Smith\""
              year: 1998
            file_with_xattrs4:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Smith\""
                year: 1998

  Scenario: User sees appropriate files after searching by JSON metadata values
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # author contains "John"
    And user of browser clicks on add query block icon in data discovery page
    And user of browser chooses "author" property for a query in query builder popup
    And user of browser chooses "contains" from comparators list in query builder popup
    And user of browser writes "John" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_json1:
              spaceId: space_of_files_with_json_meta
              author: "\"John Doe\""
              year: 1998
            file_with_json2:
              spaceId: space_of_files_with_json_meta
              author: "\"John Doe\""
              year: 1970
            file_with_json4:
              spaceId: space_of_files_with_json_meta
              author: "\"John Smith\""
              year: 1998


  Scenario: User sees appropriate files after searching by JSON metadata value keyword
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # author.keyword is "John Doe"
    And user of browser clicks on add query block icon in data discovery page
    And user of browser chooses "author.keyword" property for a query in query builder popup
    And user of browser chooses "is" from comparators list in query builder popup
    And user of browser writes "John Doe" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_json1:
              spaceId: space_of_files_with_json_meta
              author: "\"John Doe\""
              year: 1998
            file_with_json2:
              spaceId: space_of_files_with_json_meta
              author: "\"John Doe\""
              year: 1970


  Scenario: User sees appropriate files after searching by xattrs metadata values
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # __onedata.xattrs.author.__value contains "John"
    And user of browser clicks on add query block icon in data discovery page
    And user of browser chooses "__onedata.xattrs.author.__value" property for a query in query builder popup
    And user of browser chooses "contains" from comparators list in query builder popup
    And user of browser writes "John" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_xattrs1:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Doe\""
                year: 1998
            file_with_xattrs2:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Doe\""
                year: 1970
            file_with_xattrs4:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Smith\""
                year: 1998


  Scenario: User sees appropriate files after searching by xattrs metadata value keyword
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # __onedata.xattrs.author.__value.keyword is "John Doe"
    And user of browser clicks on add query block icon in data discovery page
    And user of browser chooses "__onedata.xattrs.author.__value.keyword" property for a query in query builder popup
    And user of browser chooses "is" from comparators list in query builder popup
    And user of browser writes "John Doe" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_xattrs1:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Doe\""
                year: 1998
            file_with_xattrs2:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Doe\""
                year: 1970


  Scenario: User sees appropriate files after searching using OR
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # author.keyword is "John Doe" OR author contains Samantha
    And user of browser clicks on add query block icon in data discovery page
    And user of browser clicks OR operator in query builder popup

    And user of browser clicks on add another query block icon in data discovery page
    And user of browser chooses "author.keyword" property for a query in query builder popup
    And user of browser chooses "is" from comparators list in query builder popup
    And user of browser writes "John Doe" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks on add another query block icon in data discovery page
    And user of browser chooses "author" property for a query in query builder popup
    And user of browser chooses "contains" from comparators list in query builder popup
    And user of browser writes "Samantha" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_json1:
              spaceId: space_of_files_with_json_meta
              author: "\"John Doe\""
              year: 1998
            file_with_json2:
              spaceId: space_of_files_with_json_meta
              author: "\"John Doe\""
              year: 1970
            file_with_json3:
              spaceId: space_of_files_with_json_meta
              author: "\"Samantha Anderson\""
              year: 2000


  Scenario: User sees appropriate files after searching using AND
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # author contains "John" AND year = 1998
    And user of browser clicks on add query block icon in data discovery page
    And user of browser clicks AND operator in query builder popup

    And user of browser clicks on add another query block icon in data discovery page
    And user of browser chooses "author" property for a query in query builder popup
    And user of browser chooses "contains" from comparators list in query builder popup
    And user of browser writes "John" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks on add another query block icon in data discovery page
    And user of browser chooses "year" property for a query in query builder popup
    And user of browser chooses "=" from comparators list in query builder popup
    And user of browser writes "1998" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_json1:
              spaceId: space_of_files_with_json_meta
              author: "\"John Doe\""
              year: 1998
            file_with_json4:
              spaceId: space_of_files_with_json_meta
              author: "\"John Smith\""
              year: 1998


  Scenario: User sees appropriate files after searching using NOT with space attribute
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # NOT space is space_of_files_with_json_meta
    And user of browser clicks on add query block icon in data discovery page
    And user of browser clicks NOT operator in query builder popup

    And user of browser clicks on add another query block icon in data discovery page
    And user of browser chooses "space" property for a query in query builder popup
    And user of browser chooses "is" from comparators list in query builder popup
    And user of browser chooses "space_of_files_with_json_meta" from property values list in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_xattrs1:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Doe\""
                year: 1998
            file_with_xattrs2:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Doe\""
                year: 1970
            file_with_xattrs3:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"Samantha Anderson\""
                year: 2000
            file_with_xattrs4:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Smith\""
                year: 1998
            dir1_1:
              spaceId: space_of_files_with_xattrs
            spaces:
              - space_of_files_with_xattrs


  Scenario: User sees appropriate files after searching using NOT with another property
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # NOT year = 1998
    And user of browser clicks on add query block icon in data discovery page
    And user of browser clicks NOT operator in query builder popup

    And user of browser clicks on add another query block icon in data discovery page
    And user of browser chooses "year" property for a query in query builder popup
    And user of browser chooses "=" from comparators list in query builder popup
    And user of browser writes "1998" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_json2:
              spaceId: space_of_files_with_json_meta
              author: "\"John Doe\""
              year: 1970
            file_with_json3:
              spaceId: space_of_files_with_json_meta
              author: "\"Samantha Anderson\""
              year: 2000
            file_with_xattrs1:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Doe\""
                year: 1998
            file_with_xattrs2:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Doe\""
                year: 1970
            file_with_xattrs3:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"Samantha Anderson\""
                year: 2000
            file_with_xattrs4:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Smith\""
                year: 1998
            dir1_1:
              spaceId: space_of_files_with_xattrs
            dir2_1:
              spaceId: space_of_files_with_json_meta
            spaces:
              - space_of_files_with_xattrs
              - space_of_files_with_json_meta


  Scenario: User sees appropriate files after searching with complex expression
    When user of browser waits until harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # (author contains "John" OR auhor.keyword is "Samantha Anderson") AND (NOT author.keyword is "John Smith") AND year > 1970
    And user of browser clicks on add query block icon in data discovery page
    And user of browser clicks AND operator in query builder popup

    # author contains "John" OR auhor.keyword is "Samantha Anderson"
    And user of browser clicks on add another query block icon in data discovery page
    And user of browser clicks OR operator in query builder popup

    # author contains "John"
    And user of browser clicks on add another query block icon in data discovery page
    And user of browser chooses "author" property for a query in query builder popup
    And user of browser chooses "contains" from comparators list in query builder popup
    And user of browser writes "John" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    # author.keyword is "Samantha Anderson"
    And user of browser clicks on add another query block icon in data discovery page
    And user of browser chooses "author.keyword" property for a query in query builder popup
    And user of browser chooses "is" from comparators list in query builder popup
    And user of browser writes "Samantha Anderson" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    # NOT author.keyword is "John Smith"
    And user of browser clicks on 2 nd from the left add query block icon in data discovery page
    And user of browser clicks NOT operator in query builder popup

    And user of browser clicks on 2 nd from the left add query block icon in data discovery page
    And user of browser chooses "author.keyword" property for a query in query builder popup
    And user of browser chooses "is" from comparators list in query builder popup
    And user of browser writes "John Smith" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    # year > 1970
    And user of browser clicks on 2 nd from the left add query block icon in data discovery page
    And user of browser chooses "year" property for a query in query builder popup
    And user of browser chooses ">" from comparators list in query builder popup
    And user of browser writes "1970" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup

    And user of browser clicks "Query" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_json1:
              spaceId: space_of_files_with_json_meta
              author: "\"John Doe\""
              year: 1998
            file_with_json3:
              spaceId: space_of_files_with_json_meta
              author: "\"Samantha Anderson\""
              year: 2000
