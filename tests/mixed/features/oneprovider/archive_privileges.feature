Feature: Archives privileges mixed tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
        space1:
          owner: user1
          providers:
            - oneprovider-1:
                storage: posix
                size: 1000000
          storage:
            defaults:
              provider: oneprovider-1
            directory tree:
              - dir1:
                - dir2:
                  - dir4
                  - file1
                - dir3

    And opened [browser1, browser2] with [user1, user2] signed in to ["onezone", "onezone"] service


  Scenario Outline: User of <client_checking> sees archive after getting invite token with view archives privilege from user of <client_inviting>
    When using <client_inviting>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_inviting>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_inviting>, user1 creates token with following configuration:
        name: invite token
        type: invite
        invite type: Invite user to space
        invite target: space1
        privileges:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              View archives: True
    And if <client_inviting> is web GUI, user1 copies created token
    And user1 sends token to user2
    And using <client_checking>, user2 successfully joins space space1 with received token
    Then using <client_checking>, user2 sees archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_inviting    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_creating> cannot create archive after getting invite token without create archives privilege from user of <client_inviting>
    When using <client_inviting>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_inviting>, user1 creates token with following configuration:
        name: invite token
        type: invite
        invite type: Invite user to space
        invite target: space1
        privileges:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              View archives: True
    And if <client_inviting> is web GUI, user1 copies created token
    And user1 sends token to user2
    And using <client_creating>, user2 successfully joins space space1 with received token
    Then using <client_creating>, user2 fails to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_inviting>, user1 does not see archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_inviting    | client_creating    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_creating> can create archive after getting invite token with create archives privilege from user of <client_inviting>
    When using <client_inviting>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_inviting>, user1 creates token with following configuration:
        name: invite token
        type: invite
        invite type: Invite user to space
        invite target: space1
        privileges:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: True
              Create archives: True
              View archives: True
    And if <client_inviting> is web GUI, user1 copies created token
    And user1 sends token to user2
    And using <client_creating>, user2 successfully joins space space1 with received token
    Then using <client_creating>, user2 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_inviting>, user1 sees archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_inviting    | client_creating    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_removing> cannot remove archive after getting invite token without remove archives privilege from user of <client_inviting>
    When using <client_inviting>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_inviting>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_inviting>, user1 creates token with following configuration:
        name: invite token
        type: invite
        invite type: Invite user to space
        invite target: space1
        privileges:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
               Manage datasets: True
               Create archives: True
               View archives: True
    And if <client_inviting> is web GUI, user1 copies created token
    And user1 sends token to user2
    And using <client_removing>, user2 successfully joins space space1 with received token
    Then using <client_removing>, user2 fails to remove archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1
    And using <client_inviting>, user1 sees archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_removing    | client_inviting    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_removing> removes archive after getting invite token with remove archives privilege from user of <client_inviting>
    When using <client_inviting>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_inviting>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_inviting>, user1 creates token with following configuration:
        name: invite token
        type: invite
        invite type: Invite user to space
        invite target: space1
        privileges:
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
               Manage datasets: True
               Remove archives: True
               View archives: True
    And if <client_inviting> is web GUI, user1 copies created token
    And user1 sends token to user2
    And using <client_removing>, user2 successfully joins space space1 with received token
    Then using <client_removing>, user2 succeeds to remove archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1
    And using <client_inviting>, user1 does not see archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_removing    | client_inviting    |
  | REST               | web GUI            |
  | web GUI            | REST               |
