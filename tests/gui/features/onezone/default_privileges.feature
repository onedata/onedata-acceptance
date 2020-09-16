Feature: Management of privileges in onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
          - user1
    And admin user does not have access to any space
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
          space2:
            owner: admin
            users:
                - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user1
          group3:
            owner: admin
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User sees that group added to space has default privileges
    When user of browser2 adds "group1" group to "space1" space using available groups dropdown
    And user of browser2 clicks "group1" group in "space1" space members groups list
    Then user of browser2 sees following privileges of "group1" group in space members subpage:
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
    And user of browser2 clicks to minimalize ["Data management", "Transfer management"] privileges of "group1" group in space members subpage
    And user of browser2 sees following privileges of "group1" group in space members subpage:
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


  Scenario: User sees that user added to space has default privileges
    When user of browser2 copies invite token to "space1" space
    And user of browser2 sends copied token to user of browser1
    And user of browser1 joins space using received token
    And user of browser2 clicks "admin" user in "space1" space members users list
    Then user of browser2 sees following privileges of "admin" user in space members subpage:
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
    And user of browser2 clicks to minimalize ["Data management", "Transfer management"] privileges of "admin" user in space members subpage
    And user of browser2 sees following privileges of "admin" user in space members subpage:
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
  And user of browser1 leaves "space1" space in Onezone page


  Scenario: User sees that group added to group has default privileges
    When user of browser2 adds "group1" group to "group2" group using available groups dropdown
    And user of browser2 clicks "group1" group in "group2" group members groups list

    Then user of browser2 sees following privileges of "group1" group in group members subpage:
          Group management:
            granted: Partially
            privilege subtypes:
              View group: True
              Modify group: False
              Remove group: False
              View privileges: False
              Set privileges: False
          Group hierarchy management:
            granted: False
          User management:
            granted: False
          Space management:
            granted: False
          Handle management:
            granted: False


  Scenario: User sees that user added to group has default privileges
    When browser2 invites browser1 to group "group2" using Oneprovider web GUI
    And user of browser1 joins group he was invited to in Onezone service
    And user of browser2 clicks "admin" user in "group2" group members users list

    Then user of browser2 sees following privileges of "admin" user in group members subpage:
          Group management:
            granted: Partially
            privilege subtypes:
              View group: True
              Modify group: False
              Remove group: False
              View privileges: False
              Set privileges: False
          Group hierarchy management:
            granted: False
          User management:
            granted: False
          Space management:
            granted: False
          Handle management:
            granted: False

    And user of browser1 leaves group "group2"


  Scenario: User sees that group added to harvester has default privileges
    Given user admin has no harvesters
    And using REST, user admin creates "harvester3" harvester in "onezone" Onezone service

    When user of browser1 clicks on Discovery in the main menu
    And user of browser1 clicks "harvester3" on the harvesters list in the sidebar
    And user of browser1 adds "group3" group to "harvester3" harvester using available groups dropdown
    And user of browser1 clicks "group3" group in "harvester3" harvester members groups list

    Then user of browser1 sees following privileges of "group3" group in harvester members subpage:
          Harvester management:
            granted: Partially
            privilege subtypes:
              View harvester: True
              Modify harvester: False
              Remove harvester: False
              View privileges: False
              Set privileges: False
          User management:
            granted: False
          Group management:
            granted: False
          Space management:
            granted: False

    And user of browser1 removes "harvester3" harvester in Onezone page


  Scenario: User sees that user added to harvester has default privileges
    Given user admin has no harvesters
    And using REST, user admin creates "harvester2" harvester in "onezone" Onezone service

    When user of browser1 sends invitation token from "harvester2" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser1 clicks "user1" user in "harvester2" harvester members users list

    Then user of browser1 sees following privileges of "user1" user in harvester members subpage:
          Harvester management:
            granted: Partially
            privilege subtypes:
              View harvester: True
              Modify harvester: False
              Remove harvester: False
              View privileges: False
              Set privileges: False
          User management:
            granted: False
          Group management:
            granted: False
          Space management:
            granted: False

    And user of browser1 removes "harvester2" harvester in Onezone page


  Scenario: User sees that group added to cluster has default privileges
    Given user of browser1 sees no "group3" group in "oneprovider-1" cluster members

    When user of browser1 adds "group3" group to "oneprovider-1" cluster
    And user of browser1 clicks "group3" group in "oneprovider-1" cluster members groups list

    Then user of browser1 sees following privileges of "group3" group in cluster members subpage:
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

    And user of browser1 removes "group3" group from "oneprovider-1" cluster members


  Scenario: User sees that user added to cluster has default privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list

    Then user of browser1 sees following privileges of "user1" user in cluster members subpage:
          Cluster management:
            granted: True
          User management:
            granted: True
          Group management:
            granted: True

    And user of browser1 removes "user1" user from "oneprovider-1" cluster members
