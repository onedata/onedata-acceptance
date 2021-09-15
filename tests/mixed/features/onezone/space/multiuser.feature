Feature: Multiuser
  Multiuser operations on spaces in Onezone using GUI and REST API

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - user3
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user2
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And opened browsers with [user1, user2] signed in to [onezone, onezone] service

  Scenario Outline: User invites other user to space using <client1>, that user joins to space using <client2> and using <client3> he sees that he has joined to new space
    When using <client1>, user2 invites user1 to space named "space1" in "onezone" Onezone service
    And using <client2>, user1 joins to space using received space invitation token in "onezone" Onezone service
    Then using <client3>, user1 sees that space named "space1" has appeared in "onezone" Onezone service
    And using <client1>, user2 sees that user1 is member of "space1" in "onezone" Onezone service


  Examples:
  | client1 | client2   | client3   |
  | web GUI | web GUI   | REST      |
  | REST    | REST      | web GUI   |
  | web GUI | REST      | REST      |
  | REST    | web GUI   | web GUI   |


  Scenario Outline: User invites other user to space using <client1>, that user joins using <client2> and fails to set privileges because of lack in privileges
    When using <client1>, user2 invites user1 to space named "space1" in "onezone" Onezone service
    And using <client2>, user1 joins to space using received space invitation token in "onezone" Onezone service
    And using <client2>, user1 fails to set following privileges for "user1" user in space "space1" in "onezone" Onezone service:
          User management:
            granted: True
          Harvester management:
            granted: False
          Dataset & archive management:
            granted: Partially
            privilege subtypes:
              Manage datasets: True
              View archives: False
    Then using <client1>, user2 sees following privileges of "user1" user in space "space1" in "onezone" Onezone service:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: True
              Modify space: False
              Remove space: False
              View privileges: False
              Set privileges: False
          Data management:
            granted: Partially
            privilege subtypes:
              Read files: True
              Write files: True
              Register files: False
              Manage shares: False
              View database views: False
              Manage database views: False
              Query database views: False
              View statistics: False
              View changes stream: False
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Schedule replication: False
              Cancel replication: False
              Schedule eviction: False
              Cancel eviction: False
          QoS management:
            granted: False
          User management:
            granted: False
          Group management:
            granted: False
          Support management:
            granted: False
          Harvester management:
            granted: False
          Dataset & archive management:
            granted: False
          Automation management:
            granted: False
  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |


  Scenario Outline: User invites other user to space using <client1>, that user joins using <client2> and fails to add another user to space because of lack in privileges
    When using <client1>, user2 invites user1 to space named "space1" in "onezone" Onezone service
    And using <client2>, user1 joins to space using received space invitation token in "onezone" Onezone service
    And using <client2>, user1 fails to invite "user3" to "space1" space members page in "onezone" Onezone service
    Then using <client1>, user2 does not see "user3" on "space1" space members page in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |