Feature: Basic management of harvester in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: admin
          group2:
            owner: admin
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as admin to Onezone service


  Scenario: User successfully creates new harvester
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks on Create new harvester button in discovery sidebar
    And user of browser types "harvester1" to name input field in discovery page
    And user of browser types the endpoint of deployed elasticsearch client to endpoint input field in discovery page
    And user of browser clicks on Create button in discovery page
    Then user of browser sees that "harvester1" has appeared on the harvesters list in the sidebar

    And user of browser removes "harvester1" harvester in Onezone page


  Scenario: User fails to create new harvester with invalid endpoint
    When user of browser clicks on Discovery in the main menu
    And user of browser clicks on Create new harvester button in discovery sidebar
    And user of browser types "harvester2" to name input field in discovery page
    And user of browser types "incorrect_endpoint" to endpoint input field in discovery page
    And user of browser clicks on Create button in discovery page
    Then user of browser sees that error popup has appeared


  Scenario: User successfully adds space to harvester using available spaces dropdown
    Given admin user does not have access to any space
    When user of browser creates "space1" space in Onezone
    And user of browser creates "harvester3" harvester in Onezone page

    # add space to harvester
    And user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester3" on the harvesters list in the sidebar
    And user of browser clicks Spaces of "harvester3" harvester in the sidebar
    And user of browser clicks add one of your spaces button in harvester spaces page
    And user of browser sees that "Add one of your spaces" modal has appeared
    And user of browser chooses "space1" from dropdown in add space modal
    And user of browser clicks on "Add" button in modal "Add one of spaces"

    Then user of browser sees that "space1" has appeared on the spaces list in discovery page

    And user of browser removes "harvester3" harvester in Onezone page
    And user of browser leaves "space1" space in Onezone page


  Scenario: User successfully adds space to harvester (with invitation token)
    Given admin user does not have access to any space
    When user of browser creates "space1" space in Onezone
    And user of browser creates "harvester4" harvester in Onezone page

    # copy invitation token
    And user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester4" on the harvesters list in the sidebar
    And user of browser clicks Spaces of "harvester4" harvester in the sidebar
    And user of browser clicks invite space using token button in harvester spaces page
    And user of browser sees that "Invite space using token" modal has appeared
    And user of browser clicks on copy button in active modal
    And user of browser closes "Invite using token" modal

    # join to harvester
    And user of browser adds space "space1" to harvester using copied token

    Then user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester4" on the harvesters list in the sidebar
    And user of browser clicks Spaces of "harvester4" harvester in the sidebar
    And user of browser sees that "space1" has appeared on the spaces list in discovery page

    And user of browser removes "harvester4" harvester in Onezone page
    And user of browser leaves "space1" space in Onezone page


  Scenario: User successfully creates index in harvester
    When user of browser creates "harvester5" harvester in Onezone page

    And user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester5" on the harvesters list in the sidebar
    And user of browser clicks Indices of "harvester5" harvester in the sidebar
    And user of browser clicks "Create new index" in harvester indices page menu
    And user of browser types "index1" to name input field in indices page
    And user of browser clicks on Create button in indices page
    Then user of browser sees that "index1" has appeared on the indices list

    And user of browser removes "harvester5" harvester in Onezone page


  Scenario: User successfully renames harvester
    When user of browser creates "harvester6" harvester in Onezone page

    And user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester6" on the harvesters list in the sidebar
    And user of browser clicks on "Rename" button in harvester "harvester6" menu in the sidebar
    And user of browser types "harvester7" to rename harvester input field
    And user of browser confirms harvester rename using button
    Then user of browser sees that "harvester7" has appeared on the harvesters list in the sidebar
    And user of browser sees that "harvester6" has disappeared from the harvesters list in the sidebar

    And user of browser removes "harvester7" harvester in Onezone page


  Scenario: User successfully leaves harvester
    When user of browser creates "harvester8" harvester in Onezone page

    And user of browser clicks on Discovery in the main menu
    And user of browser clicks "harvester8" on the harvesters list in the sidebar
    And user of browser clicks on "Leave" button in harvester "harvester8" menu in the sidebar
    And user of browser clicks on "Leave" button in modal "Leave harvester"
    And user of browser sees that "harvester8" has disappeared from the harvesters list in the sidebar


  Scenario: User successfully checks harvesting progress
    Given there is no "space1" space in Onezone used by user of browser

    When user of browser creates "space1" space in Onezone

    # support space
    And user of browser sends support token for "space1" to user of browser
    And user of browser clicks on Clusters in the main menu
    And user of browser clicks on "oneprovider-1" in clusters menu
    And user of browser clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser supports "space1" space in "oneprovider-1" Oneprovider panel service with following configuration:
          storage: posix
          size: 100000

    And user of browser uploads "20B-0.txt" to the root directory of "space1" using oneprovider-1 GUI

    And user of browser creates "harvester9" harvester in Onezone page
    And user of browser adds "space1" space to "harvester9" harvester using available spaces dropdown
    And user of browser creates "index1" index in "harvester9" harvester in Discovery page

    # check harvesting progress
    Then user of browser expands "index1" index record in indices page
    And user of browser is idle for 20 seconds
    And user of browser sees 100% progress in "index1" index harvesting

    And user of browser removes "harvester9" harvester in Onezone page
    And user of browser leaves "space1" space in Onezone page


  Scenario: User sees right Invite tokens after filtering them
    Given user admin has no harvesters
    And admin user does not have access to any space
    And using REST, user admin creates ["harvester10", "harvester11"] harvester in "onezone" Onezone service

    When user of browser creates "space1" space in Onezone
    And user of browser creates "space2" space in Onezone
    And user of browser removes all tokens

    And user of browser creates token with following configuration:
          name: space_token_1
          type: invite
          invite type: Invite user to space
          invite target: space1
    And user of browser creates token with following configuration:
          name: space_token_2
          type: invite
          invite type: Invite user to space
          invite target: space2

    And user of browser creates token with following configuration:
          name: harvester_token_10
          type: invite
          invite type: Invite user to harvester
          invite target: harvester10
    And user of browser creates token with following configuration:
          name: harvester_token_11
          type: invite
          invite type: Invite user to harvester
          invite target: harvester11

    And user of browser creates token with following configuration:
          name: group_token_1
          type: invite
          invite type: Invite user to group
          invite target: group1
    And user of browser creates token with following configuration:
          name: group_token_2
          type: invite
          invite type: Invite user to group
          invite target: group2

    And user of browser creates token with following configuration:
          name: cluster_token_1
          type: invite
          invite type: Invite user to cluster
          invite target: oneprovider-1
    And user of browser creates token with following configuration:
          name: cluster_token_2
          type: invite
          invite type: Invite user to cluster
          invite target: oneprovider-2

    And user of browser creates token with following configuration:
          name: register_token_1
          type: invite
          invite type: Register Oneprovider

    And user of browser chooses "Invite" filter in tokens sidebar
    Then user of browser sees exactly 9 item(s) on tokens list in tokens sidebar

    And user of browser chooses "Space" Invite filter in tokens sidebar
    And user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "space_token_1" on tokens list
    And user of browser sees that there is token named "space_token_2" on tokens list
    And user of browser chooses "space2" name Invite filter in tokens sidebar
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "space_token_2" on tokens list

    And user of browser chooses "User" Invite filter in tokens sidebar
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "register_token_1" on tokens list

    And user of browser chooses "Group" Invite filter in tokens sidebar
    And user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "group_token_1" on tokens list
    And user of browser sees that there is token named "group_token_2" on tokens list
    And user of browser chooses "group1" name Invite filter in tokens sidebar
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "group_token_1" on tokens list

    And user of browser chooses "Harvester" Invite filter in tokens sidebar
    And user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "harvester_token_10" on tokens list
    And user of browser sees that there is token named "harvester_token_11" on tokens list
    And user of browser chooses "harvester10" name Invite filter in tokens sidebar
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "harvester_token_10" on tokens list

    And user of browser chooses "Cluster" Invite filter in tokens sidebar
    And user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "cluster_token_1" on tokens list
    And user of browser sees that there is token named "cluster_token_2" on tokens list
    And user of browser chooses "oneprovider-1" name Invite filter in tokens sidebar
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "cluster_token_1" on tokens list

    And user of browser removes all tokens
    And user of browser removes "harvester10" harvester in Onezone page
    And user of browser removes "harvester11" harvester in Onezone page
    And user of browser leaves "space1" space in Onezone page
    And user of browser leaves "space2" space in Onezone page
