Feature: Management of invite tokens in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1
          - user2
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1

    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user2

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario: Group has default space member privileges after user consumes group to space invite token with default settings
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
    And user of browser1 sees that created token configuration is as following:
          type: invite
          invite type: Invite group to space
          invite target: space1
          usage count: 0/infinity
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
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    # consume invite token
    And user of browser2 succeeds to consume token for "group2" group
    And user of browser2 sees that "space1" has appeared on the spaces list in the sidebar

    Then user of browser1 sees that space space1 has following privilege configuration for group group2:
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


  Scenario: User has default group member privileges after consuming user to group invite token with default settings
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite user to group
          invite target: group1
    And user of browser1 sees that created token configuration is as following:
          invite type: Invite user to group
          invite target: group1
          privileges:
            Group management:
              granted: Partially
              privilege subtypes:
                View group: True
                Modify group: False
                View privileges: False
                Set privileges: False
                Remove group: False
            Group hierarchy management:
                granted: False
            User management:
                granted: False
            Space management:
                granted: False
            Handle management:
                granted: False
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    # consume invite token
    And user of browser2 succeeds to consume token
    And user of browser2 sees group "group2" on groups list
    And trace

    Then user of browser1 sees that group group1 has following privilege configuration for user user2:
          privileges:
            Group management:
              granted: Partially
              privilege subtypes:
                View group: True
                Modify group: False
                View privileges: False
                Set privileges: False
                Remove group: False
            Group hierarchy management:
                granted: False
            User management:
                granted: False
            Space management:
                granted: False
            Handle management:
                granted: False
