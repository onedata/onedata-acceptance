Feature: Management of invite tokens in Onezone GUI, with admin user

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1

    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, admin] to [Onezone, Onezone] service


  Scenario: Group has default harvester member privileges after user consumes group to harvester invite token with default settings
    Given user admin has no harvesters
    And user admin has "harvester1" harvester in "onezone" Onezone service
    When user of browser2 creates token with following configuration:
          type: invite
          invite type: Invite group to harvester
          invite target: harvester1
    And user of browser2 sees that created token configuration is as following:
          invite type: Invite group to harvester
          invite target: harvester1
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
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1

    And user of browser1 succeeds to consume token for "group1" group
    And user of browser1 sees that "harvester1" has appeared on the harvesters list in the sidebar

    Then user of browser2 sees that harvester "harvester1" has following privilege configuration for group "group1":
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

    And user of browser2 removes all tokens


  Scenario: User has default cluster member privileges after consuming user to cluster invite token with default settings
    When user of browser2 creates token with following configuration:
          type: invite
          invite type: Invite user to cluster
          invite target: oneprovider-1
    And user of browser2 sees that created token configuration is as following:
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
    And user of browser2 clicks on copy button in token view
    And user of browser2 sends copied token to user of browser1

    And user of browser1 joins cluster using copied token
    Then user of browser1 sees "oneprovider-1" subpage in Clusters page

    And user of browser2 sees that cluster "oneprovider-1" has following privilege configuration for user "user1":
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

    And user of browser2 removes all tokens
