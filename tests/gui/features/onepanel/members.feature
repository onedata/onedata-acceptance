Feature: Basic cluster members management utilities using onepanel

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And there is no group2 group in Onezone page used by admin before definition in next steps
    And initial groups configuration in "onezone" Onezone service:
          group2:
            owner: admin
            users:
                - user1
    And users opened [browser_admin, browser_standard] browsers' windows
    And users of [browser_admin, browser_standard] opened [Onezone, Onezone] page
    And user of [browser_admin, browser_standard] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User fails to see privileges without view privileges
    When user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sets following privileges for user1 user in cluster page:
          Cluster management:
            granted: Partially
            privilege subtypes:
              View privileges: False

    # fail to view privileges
    And user of browser_standard clicks on Clusters in the main menu
    And user of browser_standard clicks on "oneprovider-1" in clusters menu
    And user of browser_standard clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_standard clicks "admin" user in "oneprovider-1" cluster members users list
    Then user of browser_standard sees Insufficient privileges alert for "admin" user in cluster members subpage


  Scenario: User fails to set privileges without set privileges
    When user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sets following privileges for user1 user in cluster page:
          Cluster management:
            granted: Partially
            privilege subtypes:
              Set privileges: False

    # fail to uncheck privileges
    And user of browser_standard clicks on Clusters in the main menu
    And user of browser_standard clicks on "oneprovider-1" in clusters menu
    And user of browser_standard clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_standard clicks "user1" user in "oneprovider-1" cluster members users list
    Then user of browser_standard fails to set following privileges for "user1" user in cluster members subpage:
          Cluster management:
            granted: Partially
            privilege subtypes:
              View privileges: False


  Scenario: User fails to remove cluster without remove cluster privileges
    When user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sets following privileges for user1 user in cluster page:
          Cluster management:
            granted: Partially
            privilege subtypes:
              Remove cluster: False

    # fail to remove cluster
    And user of browser_standard clicks on Clusters in the main menu
    And user of browser_standard clicks on "oneprovider-1" in clusters menu
    And user of browser_standard clicks on Provider configuration item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_standard clicks on deregister provider button in clusters page
    And user of browser_standard checks the understand notice in clusters page
    And user of browser_standard clicks on confirm deregistration button in clusters page
    Then user of browser_standard sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to remove user without remove user privileges
    When user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sets following privileges for user1 user in cluster page:
          User management:
            granted: Partially
            privilege subtypes:
              Remove user: False
    # fail to remove user
    And user of browser_standard clicks on Clusters in the main menu
    And user of browser_standard clicks on "oneprovider-1" in clusters menu
    And user of browser_standard clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_standard removes "admin" user from "oneprovider-1" cluster members
    Then user of browser_standard sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to add user without add user privileges
    When user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sets following privileges for user1 user in cluster page:
          User management:
            granted: Partially
            privilege subtypes:
              Add user: False
    # fail to add user
    And user of browser_standard clicks on Clusters in the main menu
    And user of browser_standard clicks on "oneprovider-1" in clusters menu
    And user of browser_standard clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_standard clicks on "Invite user using token" button in users list menu in "oneprovider-1" cluster members view
    Then user of browser_standard sees "This resource could not be loaded" alert in "Invite using token" modal


  Scenario: User fails to remove group from cluster without remove group privileges
    When user of browser_admin creates group "group1"
    And user of browser_admin adds "group1" group to "oneprovider-1" cluster
    And user of browser_admin sees "group1" group on "oneprovider-1" cluster members list

    And user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sets following privileges for user1 user in cluster page:
          Group management:
            granted: Partially
            privilege subtypes:
              Remove group: False
    # fail to remove group from cluster
    And user of browser_standard clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_standard removes "group1" group from "oneprovider-1" cluster members
    Then user of browser_standard sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to add group to cluster without add group privileges
    When user of browser_standard creates group "group1"

    And user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sets following privileges for user1 user in cluster page:
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: False

    # fail to add group to cluster
    And user of browser_standard adds "group1" group to "oneprovider-1" cluster
    Then user of browser_standard sees that error modal with text "insufficient privileges" appeared

  Scenario: User fails to see members without view cluster
    When user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sets following privileges for user1 user in cluster page:
          Cluster management:
            granted: Partially
            privilege subtypes:
              View cluster: False

    And user of browser_standard clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    Then user of browser_standard sees "Insufficient privileges" alert in cluster members subpage


  Scenario: User fails to modify cluster without modify cluster privileges
    When user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sets following privileges for user1 user in cluster page:
          Cluster management:
            granted: Partially
            privilege subtypes:
              Modify cluster: False

    # fail to modify cluster
    And user of browser_standard clicks on Clusters in the main menu
    And user of browser_standard clicks on "oneprovider-1" in clusters menu
    And user of browser_standard clicks on Provider configuration item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser_standard is idle for 60 seconds
    And user of browser_standard clicks on Edit settings button in clusters page
    And user of browser_standard types "pro1" to Provider name input box in modify provider details form in Provider panel
    And user of browser_standard saves changes in provider details form in Provider panel
    Then user of browser_standard sees that error modal with text "Provider data modification failed" appeared


  Scenario: User successfully invites other user to cluster
    When user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    Then user of browser_admin sees "user1" user in cluster members
    And user of browser_standard sees "oneprovider-1" in clusters menu


  Scenario: User successfully removes other user from cluster
    When user of browser_admin invites user of browser_standard to "oneprovider-1" cluster
    And user of browser_standard joins to cluster
    And user of browser_admin sees "user1" user in cluster members

    And user of browser_admin removes "user1" user from "oneprovider-1" cluster members
    Then user of browser_admin does not see "user1" user in cluster members
    And user of browser_standard refreshes site
    And user of browser_standard does not see "oneprovider-1" in clusters menu


  Scenario: User successfully adds group to cluster
    When user of browser_standard does not see "oneprovider-1" in clusters menu
    And user of browser_admin clicks on Clusters in the main menu
    And user of browser_admin clicks on "oneprovider-1" in clusters menu
    And user of browser_admin adds "group2" group to "oneprovider-1" cluster
    Then user of browser_admin sees "group2" group on "oneprovider-1" cluster members list
    And user of browser_standard sees "oneprovider-1" in clusters menu


  Scenario: User successfully removes group from cluster
    When user of browser_standard does not see "oneprovider-1" in clusters menu
    And user of browser_admin clicks on Clusters in the main menu
    And user of browser_admin clicks on "oneprovider-1" in clusters menu
    And user of browser_admin adds "group2" group to "oneprovider-1" cluster
    And user of browser_admin removes "group2" group from "oneprovider-1" cluster members
    Then user of browser_admin does not see "group2" group on "oneprovider-1" cluster members list
    And user of browser_standard does not see "oneprovider-1" in clusters menu
