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
    And user of browser1 unchecks nested "View privileges" privilege in "Cluster management" privilege for user1 user in cluster page

    # fail to view privileges
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks "admin" user in "oneprovider-1" cluster members users list
    Then user of browser2 sees Insufficient permissions alert for "admin" user in cluster members subpage


  Scenario: User fails to set privileges without set privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 unchecks nested "Set privileges" privilege in "Cluster management" privilege for user1 user in cluster page

    # fail to uncheck privileges
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser2 expands "Cluster management" privilege for "user1" user in cluster members subpage
    And user of browser2 unchecks "View privileges" privilege toggle in "Cluster management" for "user1" user in cluster members subpage
    And user of browser2 clicks Save button for "user1" user in cluster members subpage
    Then user of browser2 sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to remove cluster without remove cluster privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 unchecks nested "Remove cluster" privilege in "Cluster management" privilege for user1 user in cluster page

    # fail to remove cluster
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks on deregister provider button in clusters page
    And user of browser2 checks the understand notice in clusters page
    And user of browser2 clicks on confirm deregistration button in clusters page
    Then user of browser2 sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to remove user without remove user privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 unchecks nested "Remove user" privilege in "User management" privilege for user1 user in cluster page

    # fail to remove user
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 is idle for 2 seconds
    And user of browser2 removes "admin" user from "oneprovider-1" cluster members
    Then user of browser2 sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to add user without add user privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 unchecks nested "Add user" privilege in "User management" privilege for user1 user in cluster page

    # fail to add user
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks on "Invite user using token" button in users list menu in "oneprovider-1" cluster members view
    And user of browser2 is idle for 2 seconds
    Then user of browser2 sees Insufficient permissions alert in "Invite using token" modal


  Scenario: User fails to remove group from cluster without remove group privileges
    When user of browser1 creates group "group1"
    And user of browser1 adds "group1" group to "oneprovider-1" cluster
    And user of browser1 sees "group1" group on "oneprovider-1" cluster members list

    And user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 unchecks nested "Remove group" privilege in "Group management" privilege for user1 user in cluster page

    # fail to remove group from cluster
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 removes "group1" group from "oneprovider-1" cluster members
    Then user of browser2 sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to add group to cluster without add group privileges
    When user of browser2 creates group "group1"

    And user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 unchecks nested "Add group" privilege in "Group management" privilege for user1 user in cluster page

    # fail to add group to cluster
    And user of browser2 adds "group1" group to "oneprovider-1" cluster
    Then user of browser2 sees that error modal with text "insufficient privileges" appeared

  Scenario: User fails to see members without view cluster
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 unchecks nested "View cluster" privilege in "Cluster management" privilege for user1 user in cluster page

    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 refreshes site
    Then user of browser2 sees Insufficient permissions alert in cluster members subpage


  Scenario: User fails to modify cluster without modify cluster privileges
    When user of browser1 invites user of browser2 to "oneprovider-1" cluster
    And user of browser2 joins to cluster
    And user of browser1 unchecks nested "Modify cluster" privilege in "Cluster management" privilege for user1 user in cluster page

    # fail to modify cluster
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Provider item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 is idle for 60 seconds
    And user of browser2 clicks on modify provider details button in clusters page
    And user of browser2 types "pro1" to Provider name input box in modify provider details form in Provider panel
    And user of browser2 clicks on confirm modify provider details button in clusters page
    Then user of browser2 sees that error modal with text "Forbidden" appeared

