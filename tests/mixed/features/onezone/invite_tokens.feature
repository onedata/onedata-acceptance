Feature: Identity tokens tests

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
    And opened [browser1, browser2] with [user1, user2] signed in to ["onezone", "onezone"] service


  Scenario Outline: User to space invite token has default space member privileges
    When using <client1>, user1 creates token with following configuration:
          name: invite token
          type: invite
          invite type: Invite user to space
          invite target: space1
          usage limit: 4
    Then using <client2>, user1 sees that created token configuration is as following:
          name: invite token
          type: Invite
          privileges:
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

    Examples:
    | client1 | client2 |
    | REST    | web gui |
    | web gui | REST    |