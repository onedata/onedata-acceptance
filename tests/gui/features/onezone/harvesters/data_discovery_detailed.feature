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
  Scenario: User can filter visible properties of files records
  Scenario: User can sort files records