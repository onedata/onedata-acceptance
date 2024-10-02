Feature: Automation tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
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


  Scenario: User can see correct workflow execution details using REST
    Given there is "echo" workflow dump uploaded from automation examples by user user1 in inventory "inventory1" in "onezone" Onezone service
    When using REST, user1 executes "echo" workflow on space "space1" in oneprovider-1 with following configuration:
        input: [{fileId: $(resolve_file_id space1/file1)}]
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    Then using REST, user1 sees successful execution of all workflows in oneprovider-1
    And using REST, user1 sees following "echo" workflow execution details in oneprovider-1:
        userId: $(resolve_user_id user1)
        atmInventoryId: $(resolve_inventory_id inventory1)


  Scenario: User can pause and resume workflow execution using REST
    Given there is "echo" workflow dump uploaded from automation examples by user user1 in inventory "inventory1" in "onezone" Onezone service
    When using REST, user1 executes "echo" workflow on space "space1" in oneprovider-1 with following configuration:
        input: [{fileId: $(resolve_file_id space1/file1)}]
    And using REST, user1 pauses execution of "echo" workflow in oneprovider-1
    Then using REST, user1 resumes execution of "echo" workflow in oneprovider-1
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    And using REST, user1 sees successful execution of all workflows in oneprovider-1


  Scenario: User fails to resume cancelled workflow execution using REST
    Given there is "echo" workflow dump uploaded from automation examples by user user1 in inventory "inventory1" in "onezone" Onezone service
    When using REST, user1 executes "echo" workflow on space "space1" in oneprovider-1 with following configuration:
        input: [{fileId: $(resolve_file_id space1/file1)}]
    And using REST, user1 cancels execution of "echo" workflow in oneprovider-1
    Then using REST, user1 fails to resume execution of "echo" workflow in oneprovider-1


    Scenario: User fails to resume deleted workflow execution using REST
    Given there is "echo" workflow dump uploaded from automation examples by user user1 in inventory "inventory1" in "onezone" Onezone service
    When using REST, user1 executes "echo" workflow on space "space1" in oneprovider-1 with following configuration:
        input: [{fileId: $(resolve_file_id space1/file1)}]
    And using REST, user1 pauses execution of "echo" workflow in oneprovider-1
    And using REST, user1 deletes execution of "echo" workflow in oneprovider-1
    Then using REST, user1 fails to resume execution of "echo" workflow in oneprovider-1


  Scenario: User forces continue failed workflow execution using REST
    Given there is "workflow-with-sleep-failing" workflow dump uploaded by user user1 in inventory "inventory1" in "onezone" Onezone service
    When using REST, user1 executes "workflow-with-sleep-failing" workflow on space "space1" in oneprovider-1 with following configuration:
        input: [{fileId: $(resolve_file_id space1/file1)}]
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    Then using REST, user1 forces continue execution of "workflow-with-sleep-failing" workflow in oneprovider-1
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    And using REST, user1 sees successful execution of all workflows in oneprovider-1


  Scenario: User reruns failed workflow execution using REST
    Given there is "workflow-with-sleep-failing" workflow dump uploaded by user user1 in inventory "inventory1" in "onezone" Onezone service
    When using REST, user1 executes "workflow-with-sleep-failing" workflow on space "space1" in oneprovider-1 with following configuration:
        input: [{fileId: $(resolve_file_id space1/file1)}]
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    Then using REST, user1 reruns execution of "workflow-with-sleep-failing" workflow from lane run 1, lane index 1 in oneprovider-1
    And using REST, user1 sees there is 1 workflow execution in phase "ongoing" on space "space1" in oneprovider-1
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    And using REST, user1 sees there is 1 workflow execution of status "failed" on space "space1" in oneprovider-1
