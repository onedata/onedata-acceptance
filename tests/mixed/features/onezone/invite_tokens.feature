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



#  Scenario: User successfully consumes group to space invite token with consumer caveat set for them
#    When user of browser1 creates and checks token with following configuration:
#          type: invite
#          invite type: Invite group to space
#          invite target: space1
#          usage limit: infinity
#          privileges:
#            Space management:
#              granted: Partially
#              privilege subtypes:
#                View space: True
#                Remove space: False
#                View privileges: True
#            Transfer management:
#              granted: False
#          caveats:
#            consumer:
#              - type: user
#                by: id
#                consumer name: user1
#    And user of browser1 clicks on copy button in token view
#    And user of browser1 sends copied token to user of browser2
#
#    # consume invite token
#    And user of browser2 clicks on Tokens in the main menu
#    And user of browser2 clicks on "Consume token" button in tokens sidebar
#    And user of browser2 pastes received token into token text field
#    And user of browser2 chooses "group1" group from dropdown on tokens page
#    And user of browser2 clicks on Join button on consume token page
#    Then user of browser2 sees an success notify with text matching to: .*joined.*
#    And user of browser2 sees that "space1" has appeared on the spaces list in the sidebar
#    And user of browser2 sees that space space1 has following privilege configuration for group group1:
#          privileges:
#            Space management:
#              granted: Partially
#              privilege subtypes:
#                View space: True
#                Remove space: False
#                View privileges: True
#            User management:
#              granted: False
#
#    And user of browser1 removes all tokens
#
#
#  Scenario: User fails to consume group to space invite token with consumer caveat set not for them
#    When user of browser1 creates and checks token with following configuration:
#          type: invite
#          invite type: Invite group to space
#          invite target: space1
#          usage limit: infinity
#          caveats:
#            consumer:
#              - type: user
#                by: id
#                consumer name: user2
#    And user of browser1 clicks on copy button in token view
#    And user of browser1 sends copied token to user of browser2
#
#    # consume invite token
#    And user of browser2 clicks on Tokens in the main menu
#    And user of browser2 clicks on "Consume token" button in tokens sidebar
#    And user of browser2 pastes received token into token text field
#    And user of browser2 chooses "group1" group from dropdown on tokens page
#    And user of browser2 clicks on Join button on consume token page
#    Then user of browser2 sees that error modal with text "Consuming token failed" appeared
#
#    And user of browser1 removes all tokens
#
#
#  Scenario: User successfully consumes group to space invite token with consumer caveat set for Any user
#    When user of browser1 creates and checks token with following configuration:
#          type: invite
#          invite type: Invite group to space
#          invite target: space1
#          caveats:
#            consumer:
#              - type: user
#                by: name
#                consumer name: Any user
#    And user of browser1 clicks on copy button in token view
#    And user of browser1 sends copied token to user of browser2
#    Then user of browser2 succeeds to consume token for "group1" group
#
#    And user of browser1 removes all tokens


  Scenario: User has default space member privileges after consuming user to space invite token
    When using REST, user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
#    And user of browser1 sees that created token configuration is as following:
#          type: invite
#          invite type: Invite group to space
#          invite target: space1
#          usage count: 0/infinity
#          privileges:
#            Space management:
#              granted: Partially
#              privilege subtypes:
#                View space: True
#                Modify space: False
#                Remove space: False
#                View privileges: False
#                Set privileges: False
#            Data management:
#              granted: Partially
#              privilege subtypes:
#                Read files: True
#                Write files: True
#                Manage shares: False
#                View database views: False
#                Manage database views: False
#                Query database views: False
#                View statistics: False
#                View changes stream: False
#            Transfer management:
#              granted: Partially
#              privilege subtypes:
#                View transfers: True
#                Schedule replication: False
#                Cancel replication: False
#                Schedule eviction: False
#                Cancel eviction: False
#            QoS management:
#              granted: False
#            User management:
#              granted: False
#            Group management:
#              granted: False
#            Support management:
#              granted: False
#            Harvester management:
#              granted: False
#    And user of browser1 clicks on copy button in token view
#    And user of browser1 sends copied token to user of browser2
#
#    # consume invite token
#    And user of browser2 succeeds to consume token for "group1" group
#    And user of browser2 sees that "space1" has appeared on the spaces list in the sidebar
#
#    Then user of browser1 sees that space space1 has following privilege configuration for group group1:
#          privileges:
#            Space management:
#              granted: Partially
#              privilege subtypes:
#                View space: True
#                Modify space: False
#                Remove space: False
#                View privileges: False
#                Set privileges: False
#            Data management:
#              granted: Partially
#              privilege subtypes:
#                Read files: True
#                Write files: True
#                Manage shares: False
#                View database views: False
#                Manage database views: False
#                Query database views: False
#                View statistics: False
#                View changes stream: False
#            Transfer management:
#              granted: Partially
#              privilege subtypes:
#                View transfers: True
#                Schedule replication: False
#                Cancel replication: False
#                Schedule eviction: False
#                Cancel eviction: False
#            QoS management:
#              granted: False
#            User management:
#              granted: False
#            Group management:
#              granted: False
#            Support management:
#              granted: False
#            Harvester management:
#              granted: False
#
#    And user of browser1 removes all tokens
