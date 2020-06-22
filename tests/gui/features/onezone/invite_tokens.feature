Feature: Management of invite tokens in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
            space0:
                owner: user1
                providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            space1:
                owner: admin
            space2:
                owner: user1
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: user1
            group2:
                owner: user2
            group3:
                owner: admin
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: Privileged user successfully consumes group to space invite token with consumer caveat
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                Remove space: False
                View privileges: True
            Transfer management:
              granted: False
          caveats:
            consumer:
              - type: user
                by: id
                consumer name: user1
    And user of browser1 sees that created token configuration is as following:
          type: Invite
          invite type: Invite group to space
          invite target: space1
          usage count: 0 / infinity
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                Remove space: False
                View privileges: True
            User management:
              granted: False
          caveats:
            consumer:
              - type: user
                by: name
                consumer name: user1
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    # consume invite token
    And user of browser2 clicks on Tokens in the main menu
    And user of browser2 clicks on "Consume token" button in tokens sidebar
    And user of browser2 pastes received token into token text field
    And user of browser2 chooses "group1" group from dropdown on tokens page
    And user of browser2 clicks on Join button on consume token page
    Then user of browser2 sees an success notify with text matching to: .*joined.*
    And user of browser2 sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser2 sees that space space1 has following privilege configuration for group group1:
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                Remove space: False
                View privileges: True
            User management:
              granted: False

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: Unprivileged user fails to consume group to space invite token with consumer caveat
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          caveats:
            consumer:
              - type: user
                by: id
                consumer name: user2
    And user of browser1 sees that created token configuration is as following:
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          caveats:
            consumer:
              - type: user
                by: name
                consumer name: user2
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    # consume invite token
    And user of browser2 clicks on Tokens in the main menu
    And user of browser2 clicks on "Consume token" button in tokens sidebar
    And user of browser2 pastes received token into token text field
    And user of browser2 chooses "group1" group from dropdown on tokens page
    And user of browser2 clicks on Join button on consume token page
    Then user of browser2 sees that error modal with text "Consuming token failed" appeared

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: User successfully consumes group to space invite token with consumer caveat set for Any user
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          caveats:
            consumer:
              - type: user
                by: name
                consumer name: Any user
    And user of browser1 sees that created token configuration is as following:
          type: Invite
          invite type: Invite group to space
          invite target: space1
          usage count: 0 / infinity
          caveats:
            consumer:
              - type: user
                by: name
                consumer name: Any user
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    Then user of browser2 succeeds to consume token for "group1" group

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: Group has default space member privileges after user consumes group to space invite token with default settings
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
    And user of browser1 sees that created token configuration is as following:
          type: Invite
          invite type: Invite group to space
          invite target: space1
          usage count: 0 / infinity
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
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service

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
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: Privileged group succeeds to join space using invite token with consumer caveat
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                View privileges: True
            Group management:
              granted: True
          caveats:
            consumer:
              - type: group
                by: id
                consumer name: group1
    And user of browser1 sees that created token configuration is as following:
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                View privileges: True
            Group management:
              granted: True
          caveats:
            consumer:
              - type: group
                by: name
                consumer name: group1
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    Then user of browser2 succeeds to consume token for "group1" group
    And user of browser2 sees that space space1 has following privilege configuration for group group1:
          privileges:
            Space management:
              granted: Partially
              privilege subtypes:
                View space: True
                View privileges: True
            Group management:
              granted: True

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: Unprivileged group fails to join space using invite token with consumer caveat
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          caveats:
            consumer:
              - type: group
                by: id
                consumer name: group2
    And user of browser1 clicks on copy button in token view
    And user of browser1 sees that created token configuration is as following:
          invite type: Invite group to space
          invite target: space1
          usage limit: infinity
          caveats:
            consumer:
              - type: group
                by: name
                consumer name: group2
    And user of browser1 sends copied token to user of browser2
    Then user of browser2 fails to consume token for "group1" group

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: Group succeeds to join space invite token with consumer caveat set for Any group
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Invite group to space
          invite target: space1
          caveats:
            consumer:
              - type: group
                by: name
                consumer name: Any group
    And user of browser1 sees that created token configuration is as following:
          type: Invite
          invite type: Invite group to space
          invite target: space1
          usage count: 0 / infinity
          caveats:
            consumer:
              - type: group
                by: name
                consumer name: Any group
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    Then user of browser2 succeeds to consume token for "group1" group

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: User successfully consumes harvester to space invite token until usage limit is not expired
    When user of browser1 creates "harvester1" harvester in Onezone page
    And user of browser1 creates "harvester2" harvester in Onezone page
    And user of browser1 creates "harvester3" harvester in Onezone page

    And user of browser2 creates token with following configuration:
          type: invite
          invite type: Invite harvester to space
          invite target: space2
          usage limit: 2
    And user of browser2 sees that token usage count is "0 / 2"
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1

    Then user of browser1 succeeds to consume token for "harvester1" harvester
    And user of browser2 is idle for 3 seconds
    And user of browser2 sees that token usage count is "1 / 2"
    And user of browser1 sees that "space2" has appeared on the spaces list of "harvester1" harvester

    Then user of browser1 succeeds to consume token for "harvester2" harvester
    And user of browser2 is idle for 3 seconds
    And user of browser2 sees that token usage count is "2 / 2"
    And user of browser1 sees that "space2" has appeared on the spaces list of "harvester1" harvester

    Then user of browser1 fails to consume token for "harvester3" harvester
    And user of browser1 removes "harvester1" harvester in Onezone page
    And user of browser1 removes "harvester2" harvester in Onezone page
    And user of browser1 removes "harvester3" harvester in Onezone page
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: Group has default harvester member privileges after user consumes group to harvester invite token with default settings
    When user of browser1 creates "harvester4" harvester in Onezone page
    And user of browser1 creates token with following configuration:
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
    And user of browser1 removes "harvester4" harvester in Onezone page
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: User successfully cleans up obsolete tokens
    When user of browser1 creates "harvester5" harvester in Onezone page
    And user of browser1 removes all tokens
    And user of browser1 creates token with following configuration:
          type: invite
          name: ToSurvive
          invite type: Invite user to space
          invite target: space1
          usage limit: 1
    And user of browser1 sees that created token configuration is as following:
          name: ToSurvive
          type: Invite
          invite type: Invite user to space
          invite target: space1
          usage count: 0 / 1
    And user of browser1 creates token with following configuration:
          name: ToRemove
          type: invite
          invite type: Invite group to harvester
          invite target: harvester5
          usage limit: 1
    And user of browser1 sees that created token configuration is as following:
          name: ToRemove
          type: Invite
          invite type: Invite group to harvester
          invite target: harvester5
          usage count: 0 / 1
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2

    And user of browser2 succeeds to consume token for "group1" group

    And user of browser1 is idle for 3 seconds
    And user of browser1 sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser1 clicks on "Clean up obsolete tokens" button in tokens sidebar
    And user of browser1 sees that "Clean up obsolete tokens" modal has appeared
    And user of browser1 clicks on "Remove" button in modal "Clean up obsolete tokens"

    Then user of browser1 sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser1 sees that there is token named "ToSurvive" on tokens list

    And user of browser1 removes all tokens
    And user of browser1 removes "harvester5" harvester in Onezone page
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: User fails to consume revoked token
    When user of browser1 creates "harvester6" harvester in Onezone page
    And user of browser1 creates token with following configuration:
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
    Then user of browser2 fails to consume token for "group1" group

    And user of browser1 removes all token
    And user of browser1 removes "harvester6" harvester in Onezone page
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: User fails to consume deleted token
    When user of browser1 creates "harvester7" harvester in Onezone page
    And user of browser1 creates token with following configuration:
          name: token1
          type: invite
          invite type: Invite group to harvester
          invite target: harvester7
    And user of browser1 sees that created token configuration is as following:
      name: token1
      invite type: Invite group to harvester
      invite target: harvester7
    And user of browser1 clicks on copy button in token view
    And user of browser1 sends copied token to user of browser2
    And user of browser1 removes token named "token1"
    Then user of browser2 fails to consume token for "group1" group

    And user of browser1 removes all tokens
    And user of browser1 removes "harvester7" harvester in Onezone page
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


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
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


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

    And user of browser2 succeeds to consume token
    Then user of browser2 sees that cluster oneprovider-1 has following privilege configuration for user user1:
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
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: Privileged provider succeeds to support space with invite token with consumer caveat
    When user of browser2 creates token with following configuration:
          type: invite
          invite type: Support space
          invite target: space2
          caveats:
            consumer:
              - type: oneprovider
                by: name
                consumer name: oneprovider-1
    And user of browser2 sees that created token configuration is as following:
          invite type: Support space
          invite target: space2
          caveats:
            consumer:
              - type: oneprovider
                by: name
                consumer name: oneprovider-1
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    Then user of browser1 succeeds to support "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB

    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: User sees expiration and region allow caveats in token configuration after setting them in new invite token
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Register Oneprovider
          caveats:
            expiration:
              after: 10
            region:
              allow: True
              region codes:
                - Europe
                - Asia
            country:
              allow: True
              country codes:
                - PL
                - BS
    Then user of browser1 sees that created token configuration is as following:
          invite type: Register Oneprovider
          caveats:
            expiration:
              set: True
            region:
              allow: True
              region codes:
                - Asia
                - Europe
            country:
              allow: True
              country codes:
                - PL
                - BS

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: User sees IP and region deny caveats in token configuration after setting them in new invite token
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Register Oneprovider
          caveats:
            region:
              allow: False
              region codes:
                - Europe
                - Asia
            IP:
              - 192.0.2.1
              - 192.0.2.0/24
    Then user of browser1 sees that created token configuration is as following:
          invite type: Register Oneprovider
          caveats:
            region:
              allow: False
              region codes:
                - Asia
                - Europe
            IP:
              - 192.0.2.1/32
              - 192.0.2.0/24

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: User sees ASN and region deny caveats in token configuration after setting them in new invite token
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Register Oneprovider
          caveats:
            country:
              allow: True
              country codes:
                - PL
                - BS
            ASN:
              - 64496
              - 64498
    Then user of browser1 sees that created token configuration is as following:
          invite type: Register Oneprovider
          caveats:
            country:
              allow: True
              country codes:
                - PL
                - BS
            ASN:
              - 64496
              - 64498

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: User sees all token caveats in token configuration after setting them in new invite token
    When user of browser1 creates token with following configuration:
          type: invite
          invite type: Register Oneprovider
          caveats:
            expiration:
              after: 10
            region:
              allow: True
              region codes:
                - Europe
            country:
              allow: True
              country codes:
                - BS
            ASN:
              - 64496
            IP:
              - 192.0.2.1
            consumer:
              - type: user
                by: id
                consumer name: user1
    Then user of browser1 sees that created token configuration is as following:
          invite type: Register Oneprovider
          caveats:
            expiration:
              set: True
            region:
              allow: True
              region codes:
                - Europe
            country:
              allow: True
              country codes:
                - BS
            ASN:
              - 64496
            IP:
              - 192.0.2.1/32
            consumer:
              - type: user
                by: name
                consumer name: user1

    And user of browser1 removes all tokens
    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: Provider succeeds to support space with invite token with consumer caveat set for Any Oneprovider
    When user of browser2 creates token with following configuration:
            type: invite
            invite type: Support space
            invite target: space2
            caveats:
              consumer:
                - type: oneprovider
                  by: name
                  consumer name: Any Oneprovider
    And user of browser2 sees that created token configuration is as following:
            invite type: Support space
            invite target: space2
            caveats:
              consumer:
                - type: oneprovider
                  by: name
                  consumer name: Any Oneprovider
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    Then user of browser1 succeeds to support "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB

    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service


  Scenario: Unprivileged provider fails to support space with invite token with consumer caveat
    When user of browser2 creates token with following configuration:
            type: invite
            invite type: Support space
            invite target: space2
            caveats:
              consumer:
                - type: oneprovider
                  by: name
                  consumer name: oneprovider-1
    And user of browser2 sees that created token configuration is as following:
            invite type: Support space
            invite target: space2
            caveats:
              consumer:
                - type: oneprovider
                  by: name
                  consumer name: oneprovider-1
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-2" in clusters menu
    Then user of browser1 fails to support "space1" space in "oneprovider-2" Oneprovider panel service with following configuration:
          storage: posix
          size: 1
          unit: GiB

    And using web GUI, user of browser1 leaves space named space1 in "onezone" Onezone service

