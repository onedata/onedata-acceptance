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
                    size: 10000000000
            storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - dir1
                - file1: 100
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: user1
    And opened browser with user1 signed in to "onezone" service


  Scenario: User sees successful execution of all workflows from automation-examples with its example input files
    When using REST, user1 uploads all workflows from automation-examples to inventory "inventory1" in "onezone" Onezone service
    And using REST, user1 executes all workflows with example input files on space "space1" in oneprovider-1
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    Then using REST, user1 sees successful execution of all workflows on space "space1" in oneprovider-1
