Feature: Basic cluster members management utilities using onepanel

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User fails to see privileges without view privileges
    # invite user to cluster
    When user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on "Invite user using token" button in users list menu in "oneprovider-1" cluster members view
    And user of browser1 copies invitation token from modal
    And user of browser1 closes "Invite using token" modal
    And user of browser1 sends copied token to user of browser2

    # join the cluster
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on join cluster button in clusters menu
    And user of browser2 pastes copied token into join cluster token text field
    And user of browser2 clicks on join the cluster button in clusters page

    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage

    # uncheck view privileges
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "Cluster management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "View privileges" privilege toggle in "Cluster management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks "admin" user in "oneprovider-1" cluster members users list
    Then user of browser2 sees Insufficient permissions alert for "admin" user in cluster members subpage


  Scenario: User fails to remove user without remove user privileges
    # invite user to cluster
    When user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on "Invite user using token" button in users list menu in "oneprovider-1" cluster members view
    And user of browser1 copies invitation token from modal
    And user of browser1 closes "Invite using token" modal
    And user of browser1 sends copied token to user of browser2

    # join the cluster
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on join cluster button in clusters menu
    And user of browser2 pastes copied token into join cluster token text field
    And user of browser2 clicks on join the cluster button in clusters page

    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage

    # uncheck remove user privilege
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "User management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "Remove user" privilege toggle in "User management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 is idle for 2 seconds
    And user of browser2 removes "admin" user from "oneprovider-1" cluster members
    Then user of browser2 sees that error modal with text "Insufficient permissions" appeared


  Scenario: User fails to add user without add user privileges
    # invite user to cluster
    When user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on "Invite user using token" button in users list menu in "oneprovider-1" cluster members view
    And user of browser1 copies invitation token from modal
    And user of browser1 closes "Invite using token" modal
    And user of browser1 sends copied token to user of browser2

    # join the cluster
    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on join cluster button in clusters menu
    And user of browser2 pastes copied token into join cluster token text field
    And user of browser2 clicks on join the cluster button in clusters page
    And user of browser1 is idle for 2 seconds

    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage

    # uncheck add user privilege
    And user of browser1 clicks "user1" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "user1" user in cluster members subpage
    And user of browser1 expands "User management" privilege for "user1" user in cluster members subpage
    And user of browser1 unchecks "Add user" privilege toggle in "User management" for "user1" user in cluster members subpage
    And user of browser1 clicks Save button for "user1" user in cluster members subpage

    And user of browser2 clicks on Clusters in the main menu
    And user of browser2 clicks on "oneprovider-1" in clusters menu
    And user of browser2 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser2 clicks on "Invite user using token" button in users list menu in "oneprovider-1" cluster members view
    And user of browser2 is idle for 2 seconds
    Then user of browser2 sees Insufficient permissions alert in "Invite using token" modal


  Scenario: User fails to see members without view cluster
    When user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks "admin" user in "oneprovider-1" cluster members users list
    And user of browser1 sees privileges for "admin" user in cluster members subpage
    And user of browser1 expands "Cluster management" privilege for "admin" user in cluster members subpage
    And user of browser1 unchecks "View cluster" privilege toggle in "Cluster management" for "admin" user in cluster members subpage
    And user of browser1 clicks Save button for "admin" user in cluster members subpage
    And user of browser1 refreshes site
    Then user of browser1 sees Insufficient permissions alert in cluster members subpage


  Scenario: User add group to cluster
    When user of browser1 clicks on Create group button in groups sidebar
    And user of browser1 writes "group1" into group name text field
    And user of browser1 confirms using enter

    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of browser1 clicks on Members item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 clicks on "Add one of your groups" button in groups list menu in "oneprovider-1" cluster members view
    And user of browser1 selects "group1" from group selector in add one of your groups modal
    And user of browser1 clicks "Add" confirmation button in displayed modal
    Then user of browser1 sees "group1" group on "oneprovider-1" cluster members list
