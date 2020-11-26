Feature: Querying for data discovery in Discovery Page in Onezone GUI

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
    And spaces ["space1", "space2", "space3"] belong to "harvester1" harvester of user admin
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario: Metadata keys are harvested when default index is set in GUI plugin
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester1" on the harvesters list in the sidebar
    And user of browser clicks Indices of "harvester1" harvester in the sidebar
    And user of browser sees "Used by GUI" tag on "generic-index" index record in indices page
    And user of browser expands "generic-index" index record in indices page
    And user of browser sees that generic-index index finished harvesting process for all spaces

    And user of browser opens Data Discovery page of "harvester1" harvester

    And user of browser clicks on start query icon in data discovery page
    And user of browser opens condition properties list
    Then user of browser sees ["author", "year"] on condition properties list














#  Scenario: User sees appropriate files after searching by xattr metadata values















#  Scenario: User sees appropriate files after searching by JSON metadata values
#  Scenario: User sees appropriate files after searching using OR
#  Scenario: User sees appropriate files after searching using AND
#  Scenario: User sees appropriate files after searching using NOT
#  Scenario: User sees appropriate files after searching with complex expression
#
#
































