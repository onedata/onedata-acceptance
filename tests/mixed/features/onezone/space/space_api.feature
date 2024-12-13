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
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
    Then user1 sees that output of executed command contains:
      advertisedInMarketplace: false
      name: space1


  Scenario: User reads space privileges using the command from "List all space privileges" from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List all space privileges" from "REST API" modal
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
    Then user1 sees that output of executed command contains:
      member: <space_member_privileges>
      manager: <space_manager_privileges>
      admin: <space_owner_privileges>


  Scenario: User reads direct space users using the command from "List direct space users" from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List direct space users" from "REST API" modal
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
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
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
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
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
      USER_ID: $(resolve_user_id user1)
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
    And user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List user's direct space privileges" from "REST API" modal
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
      USER_ID: $(resolve_user_id user1)
    Then user1 sees that output of executed command contains:
      privileges: <space_owner_privileges>



  Scenario: User reads user1 effective space privileges using the command from "List user's effective space privileges" from REST API modal
    When using REST, user1 creates token with following configuration:
        name: access token
        type: access
        caveats:
          interface: REST
    And user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List user's effective space privileges" from "REST API" modal
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
      USER_ID: $(resolve_user_id user1)
    Then user1 sees that output of executed command contains:
      privileges: <space_owner_privileges>


  Scenario: User reads direct space groups using the command from "List direct space groups" from REST API modal
    When using REST, user1 creates token with following configuration:
        name: access token
        type: access
        caveats:
          interface: REST
    And user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List direct space groups" from "REST API" modal
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
    Then user1 sees that output of executed command contains:
      groups: [$(resolve_group_id group1)]


  Scenario: User reads effective space groups using the command from "List effective space groups" from REST API modal
    When using REST, user1 creates token with following configuration:
        name: access token
        type: access
        caveats:
          interface: REST
    And user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List effective space groups" from "REST API" modal
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
    Then user1 sees that output of executed command contains:
      groups: [$(resolve_group_id group1), $(resolve_group_id child_group)]


  Scenario: User reads effective space group details of group1 using the command from "Get effective space group details" from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "Get effective space group details" from "REST API" modal
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
      GROUP_ID: $(resolve_group_id group1)
    Then user1 sees that output of executed command contains:
      type: team
      name: group1


  Scenario Outline: User reads group1 <priv_type> space privileges using the command from <command> from REST API modal
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command <command> from "REST API" modal
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
      GROUP_ID: $(resolve_group_id group1)
    Then user1 sees that output of executed command contains:
      privileges: [space_read_data,space_view,space_view_transfers,space_write_data]

    Examples:
    | priv_type | command                                   |
    | direct    | "List group's direct space privileges"    |
    | effective | "List group's effective space privileges" |


  Scenario: User reads space shares using the command from "List space shares" from REST API modal
    Given using REST, user user1 creates "share_file1" share of "space1/file1" supported by "oneprovider-1" provider
    When user of browser copies token "access token" from tokens page
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "REST API" button in space "space1" menu
    And user of browser copies command "List space shares" from "REST API" modal
    And user of browser executes copied command with env variables:
      TOKEN: $(resolve_token "access token")
    Then user1 sees that output of executed command contains:
      shares: [$(resolve_share_id share_file1)]
