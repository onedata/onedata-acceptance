Feature: Workflows execution tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            groups:
                - group1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 100000000000
            storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - dir1
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: user1
    And opened browser with user1 signed in to "onezone" service


  Scenario: User sees successful execution of bagit-uploader workflow with 3 GB bagit archive
    When using REST, user1 uploads bagit-uploader workflow from automation-examples to inventory "inventory1" in "onezone" Onezone service
    And using REST, user1 executes bagit-uploader workflow with 3 gb bagit archive on space "space1" in oneprovider-1
    And using REST, user1 waits extended time for all workflow executions to finish on space "space1" in oneprovider-1
    Then using REST, user1 sees successful execution of all workflows in oneprovider-1
