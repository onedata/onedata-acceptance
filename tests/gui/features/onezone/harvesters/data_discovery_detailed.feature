Feature: Testing features in Discovery Page in Onezone GUI

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
                    - dir1_1:
                      - file_xattrs:
                          content: 11111
                          metadata:
                            type: basic
                            author: John Smith
                            year: 2020
          space2:
            owner: admin
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1_2:
                        - file_json:
                            content: 11111
                            metadata:
                              type: json
                              author: Samantha Anderson
                              year: 1998
          space3:
            owner: admin
            providers:
              - oneprovider-1:
                  storage: posix
                  size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1_3:
                        - file1_3
                        - file2_3
                        - file3_3


    And user admin has no harvesters other than defined in next steps
    And user admin has "harvester1" harvester in "onezone" Onezone service
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario: Files records are paged for as many is given
    When user of browser checks if harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    And user of browser sees that paging is set for 10 pages
    Then user of browser sees 10 files on data discovery page
    And user opens next page of data discovery page
    And user of browser sees 2 files on data discovery page


  Scenario: User can filter visible properties of files records
    When user of browser checks if harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester

    # author contains "John"
    And user of browser clicks on start query icon in data discovery page
    And user of browser chooses "any property" property for a query in query builder popup
    And user of browser chooses "has phrase" from comparators list in query builder popup
    And user of browser writes "John Smith" to value input in query builder popup
    And user of browser clicks "Add" button in query builder popup
    And user of browser clicks "Query" button on data discovery page

    And user of browser clicks on "Filter properties" button on data discovery page
    And user of browser chooses following properties to filter on data discovery page:
          __onedata:
            fileName
            xattrs:
              author
          author

    And user of browser clicks on "Filter properties" button on data discovery page
    Then user of browser sees only following files in data discovery page:
            file_with_json4:
              spaceId: space_of_files_with_json_meta
              author: "\"John Smith\""
              unexpected:
                year: 1998
            file_with_xattrs4:
              spaceId: space_of_files_with_xattrs
              xattrs:
                author: "\"John Smith\""
                unexpected:
                  year: 1998


  Scenario: User can sort files records
    When user of browser checks if harvesting process in "harvester1" is finished for all spaces in "generic-index"
    And user of browser opens Data Discovery page of "harvester1" harvester
    #TODO: todo.





















