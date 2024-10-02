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
                - file1: 100
                - file2: 100
                - file3: 100
                - file4: 100
                - file5: 100
                - file6: 100
                - file7: 100
                - file8: 100
                - file9: 100
                - file10: 100

    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: user1
    And opened browser with user1 signed in to "onezone" service


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
    Given there is "workflow-with-sleep-100-failing" workflow dump uploaded by user user1 in inventory "inventory1" in "onezone" Onezone service
    When using REST, user1 executes "workflow-with-sleep-100-failing" workflow on space "space1" in oneprovider-1 with following configuration:
        input: [{fileId: $(resolve_file_id space1/file1)}]
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    Then using REST, user1 forces continue execution of "workflow-with-sleep-100-failing" workflow in oneprovider-1
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    And using REST, user1 sees successful execution of all workflows in oneprovider-1


  Scenario: User reruns failed workflow execution using REST
    Given there is "workflow-with-sleep-100-failing" workflow dump uploaded by user user1 in inventory "inventory1" in "onezone" Onezone service
    When using REST, user1 executes "workflow-with-sleep-100-failing" workflow on space "space1" in oneprovider-1 with following configuration:
        input: [{fileId: $(resolve_file_id space1/file1)}]
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    Then using REST, user1 reruns execution of "workflow-with-sleep-100-failing" workflow from lane run 1, lane index 1 in oneprovider-1
    And using REST, user1 sees there is 1 workflow execution in phase "ongoing" on space "space1" in oneprovider-1
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    And using REST, user1 sees there is 1 workflow execution of status "failed" on space "space1" in oneprovider-1


  Scenario: User retries failed workflow execution and can see that exceptionStoreId is the same as iteratedStoreId after retry using REST
    Given there is "workflow-with-sleep-50-failing" workflow dump uploaded by user user1 in inventory "inventory1" in "onezone" Onezone service
    When using REST, user1 executes "workflow-with-sleep-50-failing" workflow on space "space1" in oneprovider-1 with following configuration:
        input: [{fileId: $(resolve_file_id space1/file1)}, {fileId: $(resolve_file_id space1/file2)}, {fileId: $(resolve_file_id space1/file3)},
                {fileId: $(resolve_file_id space1/file4)}, {fileId: $(resolve_file_id space1/file5)}, {fileId: $(resolve_file_id space1/file6)},
                {fileId: $(resolve_file_id space1/file7)}, {fileId: $(resolve_file_id space1/file8)}, {fileId: $(resolve_file_id space1/file9)},
                {fileId: $(resolve_file_id space1/file10)}]
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    And using REST, user1 saves "workflow-with-sleep-50-failing" workflow execution details in oneprovider-1
    Then using REST, user1 retries execution of "workflow-with-sleep-50-failing" workflow from lane run 1, lane index 1 in oneprovider-1
    And using REST, user1 waits for all workflow executions to finish on space "space1" in oneprovider-1
    And using REST, user1 sees that iteratedStoreId is the same as the exceptionStoreId from previous run in "workflow-with-sleep-50-failing" workflow execution details in oneprovider-1

