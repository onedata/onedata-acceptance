Feature: Querying for data discovery in Discovery Page in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And admin user does not have access to any space
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
                      - file0:
                          content: 11111
                          metadata:
                            type: basic
                            author: John Smith
                            year: 2020
                      - file1_1:
                          content: 11111
                          metadata:
                            type: basic
                            author: John Smith
                            year: 2019
                      - file2_1:
                          content: 11111
                          metadata:
                            type: json
                            author: John Kowalski
                            year: 2019
                      - file3_1:
                          content: 11111
                          metadata:
                            type: basic
                            author: Samantha Anderson
                            year: 1998
                      - file4_1:
                          content: 11111
                          metadata:
                            type: json
                            author: Samantha Anderson
                            year: 1998
                      - dir_inner
                    - loose_file_1: 1111
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
                      - file0:
                          content: 11111
                          metadata:
                            type: basic
                            author: John Smith
                            year: 2020
                      - file1_2:
                          content: 11111
                          metadata:
                            type: basic
                            author: John Smith
                            year: 2019
                      - file2_2:
                          content: 11111
                          metadata:
                            type: json
                            author: John Kowalski
                            year: 2019
                      - file3_2:
                          content: 11111
                          metadata:
                            type: basic
                            author: Samantha Anderson
                            year: 1998
                      - file4_2:
                          content: 11111
                          metadata:
                            type: json
                            author: Samantha Anderson
                            year: 1998
                      - dir_inner
                    - loose_file_2: 1111
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
                        - file1_3:
                            content: 11111
                            metadata:
                              type: json
                              author: Samantha Anderson
                              year: 1998


    And user admin has no harvesters
    And user admin has "harvester1" harvester in "onezone" Onezone service
    And space "space1" belongs to "harvester1" harvester of user admin
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service

  Scenario: Files of supported spaces are visible in Data discovery page
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester1" on the harvesters list in the sidebar
    And user of browser clicks Data discovery of "harvester1" harvester in the sidebar
    And user of browser sees Data Discovery page

    And user of browser sees following files in Data discovery page:
          - filename: "file1_3"
              json_metadata_exists: true,
              spaceId: id of "space3"