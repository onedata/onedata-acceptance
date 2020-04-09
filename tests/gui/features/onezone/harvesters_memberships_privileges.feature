Feature: Basic management of harvester in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User successfully adds user to harvester
    When user of browser1 creates "harvester10" harvester in Onezone page

    # copy invitation token
    And user of browser1 clicks on Discovery in the main menu
    And user of browser1 clicks "harvester10" on the harvesters list in the sidebar
    And user of browser1 clicks Members of "harvester10" harvester in the sidebar
    And user of browser1 clicks on "Invite user using token" button in users list menu in "harvester10" harvester members view
    And user of browser1 copies invitation token from modal
    And user of browser1 clicks on "Cancel" button in modal "Invite using token"
    And user of browser1 sends copied token to user of browser2

    # join to harvester
    And user of browser2 clicks on Tokens in the main menu
    And user of browser2 clicks on "Consume token" button in tokens sidebar
    And user of browser2 pastes copied token into token text field
    And user of browser2 clicks on Join button on tokens page

    Then user of browser2 sees that "harvester10" has appeared on the harvesters list in the sidebar

    And user of browser1 removes "harvester10" harvester in Onezone page


  Scenario: User fails to see harvester without view harvester privilege
    When user of browser1 creates "harvester11" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester11" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester11" has appeared on the harvesters list in the sidebar

    # check view harvester privilege
    And user of browser1 clicks Members of "harvester11" harvester in the sidebar
    And user of browser1 clicks "user1" user in "harvester11" harvester members users list
    And user of browser1 expands "Harvester management" privilege for "user1" user in harvester members subpage
    And user of browser1 unchecks "View harvester" privilege toggle in "Harvester management" for "user1" user in harvester members subpage
    And user of browser1 clicks Save button for "user1" user in harvester members subpage

    And user of browser2 refreshes site
    And user of browser2 clicks Members of "harvester11" harvester in the sidebar
    Then user of browser2 sees Insufficient permissions alert in harvester members subpage
    And user of browser2 clicks Spaces of "harvester11" harvester in the sidebar
    And user of browser2 sees Insufficient permissions alert on Spaces subpage
    And user of browser2 clicks Indices of "harvester11" harvester in the sidebar
    And user of browser2 sees Insufficient permissions alert on Indices subpage

    And user of browser1 removes "harvester11" harvester in Onezone page


  Scenario: User successfully renames harvester with modify harvester privilege
    When user of browser1 creates "harvester12" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester12" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester12" has appeared on the harvesters list in the sidebar

    And user of browser2 renames "harvester12" harvester to "harvester123" in Onezone page
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 checks "Modify harvester" privilege in "Harvester management" privileges group for user1 user in "harvester12" harvester
    Then user of browser2 refreshes site
    And user of browser2 renames "harvester12" harvester to "harvester123" in Onezone page
    And user of browser1 removes "harvester123" harvester in Onezone page


  Scenario: User successfully removes harvester with remove harvester privilege
    When user of browser1 creates "harvester13" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester13" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester13" has appeared on the harvesters list in the sidebar

    And user of browser2 removes "harvester13" harvester in Onezone page
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 checks "Remove harvester" privilege in "Harvester management" privileges group for user1 user in "harvester13" harvester

    And user of browser2 removes "harvester13" harvester in Onezone page
    And user of browser2 sees that "harvester13" has disappeared on the harvesters list in the sidebar


  Scenario: User successfully views privileges with view privileges privilege
    When user of browser1 creates "harvester14" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester14" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester14" has appeared on the harvesters list in the sidebar

    # fail to view privileges
    And user of browser2 clicks Members of "harvester14" harvester in the sidebar
    And user of browser2 clicks "admin" user in "harvester14" harvester members users list
    And user of browser2 sees Insufficient permissions alert in harvester members subpage

    And user of browser1 checks "View privileges" privilege in "Harvester management" privileges group for user1 user in "harvester14" harvester

    # view privileges
    And user of browser2 refreshes site
    And user of browser2 clicks "user1" user in "harvester14" harvester members users list
    Then user of browser2 sees privileges for "user1" user in harvester members subpage

    And user of browser1 removes "harvester14" harvester in Onezone page


  Scenario: User successfully sets privileges with set privileges privilege
    When user of browser1 creates "harvester15" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester15" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester15" has appeared on the harvesters list in the sidebar

    And user of browser2 checks "Harvester management" privileges group for user1 user in "harvester15" harvester
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 checks "Set privileges" privilege in "Harvester management" privileges group for user1 user in "harvester15" harvester

    Then user of browser2 refreshes site
    And user of browser2 checks "Harvester management" privileges group for user1 user in "harvester15" harvester

    And user of browser1 refreshes site
    And user of browser1 clicks "user1" user in "harvester15" harvester members users list
    And user of browser1 sees that "Harvester management" is checked for "user1" user in harvester members subpage

    And user of browser1 removes "harvester15" harvester in Onezone page


  Scenario: User successfully generates invitation token for user with add user privilege
    When user of browser1 creates "harvester16" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester16" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester16" has appeared on the harvesters list in the sidebar

    # fail to generate invitation token for user
    And user of browser2 clicks on Discovery in the main menu
    And user of browser2 clicks "harvester16" on the harvesters list in the sidebar
    And user of browser2 clicks Members of "harvester16" harvester in the sidebar
    And user of browser2 clicks on "Invite user using token" button in users list menu in "harvester16" harvester members view
    And user of browser2 sees This resource could not be loaded alert in Invite user using token modal
    And user of browser2 clicks on "Cancel" button in modal "Invite using token"

    And user of browser1 checks "Add user" privilege in "User management" privileges group for user1 user in "harvester16" harvester

    # generate invitation token for user
    Then user of browser2 clicks on "Invite user using token" button in users list menu in "harvester16" harvester members view
    And user of browser2 sees non-empty token in token area

    And user of browser1 removes "harvester16" harvester in Onezone page


  Scenario: User successfully removes user from harvester with remove user privilege
    When user of browser1 creates "harvester17" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester17" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester17" has appeared on the harvesters list in the sidebar

    # fail to remove user
    And user of browser2 removes "admin" user from "harvester17" harvester members
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 checks "Remove user" privilege in "User management" privileges group for user1 user in "harvester17" harvester

    # remove user
    Then user of browser2 removes "admin" user from "harvester17" harvester members
    And user of browser1 sees that "harvester17" has disappeared on the harvesters list in the sidebar


  Scenario: User successfully adds group to harvester with add group privilege
    When user of browser2 creates group "group1"

    And user of browser1 creates "harvester18" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester18" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester18" has appeared on the harvesters list in the sidebar

    # fail to add group to harvester
    And user of browser2 clicks on Discovery in the main menu
    And user of browser2 clicks "harvester18" on the harvesters list in the sidebar
    And user of browser2 adds "group1" group to "harvester18" harvester using available groups dropdown
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 checks "Add group" privilege in "Group management" privileges group for user1 user in "harvester18" harvester

    Then user of browser2 adds "group1" group to "harvester18" harvester using available groups dropdown
    And user of browser2 sees "group1" group in "harvester18" harvester members groups list

    And user of browser1 removes "harvester18" harvester in Onezone page


  Scenario: User successfully removes group from harvester with remove group privilege
    When user of browser1 creates group "group1"

    And user of browser1 creates "harvester19" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester19" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester19" has appeared on the harvesters list in the sidebar

    # add group to harvester
    Then user of browser1 adds "group1" group to "harvester19" harvester using available groups dropdown

    # fail to remove group from harvester
    And user of browser2 removes "group1" group from "harvester19" harvester members
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 checks "Remove group" privilege in "Group management" privileges group for user1 user in "harvester19" harvester

    # remove group from harvester
    And user of browser2 removes "group1" group from "harvester19" harvester members
    And user of browser2 does not see "group1" group in "harvester19" harvester members groups list

    And user of browser1 removes "harvester19" harvester in Onezone page


  Scenario: User successfully adds space with add space privilege
    Given admin user does not have access to any space
    When user of browser2 creates "space1" space in Onezone

    And user of browser1 creates "harvester20" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester20" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester20" has appeared on the harvesters list in the sidebar

    # fail to add space
    And user of browser2 clicks on Discovery in the main menu
    And user of browser2 adds "space1" space to "harvester20" harvester using available spaces dropdown
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 checks "Add space" privilege in "Space management" privileges group for user1 user in "harvester20" harvester
    And user of browser2 adds "space1" space to "harvester20" harvester using available spaces dropdown

    Then user of browser2 sees that "space1" has appeared on the spaces list in discovery page
    And user of browser1 removes "harvester20" harvester in Onezone page


  Scenario: User successfully removes space with remove space privilege
    Given admin user does not have access to any space
    When user of browser1 creates "space2" space in Onezone
    And user of browser1 creates "harvester21" harvester in Onezone page
    And user of browser1 sends invitation token from "harvester21" harvester to user of browser2
    And user of browser2 joins to harvester in Onezone page
    And user of browser2 sees that "harvester21" has appeared on the harvesters list in the sidebar
    And user of browser1 adds "space2" space to "harvester21" harvester using available spaces dropdown

    # fail to remove space from harvester
    And user of browser2 clicks Spaces of "harvester21" harvester in the sidebar
    And user of browser2 removes "space2" space from harvester
    And user of browser2 sees that error popup has appeared
    And user of browser2 clicks on "Close" button in modal "Error"

    And user of browser1 checks "Remove space" privilege in "Space management" privileges group for user1 user in "harvester21" harvester
    Then user of browser2 removes "space2" space from harvester
    And user of browser1 removes "harvester21" harvester in Onezone page
    And user of browser1 leaves "space2" space in Onezone page


