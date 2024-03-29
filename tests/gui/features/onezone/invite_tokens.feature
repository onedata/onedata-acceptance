Feature: Management of invite tokens in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1
          - user2
    And admin user does not have access to any space other than defined in next steps
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: admin
          space2:
            owner: user1
          space3:
            owner: admin

    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user2
          group3:
            owner: admin
          group4:
            owner: admin

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


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
    And user of browser2 succeeds to consume token for "group1" group
    And user of browser2 sees that "space1" has appeared on the spaces list in the sidebar

    Then user of browser1 sees that space space1 has following privilege configuration for group group1:
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

    And user of browser1 removes all tokens


  Scenario: User successfully consumes harvester to space invite token until usage limit is not expired
    Given user admin has no harvesters
    And using REST, user admin creates ["harvester1", "harvester2", "harvester3"] harvesters in "onezone" Onezone service

    When user of browser2 creates token with following configuration:
          type: invite
          invite type: Invite harvester to space
          invite target: space2
          usage limit: 2
    And user of browser2 sees that token usage count is "0/2"
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1

    Then user of browser1 succeeds to consume token for "harvester1" harvester
    And user of browser2 refreshes site
    And user of browser2 sees that token usage count is "1/2"
    And user of browser1 sees that "space2" has appeared on the spaces list of "harvester1" harvester

    Then user of browser1 succeeds to consume token for "harvester2" harvester
    And user of browser2 refreshes site
    And user of browser2 sees that token usage count is "2/2"
    And user of browser1 sees that "space2" has appeared on the spaces list of "harvester1" harvester

    Then user of browser1 fails to consume token for "harvester3" harvester


  Scenario: Group has default harvester member privileges after user consumes group to harvester invite token with default settings
    Given user admin has no harvesters
    And using REST, user admin creates "harvester4" harvester in "onezone" Onezone service
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to harvester
          invite target: harvester4
    And user of browser1 sees that created token configuration is as following:
          invite type: Invite group to harvester
          invite target: harvester4
          privileges:
            Harvester management:
              granted: Partially
              privilege subtypes:
                View harvester: True
                Modify harvester: False
                View privileges: False
                Set privileges: False
            User management:
              granted: False
            Group management:
              granted: False
            Space management:
              granted: False
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    And user of browser2 succeeds to consume token for "group1" group
    And user of browser2 sees that "harvester4" has appeared on the harvesters list in the sidebar
    Then user of browser1 sees that harvester harvester4 has following privilege configuration for group group1:
          privileges:
            Harvester management:
              granted: Partially
              privilege subtypes:
                View harvester: True
                Modify harvester: False
                View privileges: False
                Set privileges: False
            User management:
              granted: False
            Group management:
              granted: False
            Space management:
              granted: False

    And user of browser1 removes all tokens


  Scenario: User successfully cleans up obsolete tokens
    Given user admin has no harvesters
    And using REST, user admin creates "harvester5" harvester in "onezone" Onezone service
    When user of browser1 removes all tokens
    And user of browser1 creates and checks token with following configuration:
          type: invite
          name: ToSurvive
          invite type: Invite user to space
          invite target: space1
          usage limit: 1
    And user of browser1 creates and checks token with following configuration:
          name: ToRemove
          type: invite
          invite type: Invite group to harvester
          invite target: harvester5
          usage limit: 1
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    And user of browser2 succeeds to consume token for "group1" group

    And user of browser1 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser1 clicks on "Clean up obsolete tokens" button in tokens sidebar
    And user of browser1 sees that "Clean up obsolete tokens" modal has appeared
    And user of browser1 clicks on "Remove" button in modal "Clean up obsolete tokens"

    Then user of browser1 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "ToSurvive" on tokens list

    And user of browser1 removes all tokens


  Scenario: User fails to consume revoked token
    Given user admin has no harvesters
    And using REST, user admin creates "harvester6" harvester in "onezone" Onezone service
    When user of browser1 creates token with following configuration:
          name: token1
          type: invite
          invite type: Invite group to harvester
          invite target: harvester6
    And user of browser1 revokes token named "token1"
    And user of browser1 sees that created token configuration is as following:
          name: token1
          invite type: Invite group to harvester
          invite target: harvester6
          revoked: True
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    Then user of browser2 sees alert with text: "Provided token has been revoked." on tokens page while trying to consume token

    And user of browser1 removes all tokens


  Scenario: User fails to consume deleted token
    Given user admin has no harvesters
    And using REST, user admin creates "harvester7" harvester in "onezone" Onezone service
    When user of browser1 creates and checks token with following configuration:
          name: token2
          type: invite
          invite type: Invite group to harvester
          invite target: harvester7
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    And user of browser1 removes token named "token2"
    Then user of browser2 sees alert with text: "This resource could not be loaded" on tokens page while trying to consume token

    And user of browser1 removes all tokens


  Scenario: User has default group member privileges after consuming user to group invite token with default settings
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite user to group
          invite target: group3
    And user of browser1 sees that created token configuration is as following:
          invite type: Invite user to group
          invite target: group3
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

    And user of browser2 succeeds to consume token
    Then user of browser2 sees that group group3 has following privilege configuration for user user1:
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

    And user of browser1 removes all tokens


  Scenario: User has default cluster member privileges after consuming user to cluster invite token with default settings
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite user to cluster
          invite target: oneprovider-1
    And user of browser1 sees that created token configuration is as following:
          invite type: Invite user to cluster
          invite target: oneprovider-1
          privileges:
            Cluster management:
              granted: Partially
              privilege subtypes:
                View cluster: True
                Modify cluster: False
                Remove cluster: False
                View privileges: False
                Set privileges: False
            User management:
                granted: False
            Group management:
                granted: False
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    And user of browser2 joins cluster using copied token
    Then user of browser2 sees "oneprovider-1" subpage in Clusters page
    And user of browser2 sees that cluster oneprovider-1 has following privilege configuration for user user1:
          privileges:
            Cluster management:
              granted: Partially
              privilege subtypes:
                View cluster: True
                Modify cluster: False
                Remove cluster: False
                View privileges: False
                Set privileges: False
            User management:
                granted: False
            Group management:
                granted: False

    And user of browser1 removes all tokens



  Scenario: User sees right Invite tokens after filtering them
    Given user admin has no harvesters
    And using REST, user admin creates ["harvester8", "harvester9"] harvester in "onezone" Onezone service

    Then user of browser1 removes all tokens

    And user of browser1 creates token with following configuration:
          name: space_token_1
          type: invite
          invite type: Invite user to space
          invite target: space1
    And user of browser1 creates token with following configuration:
          name: space_token_3
          type: invite
          invite type: Invite user to space
          invite target: space3

    And user of browser1 creates token with following configuration:
          name: harvester_token_8
          type: invite
          invite type: Invite user to harvester
          invite target: harvester8
    And user of browser1 creates token with following configuration:
          name: harvester_token_9
          type: invite
          invite type: Invite user to harvester
          invite target: harvester9

    And user of browser1 creates token with following configuration:
          name: group_token_3
          type: invite
          invite type: Invite user to group
          invite target: group3
    And user of browser1 creates token with following configuration:
          name: group_token_4
          type: invite
          invite type: Invite user to group
          invite target: group4

    And user of browser1 creates token with following configuration:
          name: cluster_token_1
          type: invite
          invite type: Invite user to cluster
          invite target: oneprovider-1
    And user of browser1 creates token with following configuration:
          name: cluster_token_2
          type: invite
          invite type: Invite user to cluster
          invite target: oneprovider-2

    And user of browser1 creates token with following configuration:
          name: register_token_1
          type: invite
          invite type: Register Oneprovider

    And user of browser1 chooses "Invite" filter in tokens sidebar
    Then user of browser1 sees exactly 9 item(s) on tokens list in tokens sidebar

    And user of browser1 chooses "Space" Invite filter in tokens sidebar
    And user of browser1 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "space_token_1" on tokens list
    And user of browser1 sees that there is token named "space_token_3" on tokens list
    And user of browser1 chooses "space3" name Invite filter in tokens sidebar
    And user of browser1 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "space_token_3" on tokens list

    And user of browser1 chooses "User" Invite filter in tokens sidebar
    And user of browser1 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "register_token_1" on tokens list

    And user of browser1 chooses "Group" Invite filter in tokens sidebar
    And user of browser1 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "group_token_3" on tokens list
    And user of browser1 sees that there is token named "group_token_4" on tokens list
    And user of browser1 chooses "group3" name Invite filter in tokens sidebar
    And user of browser1 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "group_token_3" on tokens list

    And user of browser1 chooses "Harvester" Invite filter in tokens sidebar
    And user of browser1 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "harvester_token_8" on tokens list
    And user of browser1 sees that there is token named "harvester_token_9" on tokens list
    And user of browser1 chooses "harvester8" name Invite filter in tokens sidebar
    And user of browser1 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "harvester_token_8" on tokens list

    And user of browser1 chooses "Cluster" Invite filter in tokens sidebar
    And user of browser1 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "cluster_token_1" on tokens list
    And user of browser1 sees that there is token named "cluster_token_2" on tokens list
    And user of browser1 chooses "oneprovider-1" name Invite filter in tokens sidebar
    And user of browser1 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "cluster_token_1" on tokens list

    And user of browser1 removes all tokens
    And user of browser1 removes "harvester8" harvester in Onezone page
    And user of browser1 removes "harvester9" harvester in Onezone page


  Scenario: User can see removed space ID in invitation token
    When user of browser2 creates token with following configuration:
          name: space_token_1
          type: invite
          invite type: Invite group to space
          invite target: space2
    And user of browser2 removes "space2" space in Onezone page
    And user of browser2 clicks on Tokens in the main menu
    And user of browser2 sees that there is token named "space_token_1" on tokens list
    And user of browser2 clicks on "space_token_1" on token list
    And user of browser2 refreshes site
    Then user of browser2 sees that created token configuration is as following:
          name: space_token_1
          invite type: Invite group to space
          invite target: $(resolve_id space2)
