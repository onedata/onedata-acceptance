Feature: Datasets mixed tests

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
              - dir1
              - dir2:
                  - dir3:
                    - dir4:
                      - dir5
                    - file1: 150

    And opened [browser1, browser2] with [user1, user2] signed in to ["onezone", "onezone"] service


  Scenario Outline: User of <client_checking> sees dataset created previously via <client_creating>
    When using <client_creating>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client_checking>, user1 sees dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> does not see dataset removed previously via <client_removing>
    When using <client_checking>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_removing>, user1 sees dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client_removing>, user1 removes dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_checking>, user1 does not see dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_checking    | client_removing    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> sees dataset with write protection flags created previously via <client_creating>
    When using <client_creating>, user1 creates dataset with data and metadata write protection flags for item "dir1" in space "space1" in oneprovider-1
    And using <client_checking>, user1 sees dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client_checking>, user1 sees data and metadata write protection flags for dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> sees datasets directory tree created previously via <client_creating>
    When using <client_creating>, user1 creates dataset for item "dir2" in space "space1" in oneprovider-1
    And using <client_creating>, user1 creates dataset for item "dir2/dir3/dir4" in space "space1" in oneprovider-1
    And using <client_creating>, user1 creates dataset for item "dir2/dir3/file1" in space "space1" in oneprovider-1
    And using <client_creating>, user1 creates dataset for item "dir2/dir3/dir4/dir5" in space "space1" in oneprovider-1
    Then using <client_checking>, user1 sees that datasets structure in space "space1" in oneprovider-1 is as follow:
         - dir2:
           - dir4:
             - dir5
           - file1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> sees that directory has effective protection flags from its parents after user of  <client_creating> marks directories as dataset with protection flags
    When using <client_creating>, user1 creates dataset with metadata write protection flags for item "dir2" in space "space1" in oneprovider-1
    And using <client_creating>, user1 creates dataset with data write protection flags for item "dir2/dir3" in space "space1" in oneprovider-1
    Then using <client_checking>, user1 sees that item "dir2/dir3/dir4/dir5" has effective data and metadata write protection flags in space "space1" in oneprovider-1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> sees protection flags set via <client_setting> for datasets created previously via <client_checking>
    When using <client_checking>, user1 creates dataset for item "dir2" in space "space1" in oneprovider-1
    And using <client_checking>, user1 creates dataset for item "dir2/dir3" in space "space1" in oneprovider-1
    And using <client_checking>, user1 creates dataset for item "dir2/dir3/file1" in space "space1" in oneprovider-1
    And using <client_setting>, user1 sets data protection flag for dataset "dir2" in space "space1" in oneprovider-1
    And using <client_setting>, user1 sets metadata protection flags for dataset "dir2/dir3" in space "space1" in oneprovider-1
    Then using <client_checking>, user1 sees that dataset "dir2/dir3/file1" has effective data and metadata write protection flags in space "space1" in oneprovider-1

  Examples:
  | client_checking    | client_setting     |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> sees dataset in detached view mode after user of <client_detaching> detached dataset
    When using <client_checking>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_detaching>, user1 detaches dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client_checking>, user1 sees that dataset for item "dir1" is detached in space "space1" in oneprovider-1

  Examples:
  | client_checking    | client_detaching   |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_detaching> sees dataset in attached view mode reattached via <client_reattaching> detached previously via <client_detaching>
    When using <client_reattaching>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_detaching>, user1 detaches dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_reattaching>, user1 reattaches dataset for item "dir1" in space "space1" in oneprovider-1
    Then using <client_detaching>, user1 sees dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_detaching   | client_reattaching |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_creating> creates dataset after getting invite token with manage dataset privilege from user of <client_inviting>
    When using <client_inviting>, user1 creates token with following configuration:
          name: invite token
          type: invite
          invite type: Invite user to space
          invite target: space1
          privileges:
            Dataset & archive management:
              granted: Partially
              privilege subtypes:
                Manage datasets: True
    And if <client_inviting> is web GUI, user1 copies created token
    And user1 sends token to user2
    And using <client_creating>, user2 successfully joins space space1 with received token
    Then using <client_creating>, user2 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_inviting>, user1 sees dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_inviting    | client_creating    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_creating> fails to create dataset after getting invite token from user of <client_inviting>
     When using <client_inviting>, user1 creates token with following configuration:
          name: invite token
          type: invite
          invite type: Invite user to space
          invite target: space1
    And if <client_inviting> is web GUI, user1 copies created token
    And user1 sends token to user2
    And using <client_creating>, user2 successfully joins space space1 with received token
    Then using <client_creating>, user2 fails to create dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_inviting>, user1 does not see dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_inviting    | client_creating    |
  | REST               | web GUI            |
  | web GUI            | REST               |


