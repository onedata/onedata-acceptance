Feature: Space API tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
        child_group:
            owner: user1
        group1:
            owner: user2
            groups:
              - child_group
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            groups:
              - group1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - file1: 11111
    And opened browser with user1 signed in to "onezone" service


  Scenario: User reads space details using the command from "Get space details" from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "Get space details" from "REST API" modal
    And user of browser executes copied command
    Then user1 sees that output of executed command contains:
      advertisedInMarketplace: false
      name: space1


  Scenario: User reads space privileges using the command from "List all space privileges" from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List all space privileges" from "REST API" modal
    And user of browser executes copied command
    Then user1 sees that output of executed command contains:
      member: [space_read_data,space_view,space_view_transfers,space_write_data]
      manager: [space_add_group,space_add_harvester,space_add_user,space_create_archives,
        space_manage_archives,space_manage_datasets,space_manage_shares,space_query_views,
        space_read_data,space_register_files,space_remove_group,space_remove_harvester,
        space_remove_user,space_schedule_atm_workflow_executions,space_schedule_replication,
        space_view,space_view_archives,space_view_atm_workflow_executions,
        space_view_changes_stream,space_view_privileges,space_view_qos,space_view_statistics,
        space_view_transfers,space_view_views,space_write_data]
      admin: [space_add_group,space_add_harvester,space_add_support,space_add_user,
        space_cancel_eviction,space_cancel_replication,space_create_archives,space_delete,
        space_manage_archives,space_manage_atm_workflow_executions,space_manage_datasets,
        space_manage_in_marketplace,space_manage_qos,space_manage_shares,space_manage_views,
        space_query_views,space_read_data,space_recall_archives,space_register_files,space_remove_archives,
        space_remove_group,space_remove_harvester,space_remove_support,space_remove_user,
        space_schedule_atm_workflow_executions,space_schedule_eviction,space_schedule_replication,
        space_set_privileges,space_update,space_view,space_view_archives,space_view_atm_workflow_executions,
        space_view_changes_stream,space_view_privileges,space_view_qos,space_view_statistics,space_view_transfers,
        space_view_views,space_write_data]


  Scenario: User reads direct space users using the command from "List direct space users" from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List direct space users" from "REST API" modal
    And user of browser executes copied command
    Then user1 sees that output of executed command contains:
      users: [$(resolve_user_id user1)]


  Scenario: User reads effective space users using the command from "List effective space users" from REST API modal
    When using REST, user1 creates token with following configuration:
        name: access token
        type: access
        caveats:
          interface: REST
    And user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List effective space users" from "REST API" modal
    And user of browser executes copied command
    Then user1 sees that output of executed command contains:
      users: [$(resolve_user_id user1), $(resolve_user_id user2)]


  Scenario: User reads effective space user details of user1 using the command from "Get effective space user details" from REST API modal
    When using REST, user1 creates token with following configuration:
        name: access token
        type: access
        caveats:
          interface: REST
    And user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "Get effective space user details" from "REST API" modal
    And user of browser executes copied command with env variable "USER_ID" with value of "user1"
    Then user1 sees that output of executed command contains:
      username: user1
      userId: $(resolve_user_id user1)
      name: user1
      login: user1
      fullName: user1
      alias: user1


  Scenario: User reads user1 direct space privileges using the command from "List user's direct space privileges" from REST API modal
    When using REST, user1 creates token with following configuration:
        name: access token
        type: access
        caveats:
          interface: REST
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List user's direct space privileges" from "REST API" modal
    And user of browser executes copied command with env variable "USER_ID" with value of "user1"
    Then user1 sees that output of executed command contains:
      privileges: [space_add_group,space_add_harvester,space_add_support,space_add_user,
        space_cancel_eviction,space_cancel_replication,space_create_archives,space_delete,space_manage_archives,
        space_manage_atm_workflow_executions,space_manage_datasets,space_manage_in_marketplace,space_manage_qos,
        space_manage_shares,space_manage_views,space_query_views,space_read_data,space_recall_archives,
        space_register_files,space_remove_archives,space_remove_group,space_remove_harvester,space_remove_support,
        space_remove_user,space_schedule_atm_workflow_executions,space_schedule_eviction,space_schedule_replication,
        space_set_privileges,space_update,space_view,space_view_archives,space_view_atm_workflow_executions,
        space_view_changes_stream,space_view_privileges,space_view_qos,space_view_statistics,space_view_transfers,
        space_view_views,space_write_data]



  Scenario: User reads user1 effective space privileges using the command from "List user's effective space privileges" from REST API modal
    When using REST, user1 creates token with following configuration:
        name: access token
        type: access
        caveats:
          interface: REST
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List user's effective space privileges" from "REST API" modal
    And user of browser executes copied command with env variable "USER_ID" with value of "user1"
    Then user1 sees that output of executed command contains:
      privileges: [space_add_group,space_add_harvester,space_add_support,space_add_user,
        space_cancel_eviction,space_cancel_replication,space_create_archives,space_delete,space_manage_archives,
        space_manage_atm_workflow_executions,space_manage_datasets,space_manage_in_marketplace,space_manage_qos,
        space_manage_shares,space_manage_views,space_query_views,space_read_data,space_recall_archives,
        space_register_files,space_remove_archives,space_remove_group,space_remove_harvester,space_remove_support,
        space_remove_user,space_schedule_atm_workflow_executions,space_schedule_eviction,space_schedule_replication,
        space_set_privileges,space_update,space_view,space_view_archives,space_view_atm_workflow_executions,
        space_view_changes_stream,space_view_privileges,space_view_qos,space_view_statistics,space_view_transfers,
        space_view_views,space_write_data]


  Scenario: User reads direct space groups using the command from "List direct space groups" from REST API modal
    When using REST, user1 creates token with following configuration:
        name: access token
        type: access
        caveats:
          interface: REST
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List direct space groups" from "REST API" modal
    And user of browser executes copied command
    Then user1 sees that output of executed command contains:
      groups: [$(resolve_group_id group1)]


  Scenario: User reads effective space groups using the command from "List effective space groups" from REST API modal
    When using REST, user1 creates token with following configuration:
        name: access token
        type: access
        caveats:
          interface: REST
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List effective space groups" from "REST API" modal
    And user of browser executes copied command
    Then user1 sees that output of executed command contains:
      groups: [$(resolve_group_id group1), $(resolve_group_id child_group)]


  Scenario: User reads effective space group details of group1 using the command from "Get effective space group details" from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "Get effective space group details" from "REST API" modal
    And user of browser executes copied command with env variable "GROUP_ID" with value of "group1"
    Then user1 sees that output of executed command contains:
      type: team
      name: group1


  Scenario: User reads group1 direct space privileges using the command from "List group's direct space privileges" from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List group's direct space privileges" from "REST API" modal
    And user of browser executes copied command with env variable "GROUP_ID" with value of "group1"
    Then user1 sees that output of executed command contains:
      privileges: [space_read_data,space_view,space_view_transfers,space_write_data]


  Scenario: User reads group1 effective space privileges using the command from "List group's effective space privileges" from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List group's effective space privileges" from "REST API" modal
    And user of browser executes copied command with env variable "GROUP_ID" with value of "group1"
    Then user1 sees that output of executed command contains:
      privileges: [space_read_data,space_view,space_view_transfers,space_write_data]


  Scenario: User reads space shares using the command from "List space shares" from REST API modal
    Given using REST, user user1 creates "share_file1" share of "space1/file1" supported by "oneprovider-1" provider
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List space shares" from "REST API" modal
    And user of browser executes copied command
    Then user1 sees that output of executed command contains:
      shares: [$(resolve_share_id share_file1)]
