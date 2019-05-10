Feature: Basic cluster members management utilities using onepanel

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User fails to see privileges without view privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage

    # uncheck view privileges
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "Cluster management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "View privileges" privilege toggle in "Cluster management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    # fail to view privileges
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks "admin" user in "oneprovider-1" cluster members users list
    Then user of browser2 sees Insufficient permissions alert for "admin" user in cluster members subpage


  Scenario: User fails to set privileges without set privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage

    # uncheck set privileges
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "Cluster management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "Set privileges" privilege toggle in "Cluster management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    # fail to uncheck privileges
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser2 expands "Cluster management" privilege for "user1" user in cluster members subpage
    And user of browser2 unchecks "View privileges" privilege toggle in "Cluster management" for "user1" user in cluster members subpage
    And user of browser2 clicks Save button for "user1" user in cluster members subpage
    Then user of browser2 sees that error modal with text "Insufficient permissions" appeared


  Scenario: User fails to remove cluster without remove cluster privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage

    # uncheck remove cluster
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "Cluster management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "Remove cluster" privilege toggle in "Cluster management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    # fail to remove cluster
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks on deregister provider button in clusters page
    And user of browser2 checks the understand notice in clusters page
    And user of browser2 clicks on confirm deregistration button in clusters page
    Then user of browser2 sees that error modal with text "Insufficient permissions" appeared


  Scenario: User fails to remove user without remove user privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage

    # uncheck remove user privilege
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "User management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "Remove user" privilege toggle in "User management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    # fail to remove user
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 is idle for 2 seconds
    And user of browser2 removes "admin" user from "oneprovider-1" cluster members
    Then user of browser2 sees that error modal with text "Insufficient permissions" appeared


  Scenario: User fails to add user without add user privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage

    # uncheck add user privilege
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "User management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "Add user" privilege toggle in "User management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    # fail to add user
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks on "Invite user using token" button in users list menu in "oneprovider-1" cluster members view
    And user of browser2 is idle for 2 seconds
    Then user of browser2 sees Insufficient permissions alert in "Invite using token" modal


  Scenario: User fails to remove group from cluster
    # create group
    When user of browser1 clicks on Create group button in groups sidebar
    And user of browser1 writes "group1" into group name text field
    And user of browser1 confirms using enter

    # add group to cluster
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on "Add one of your groups" button in groups list menu in "oneprovider-1" cluster members view
    And user of browser1 selects "group1" from group selector in add one of your groups modal
    And user of browser1 clicks "Add" confirmation button in displayed modal
    And user of browser1 sees "group1" group on "oneprovider-1" cluster members list

    And user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster

    # uncheck remove group privileges
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "Group management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "Remove group" privilege toggle in "Group management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage
    And user of browser1 refreshes site

    # fail to remove group from cluster
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 removes "group1" group from "oneprovider-1" cluster members
    Then user of browser2 sees that error modal with text "Insufficient permissions" appeared


  Scenario: User fails to add group to cluster
    # create group
    When user of browser2 clicks on Create group button in groups sidebar
    And user of browser2 writes "group1" into group name text field
    And user of browser2 confirms using enter

    And user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster

    # uncheck add group privileges
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "Group management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "Add group" privilege toggle in "Group management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    # fail to add group to cluster
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks on "Add one of your groups" button in groups list menu in "oneprovider-1" cluster members view
    And user of browser2 selects "group1" from group selector in add one of your groups modal
    And user of browser2 clicks "Add" confirmation button in displayed modal
    Then user of browser2 sees that error modal with text "Insufficient permissions" appeared

  Scenario: User fails to see members without view cluster
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster

    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser2 sees privileges for "user1" user in cluster members subpage

    # uncheck view privileges
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "Cluster management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "View cluster" privilege toggle in "Cluster management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    And user of browser2 refreshes site
    Then user of browser2 sees Insufficient permissions alert in cluster members subpage


  Scenario: User fails to modify cluster without remove cluster privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage

    # uncheck modify cluster
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "Cluster management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "Modify cluster" privilege toggle in "Cluster management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    # fail to modify cluster
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 is idle for 60 seconds
    And user of browser2 clicks on modify provider details button in clusters page
    And user of browser2 types "pro1" to Provider name input box in modify provider details form in Provider panel
    And user of browser2 clicks on confirm modify provider details button in clusters page
    Then user of browser2 sees that error modal with text "Forbidden" appeared



